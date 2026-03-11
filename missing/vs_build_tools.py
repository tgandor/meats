import ctypes
import json
import os
import subprocess

if "ProgramFiles(x86)" not in os.environ:
    exit("Probably not Windows")

vs_where = os.path.join(
    os.environ["ProgramFiles(x86)"],
    "Microsoft Visual Studio",
    "Installer",
    "vswhere.exe",
)

if not os.path.exists(vs_where):
    exit("No Visual Studio components (vswhere.exe missing)")

command = [
    vs_where,
    "-products",
    "Microsoft.VisualStudio.Product.BuildTools",
    "-format",
    "json",
]

# Pobierz kodowanie OEM konsoli z Windows API (cp850 w PL, cp437 w US, etc.)
console_cp = ctypes.windll.kernel32.GetConsoleOutputCP()
console_encoding = f"cp{console_cp}"

raw, _ = subprocess.Popen(
    command, stdout=subprocess.PIPE, encoding=console_encoding
).communicate()

data = json.loads(raw)
print(data)

for toolset in data:
    print(f"Visual Studio Build Tools {toolset['installationVersion']} at {toolset['installationPath']}")
    print("Activate with:")
    print(f'"{toolset["productPath"]}"\n\n')
