#!/usr/bin/env python

from __future__ import division
from __future__ import print_function

import argparse
import glob
import os
import time


def _parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--amf", action="store_true", help="use h264_amf codec (e.g. Windows on AMD)"
    )
    parser.add_argument(
        "--bitrate-audio", "-ba", help="specify output bitrate for audio"
    )
    parser.add_argument("--bitrate", "-b", help="specify output bitrate for video")
    parser.add_argument(
        "--classify",
        "-k",
        action="store_true",
        help="detect weak or negative (nocebo) compression",
    )
    parser.add_argument(
        "--converter", help="Manually specify [full path to] ffmpeg or avconv"
    )
    parser.add_argument("--copy-audio", "-c", action="store_true")
    parser.add_argument("--copy-video", "-cv", action="store_true")
    parser.add_argument(
        "--copy",
        "-C",
        action="store_true",
        help="No-op copy, e.g. for cutting or remuxing",
    )
    parser.add_argument(
        "--deinterlace",
        "-d",
        action="store_true",
        help="deinterlace with yadif (requires recoding)",
    )
    parser.add_argument(
        "--dry-run", "-n", action="store_true", help="print commands, but do nothing"
    )
    parser.add_argument("--duration", "-t", help="Duration limit for encoding")
    parser.add_argument(
        "--evaluate",
        "-e",
        action="store_true",
        help="move result to placebo/ if size after > 80%%",
    )
    parser.add_argument(
        "--fix-avidemux",
        action="store_true",
        help="rotate 90 via metadata (use as only option)",
    )
    parser.add_argument("--framerate", "-r", help="specify output FPS for video")
    parser.add_argument(
        "--here",
        "-H",
        action="store_true",
        help="convert to the same place (only from other format)",
    )
    parser.add_argument("--delete", "-D", action="store_true", help="DELETE original")
    parser.add_argument("--hevc", action="store_true", help="use h.265 (HEVC) codec")
    parser.add_argument("--hwaccel", "-hw", help="specify input hardware acceleration")
    parser.add_argument(
        "--move",
        "-m",
        action="store_true",
        help="move original file to original/ directory",
    )
    parser.add_argument("--name-suffix", "-ns", help="")
    parser.add_argument(
        "--nv",
        "-nv",
        action="store_true",
        help="Enable both nvdec and nvenc for transcoding",
    )
    parser.add_argument("--nvdec", "-nvd", action="store_true")
    parser.add_argument("--nvenc", "-nve", action="store_true")
    parser.add_argument("--quality", "-q", type=int, default=23)
    parser.add_argument("--scale", "-s", help="scale video filter, eg. 960:-1")
    parser.add_argument("--rot180", action="store_true", help="rotate video 180 degrees")
    parser.add_argument("--rotR", action="store_true", help="rotate video 90 degrees CW")
    parser.add_argument("--rotL", action="store_true", help="rotate video 90 degrees CCW")
    parser.add_argument("--stabilize", "-stab", action="store_true")
    parser.add_argument(
        "--start", "-ss", help="Start time for encoding in seconds or [HH:]MM:SS"
    )
    parser.add_argument("files_or_globs", nargs="+")
    return parser.parse_args()


def makedirs(path, exist_ok=True):
    # Py 2.7 planned obsolescence (not including trivial feature improvements)
    if exist_ok and os.path.exists(path):
        return
    os.makedirs(path)


def duration_format(duration):
    """Format a float of seconds as number and H:M:S string.

    For example:
    >>> duration_format(123)
    '123.00 s (00:02:03)'

    >>> duration_format(12345.67)
    '12345.67 s (03:25:45)'
    """
    duration_tuple = time.gmtime(duration)
    return "{:.2f} s ({})".format(
        float(duration), time.strftime("%H:%M:%S", duration_tuple)
    )


def time_format(timestamp):
    time_tuple = time.gmtime(timestamp)
    return time.strftime("%H:%M:%S", time_tuple)


class TimedSystem:
    def __init__(self):
        self.total = 0
        self.log = []

    def run(self, command):
        start = time.time()
        print(time.strftime("%H:%M:%S"), "starting", command)
        status = os.system(command)
        finish = time.time()
        elapsed = finish - start
        print(time.strftime("%H:%M:%S"), "finished in: ", duration_format(elapsed))
        self.total += elapsed
        self.log.append((command, start, finish, elapsed))
        if status != 0:
            raise RuntimeError(
                "Error (status={}) executing command: {}".format(status, command)
            )
        return status

    def report(self):
        for command, start, finish, elapsed in self.log:
            print(time_format(start), command)
            print(time_format(finish), "took:", duration_format(elapsed))
        print(time.strftime("%H:%M:%S"), "Finished in: ", duration_format(self.total))


def ratio_format(pre, post):
    return "{:,}\t{:,}\t{:.1f}%\t{:.1f}x\t{:,}".format(
        pre, post, 100 * post / pre, pre / post, post - pre
    )


class CompressionStats:
    def __init__(self):
        self.items = []
        self.total_pre = 0
        self.total_post = 0

    def add(self, before, after):
        size_pre = os.path.getsize(before)
        size_post = os.path.getsize(after)
        if size_post == 0:
            raise ValueError("Empty output file: {}".format(after))
        self.total_pre += size_pre
        self.total_post += size_post
        self.items.append((os.path.basename(before), size_pre, size_post))
        return size_pre / size_post

    def report(self):
        if not self.items:
            print("No compression stats to report.")
            return

        for name, before, after in self.items:
            print("{}\t{}".format(name, ratio_format(before, after)))
        print("Total:\t{}".format(ratio_format(self.total_pre, self.total_post)))


try:
    from shutil import which
except ImportError:

    def which(program):
        # https://stackoverflow.com/a/377028/1338797
        import os

        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None


def _validate_args(args):
    if args.here and args.evaluate:
        raise ValueError("--here and --evaluate are conflicting options.")


def _get_encoder_options(args):
    common_options = " -hide_banner -map_metadata 0 -pix_fmt yuv420p -strict -2"

    if args.copy or args.fix_avidemux or args.copy_video:
        return "copy" + common_options

    if args.nv or args.nvenc:
        codec = "hevc_nvenc" if args.hevc else "h264_nvenc"
        encoder_options = "{} -cq {} -preset slow {}".format(
            codec, args.quality, common_options
        )
        # this looks promising, but for now produces overkill
        # https://superuser.com/a/1236387/269542
        # encoder_options = ('h264_nvenc -preset llhq -rc:v vbr_minqp -qmin:v 19 -qmax:v 21 -b:v 2500k '
        #                    '-maxrate:v 5000k -profile:v high ' + common_options)
    elif args.amf:
        if args.hevc:
            raise ValueError("Not implemented")
        encoder_options = "h264_amf {}".format(common_options)
        if not args.bitrate:
            print("Warning - using --amf codec without --bitrate/-b specified.")
    else:
        if args.hevc:
            raise ValueError("Not implemented")
        encoder_options = "h264 -crf {} -preset veryslow {}".format(
            args.quality, common_options
        )

    if args.bitrate:
        encoder_options += " -b:v {}".format(args.bitrate)

    if args.framerate:
        encoder_options += " -r {}".format(args.framerate)

    return encoder_options


def _get_filters(args):
    filters = ""

    if args.deinterlace:
        filters += " -vf yadif"

    if args.scale:
        filters += " -vf scale=" + args.scale

    if args.stabilize:
        filters += " -vf vidstabtransform,unsharp=5:5:0.8:3:3:0.4"

    if args.fix_avidemux:
        filters += ' -metadata:s:v rotate="270"'

    if args.rot180:
        filters += ' -vf vflip,hflip'

    if args.rotL:
        filters += ' -vf transpose=2'

    if args.rotR:
        filters += ' -vf transpose=1'

    return filters


def _get_input_options(args):
    input_options = ""

    if args.nv or args.nvdec:
        input_options += "-hwaccel nvdec"
    if args.hwaccel:
        input_options += "-hwaccel {}".format(args.hwaccel)
    if args.start:
        input_options += " -ss {}".format(args.start)
    if args.duration:
        input_options += " -t {}".format(args.duration)

    return input_options


def _iter_files(files_or_globs):
    for pattern in files_or_globs:
        if os.path.exists(pattern):
            yield pattern
        else:
            for path in glob.glob(pattern):
                yield path


def _main():
    args = _parse_cli()
    _validate_args(args)

    if args.move and not args.dry_run:
        makedirs("original", exist_ok=True)
    if not args.here and not args.dry_run:
        makedirs("converted", exist_ok=True)

    converter = args.converter
    if converter is None:
        converter = which("ffmpeg")
    if converter is None:
        converter = which("avconv")
    if converter is None:
        # Py2 on Windows, rarely nowadays
        converter = which("ffmpeg.exe")
    if converter is None:
        print("Neither ffmpeg nor avconv found.")
        exit()

    print("Using:", converter)

    ts = TimedSystem()
    stats = CompressionStats()

    files = list(_iter_files(args.files_or_globs))
    for i, filename in enumerate(files, 1):
        print(i, "/", len(files), filename)
        basename = os.path.basename(filename)

        if args.move:
            original = os.path.join("original", basename)
            if not args.dry_run:
                os.rename(filename, original)
        else:
            original = filename

        if args.stabilize:
            preprocessing = '{} -i "{}" -vf vidstabdetect -f null -'.format(
                converter, original
            )
            ts.run(preprocessing)

        if args.here:
            converted = os.path.splitext(filename)[0] + ".mp4"
            if converted == filename:
                print("Cannot convert", filename, "here (same file).")
                continue
        else:
            converted = (
                os.path.splitext(os.path.join("converted", basename))[0] + ".mp4"
            )

        if os.path.exists(converted):
            print("Skipping, output exists:", converted)
            continue

        audio_options = "aac"
        if args.copy_audio or args.copy or args.fix_avidemux:
            audio_options = "copy"
        elif args.bitrate_audio:
            audio_options += " -b:a " + args.bitrate_audio

        commandline = '{} {} -i "{}" {} -c:a {} -c:v {} "{}"'.format(
            converter,
            _get_input_options(args),
            original,
            _get_filters(args),
            audio_options,
            _get_encoder_options(args),
            converted,
        )

        if args.dry_run:
            print(commandline)
            continue

        try:
            ts.run(commandline)
        except RuntimeError:
            if os.path.getsize(converted) == 0:
                print("WARNING: removing empty:", converted)
                os.unlink(converted)
            raise

        ratio = stats.add(original, converted)

        if args.evaluate and ratio < 1.25:
            dump_dir = "placebo" if ratio > 1 else "nocebo"
            print(basename, "compressed {:.1f}x".format(ratio), "which is", dump_dir)
            makedirs(dump_dir, exist_ok=True)
            os.rename(converted, os.path.join(dump_dir, os.path.basename(converted)))

        if args.delete:
            print("Deleting:", original)
            os.unlink(original)

    if not args.dry_run:
        ts.report()
        stats.report()


if __name__ == "__main__":
    _main()
