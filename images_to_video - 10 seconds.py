#!/usr/bin/env python3
import sys
import os
import subprocess
import tempfile

# ===============================
# CONFIG
# ===============================
DURATION = 10      # seconds per image
WIDTH = 1080
HEIGHT = 1920
FPS = 30
BITRATE = "6000k"
# ===============================

if len(sys.argv) < 2:
    print("Drag and drop image files onto this script.")
    sys.exit(1)

images = sys.argv[1:]
first_name = os.path.splitext(os.path.basename(images[0]))[0]
output = f"{first_name}_combined.mp4"

# Temporary file for FFmpeg concat
with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tf:
    for img in images:
        tf.write(f"file '{os.path.abspath(img)}'\n")
        tf.write(f"duration {DURATION}\n")
    tf.write(f"file '{os.path.abspath(images[-1])}'\n")  # last image repeat
    concat_file = tf.name

# FFmpeg command
vf_filter = (
    f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
    f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:black"
)

cmd = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_file,
    "-vf", vf_filter,
    "-r", str(FPS),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-profile:v", "high",
    "-b:v", BITRATE,
    "-movflags", "+faststart",
    output
]

print("Running FFmpeg:")
print(" ".join(cmd))
subprocess.run(cmd, check=True)

# Cleanup
os.remove(concat_file)
print(f"\n✔ Done. Output saved as: {output}")
