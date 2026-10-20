#!/usr/bin/env bash
set -euo pipefail

if (($# == 0)); then
    echo "usage: $0 <audio-or-video> [whisper options...]"
    exit 1
fi

OUTROOT="results"
mkdir -p "$OUTROOT"

args=("$@")

lang_en=0
for ((i=0; i<${#args[@]}; i++)); do
    if [[ ${args[i]} == "--language" ]]; then
        if ((i + 1 < ${#args[@]})) && [[ ${args[i+1]} == "en" ]]; then
            lang_en=1
        fi
    fi
done

models=(
    default
    base
    small
    medium
    large
    turbo
)

if ((lang_en)); then
    models+=(
        tiny.en
        base.en
        small.en
        medium.en
    )
fi

run_one() {
    local model="$1"
    local temp="$2"

    local dirname

    if [[ "$model" == "default" ]]; then
        dirname="default"
    else
        dirname="$model"
    fi

    if [[ "$temp" == "0" ]]; then
        dirname="${dirname}_t0"
    fi

    local outdir="${OUTROOT}/${dirname}"
    mkdir -p "$outdir"

    local cmd=(whisper)

    if [[ "$model" != "default" ]]; then
        cmd+=(--model "$model")
    fi

    if [[ "$temp" == "0" ]]; then
        cmd+=(--temperature 0)
    fi

    cmd+=("${args[@]}")

    printf '%q ' "${cmd[@]}" > "${outdir}/command.txt"
    echo >> "${outdir}/command.txt"

    echo
    echo "============================================================"
    echo "Running: ${dirname}"
    echo "============================================================"

    local start end elapsed

    start=$(date +%s)

    "${cmd[@]}"

    end=$(date +%s)
    elapsed=$((end - start))

    echo "${elapsed}" > "${outdir}/elapsed.txt"

    find . -maxdepth 1 -type f \
        \( \
            -name '*.txt' -o \
            -name '*.srt' -o \
            -name '*.vtt' -o \
            -name '*.json' \
        \) \
        -exec mv -f {} "${outdir}/" \;

    echo "elapsed=${elapsed}s"
}

for model in "${models[@]}"; do
    run_one "$model" default
    run_one "$model" 0
done

