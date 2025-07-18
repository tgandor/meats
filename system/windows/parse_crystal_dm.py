import re
import json
import pyperclip
from datetime import datetime


def parse_cdm_output(text):
    results = {"device": None, "test_date": None, "results": {}}

    current_section = None
    pattern = re.compile(
        r"(?P<type>SEQ|RND)\s+(?P<size>\d+[KMiB]+)\s+\(Q=\s*(?P<qd>\d+),\s*T=\s*(?P<threads>\d+)\):\s+"
        r"(?P<mbps>[\d.]+)\s+MB/s\s+\[\s*(?P<iops>[\d.]+)\s+IOPS\]\s+<\s*(?P<latency>[\d.]+)\s+us>"
    )

    unit_letter = "X"
    label = "Unknown"
    size_gb = "0"
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
            try:
                unit_letter = "X"
                letter_match = re.search(r"\[(\w):", line)
                if letter_match:
                    unit_letter = letter_match.group(1)
                size_match = re.search(r"\((\d+)/(\d+)GiB\)", line)
                if size_match:
                    size_gb = size_match.group(2)
            except Exception:
                pass

        if "Profile:" in line:
            label = line.split("Profile:")[1].strip()

    return results, dt, unit_letter, label, size_gb


# Main execution
text = pyperclip.paste()
parsed_data, dt, unit, label, size = parse_cdm_output(text)

filename = f"{dt.strftime('%Y%m%d_%H%M')}_{unit}_{label.replace(' ', '')}_{size}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, indent=2)

print(f"✅ Datos guardados en el archivo: {filename}")
