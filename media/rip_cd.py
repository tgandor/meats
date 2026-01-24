import subprocess
import pycddb
import eyed3
import os

# Set the path to VLC and the CD device (e.g., /dev/cdrom or D: for Windows)
vlc_path = "vlc"  # Change this to the correct path if needed
cd_device = "/dev/cdrom"  # Change this to your CD device

# Output folder for the downloaded files
output_folder = "output"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Use pycddb to fetch CDDB information (track names)
cddb = pycddb.CDDB()
cddb.init()

# Initialize VLC with the CD device
subprocess.run([vlc_path, f"cdda:///{cd_device}"])

# Fetch CDDB information for the CD
disc_id = cddb.compute_discid(cd_device)
disc_info = cddb.get_disc(disc_id)

# Initialize eyed3 for tagging
tagger = eyed3.Tag()

# Iterate through each track and rip it
for track_number, track in enumerate(disc_info.tracks, start=1):
    track_name = track.title
    output_file = os.path.join(output_folder, f"{track_number:02d} - {track_name}.mp3")

    # Rip the track to MP3 format using VLC
    subprocess.run([vlc_path, f"cdda:///{cd_device}", f"--sout=file/mp3:{output_file}"])

    # Fill out ID3v2 tags
    audiofile = eyed3.load(output_file)
    audiofile.tag.title = track_name
    audiofile.tag.artist = disc_info.artist
    audiofile.tag.album = disc_info.title
    audiofile.tag.track_num = (track_number, len(disc_info.tracks))
    audiofile.tag.save()

print("CD ripping and tagging complete.")
