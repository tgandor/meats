#!/usr/bin/env python
import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Split:
    start: datetime
    description: str


def parse_splits(path):
    data = open(path).read().strip().split("\n")
    result = []
    for l1 in data:
        words = l1.split()
        if len(words) > 1 and words[1] == "--":
            continue
        start = datetime.strptime(words[0], "%H:%M:%S")
        result.append(Split(start, "_".join(words[1:])))
    return result


def extract_text_chunks(json_result, splits, n_chunks=2):
    text_chunks = defaultdict(list)

    for entry in json_result:
        start_seconds = float(entry["start"])
        start_time = str(timedelta(seconds=start_seconds))
        timestamp = datetime.strptime(start_time, "%H:%M:%S")

        for split in splits:
            if timestamp >= split.start and len(text_chunks[split.start]) < n_chunks:
                text_chunks[split.start].append(entry["text"])
                break
    return text_chunks


def main():
    parser = argparse.ArgumentParser(
        description="Extract text chunks based on timestamps."
    )
    parser.add_argument("json_file", help="Path to the JSON result file")
    parser.add_argument("timestamps_file", help="Path to the timestamps file")
    args = parser.parse_args()

    splits = parse_splits(args.timestamps_file)
    with open(args.json_file, "r") as json_file:
        json_result = json.load(json_file)
    text_chunks = extract_text_chunks(json_result, splits)
    width = len(str(len(splits)))

    for idx, split in enumerate(splits, 1):
        description = " ".join(chunk.strip() for chunk in text_chunks[split.start])
        filename = f"{idx:0{width}d}_{split.description}.txt"
        print(
            f'Timestamp: {split.start.strftime("%H:%M:%S")}, File: {filename}, Text: {description}'
        )
        with open(filename, "w") as descr:
            descr.write(description + "\n")


if __name__ == "__main__":
    main()
