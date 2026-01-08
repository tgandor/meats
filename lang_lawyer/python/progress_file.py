import sys
import time


class ProgressFile:
    """
    Wrap a text file handle for psycopg2 copy_expert.
    Reports progress (bytes, lines, rate) to stderr.
    """
    def __init__(self, fh, label="COPY", report_every_bytes=5_000_000, report_every_secs=1.0):
        self.fh = fh              # text-mode file object
        self.label = label
        self.bytes = 0
        self.lines = 0
        self._last_report_bytes = 0
        self._last_report_time = time.time()
        self._report_every_bytes = report_every_bytes
        self._report_every_secs = report_every_secs
        self._eof = False

    def readline(self):
        """Read a single line (psycopg2 may use this method)."""
        line = self.fh.readline()
        if not line:
            self._eof = True
            # Final report
            self._report(final=True)
            return line

        self.bytes += len(line)
        self.lines += 1
        self._report()
        return line

    def read(self, size=-1):
        """Read up to `size` chars (psycopg2 uses str in text mode)."""
        chunk = self.fh.read(size)
        if not chunk:
            self._eof = True
            # Final report
            self._report(final=True)
            return chunk

        self.bytes += len(chunk)
        # Count lines cheaply (works for CSV; not exact if quoted newlines inside fields)
        self.lines += chunk.count("\n")
        self._report()
        return chunk

    def _report(self, final=False):
        now = time.time()
        need_bytes = (self.bytes - self._last_report_bytes) >= self._report_every_bytes
        need_time = (now - self._last_report_time) >= self._report_every_secs
        if final or need_bytes or need_time:
            dt = max(now - self._last_report_time, 1e-6)
            dbytes = self.bytes - self._last_report_bytes
            rate = dbytes / dt
            # One-line status for tmux-friendly output; overwrite in-place
            msg = (f"{self.label}: {self.bytes/1e6:.1f} MB, "
                   f"{self.lines:,} lines, {rate/1e6:.2f} MB/s\r")
            print(msg, file=sys.stderr)
            self._last_report_time = now
            self._last_report_bytes = self.bytes

    def close(self):
        self.fh.close()

    def __getattr__(self, name):
        return getattr(self.fh, name)

