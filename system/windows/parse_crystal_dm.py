import re
import json
import pyperclip
import subprocess
from datetime import datetime


def parse_cdm_output(text):
    results = {"device": None, "test_date": None, "results": {}}

    current_section = None
    pattern = re.compile(
        r"(?P<type>SEQ|RND)\s+(?P<size>\d+[KMiB]+)\s+\(Q=\s*(?P<qd>\d+),\s*T=\s*(?P<threads>\d+)\):\s+"
        r"(?P<mbps>[\d.]+)\s+MB/s\s+\[\s*(?P<iops>[\d.]+)\s+IOPS\]\s+<\s*(?P<latency>[\d.]+)\s+us>"
    )

    drive_letter = None
    label = "Unknown"
    size_gib = "Unknown"
    dt = datetime.now()

    for line in text.splitlines():
        line = line.strip()

        if line == "[Read]":
            current_section = "read"
            continue
        elif line == "[Write]":
            current_section = "write"
            continue

        match = pattern.search(line)
        if match and current_section:
            key = f"{match.group('type')}_{match.group('size')}_Q{match.group('qd')}T{match.group('threads')}"
            if key not in results["results"]:
                results["results"][key] = {}
            results["results"][key][current_section] = {
                "MBps": float(match.group("mbps")),
                "IOPS": float(match.group("iops")),
                "latency_us": float(match.group("latency")),
            }

        if line.startswith("Date:"):
            try:
                date_str = line.split("Date:")[1].strip()
                dt = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
                results["test_date"] = dt.isoformat()
            except Exception:
                dt = datetime.now()

        if "Test:" in line and "[" in line:
            match_drive = re.search(r"\[(\w):\s+\d+%", line)
            match_size = re.search(r"\((\d+)/(\d+)GiB\)", line)
            if match_drive:
                drive_letter = match_drive.group(1)
            if match_size:
                size_gib = str(int(match_size.group(2)))

    if drive_letter:
        try:
            ps_command = f"(Get-Volume -DriveLetter '{drive_letter}').FileSystemLabel"
            label = subprocess.check_output(
                ["powershell", "-Command", ps_command], text=True
            ).strip()
            if not label:
                label = "NoLabel"
        except Exception:
            print(f"Error retrieving label for drive {drive_letter}")
            label = "Error"

    filename = f"{dt.strftime('%Y%m%d_%H%M')}_{drive_letter}_{label}_{size_gib}G.json"

    return results, filename


if __name__ == "__main__":
    text = pyperclip.paste()
    parsed_data, filename = parse_cdm_output(text)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2)

    print(f"✅ Datos guardados en {filename}")
