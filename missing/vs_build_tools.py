import os
import json
import subprocess

if "ProgramFiles(x86)" not in os.environ:
    exit("Probably not Windows")

vs_where = os.path.join(
    os.environ["ProgramFiles(x86)"],
    "Microsoft Visual Studio",
    "Installer",
    "vswhere.exe",
)

if not os.path.exists("vs_where"):
    exit("No Visual Studio components (vswhere.exe missing)")

command = [
    vs_where,
    "-products",
    "Microsoft.VisualStudio.Product.BuildTools",
    "-format",
    "json",
]

raw, _ = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()

data = json.loads(raw.decode())
print(data)
