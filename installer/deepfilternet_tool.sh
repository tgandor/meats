#!/usr/bin/env bash
# Instaluje DeepFilterNet jako izolowane uv tool (nie w globalnych site-packages).
#
# Użycie:
#   ./deepfilternet_tool.sh              # CPU-only torch (domyślnie, ~700 MB)
#   ./deepfilternet_tool.sh cpu          # to samo, jawnie
#   ./deepfilternet_tool.sh cu124        # CUDA 12.4 (~2.5 GB)
#   ./deepfilternet_tool.sh cu121        # CUDA 12.1
#   ./deepfilternet_tool.sh cu118        # CUDA 11.8
#
# Wymagania: uv (https://docs.astral.sh/uv/getting-started/installation/)
#   uv instalacja: curl -LsSf https://astral.sh/uv/install.sh | sh
#
# Testowano na: Windows 10/11, Ubuntu 24.04 / WSL2.
#
# Uwagi techniczne (odkryte empirycznie):
#   - deepfilternet 0.5.6 wymaga deepfilterlib (Rust), który ma koła tylko do Python 3.11
#     → używamy --python 3.11
#   - torchaudio ≥2.4 przeniosło AudioMetaData; deepfilternet 0.5.6 używa starego API
#     → ograniczamy do torch/torchaudio <2.4 (np. 2.3.1 działa)
#   - deepfilternet wymaga numpy<2 (konflikt z nowszym numpy)
#   - Indeks PyTorch ma swój pakiet `packaging` który blokuje rozwiązanie zależności
#     → konieczne --index-strategy unsafe-best-match

set -euo pipefail

TORCH_FLAVOR="${1:-cpu}"

case "$TORCH_FLAVOR" in
    cpu|cu*)
        PYTORCH_INDEX="https://download.pytorch.org/whl/${TORCH_FLAVOR}"
        ;;
    *)
        echo "Nieznany wariant torch: '$TORCH_FLAVOR'" >&2
        echo "Dostępne: cpu, cu124, cu121, cu118" >&2
        exit 1
        ;;
esac

echo "=== DeepFilterNet install ==="
echo "  Paczka  : deepfilternet 0.5.6"
echo "  Python  : 3.11"
echo "  Torch   : $TORCH_FLAVOR (${PYTORCH_INDEX})"
echo ""

uv tool install "deepfilternet==0.5.6" \
    --python 3.11 \
    --with "torch<2.4" \
    --with "torchaudio<2.4" \
    --with "numpy<2" \
    --extra-index-url "${PYTORCH_INDEX}" \
    --index-strategy unsafe-best-match

echo ""
echo "=== Test instalacji ==="
deepFilter --help | head -5

echo ""
echo "Gotowe! Przykładowe użycie:"
echo "  deepFilter plik.wav                              # odszumiony -> plik_DeepFilterNet2.wav"
echo "  deepFilter -i plik.wav -o katalog_wynikowy/"
echo "  deepFilter --atten-lim 40 plik.wav              # maks. 40 dB tłumienia"
