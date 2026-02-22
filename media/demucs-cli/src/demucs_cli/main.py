import os
import sys
import pathlib
import tempfile
import subprocess
from typing import List, Optional

import torch
import torchaudio
import soundfile as sf
import typer
from rich import print
from rich.progress import track
from glob import glob

app = typer.Typer(add_completion=False)

def _load_model(model_name: str = "dns48", device: Optional[str] = None):
    """
    Ładuje model przez PyTorch Hub (auto-cache w ~/.cache/torch/hub).
    Dostępne nazwy w hubconf.py to m.in. 'dns48' (48 kHz).
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    # facebookresearch/denoiser ma hubconf.py z definicją modeli i pre-trained wag
    # https://github.com/facebookresearch/denoiser  (hubconf)
    model = torch.hub.load("facebookresearch/denoiser", model_name)  # ściągnie do ~/.cache/torch/hub
    model.to(device)
    model.eval()
    return model, device

def _ensure_mono(wave: torch.Tensor) -> torch.Tensor:
    # wave: [channels, samples]; wymuszamy mono
    if wave.ndim == 1:
        wave = wave.unsqueeze(0)
    if wave.size(0) > 1:
        wave = wave.mean(dim=0, keepdim=True)
    return wave

def _resample_if_needed(wave: torch.Tensor, sr: int, target_sr: int) -> (torch.Tensor, int):
    if sr == target_sr:
        return wave, sr
    wave = torchaudio.functional.resample(wave, orig_freq=sr, new_freq=target_sr)
    return wave, target_sr

def _safe_out_path(in_path: pathlib.Path, out: Optional[str]) -> pathlib.Path:
    if out is None:
        return in_path.with_name(in_path.stem + "_clean" + in_path.suffix)
    out_p = pathlib.Path(out)
    if out_p.suffix:  # plik
        return out_p
    # katalog
    out_p.mkdir(parents=True, exist_ok=True)
    return out_p / in_path.name.replace(in_path.suffix, f"_clean{in_path.suffix}")

def _write_mp3(tmp_wav: pathlib.Path, out_path: pathlib.Path, bitrate="192k"):
    # transkodujemy do mp3 przez ffmpeg (najpewniej obecny w systemie użytkownika)
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(tmp_wav),
        "-c:a", "libmp3lame", "-b:a", bitrate,
        str(out_path),
    ]
    subprocess.run(cmd, check=True)

def _process_file(path: str, out: Optional[str], model, device: str, model_sr: int = 48000):
    in_path = pathlib.Path(path)
    if not in_path.exists():
        print(f"[red]Plik nie istnieje:[/red] {path}")
        return 1

    # 1) wczytanie przez torchaudio (obsługuje mp3)
    wave, sr = torchaudio.load(str(in_path))  # [C, N], int16/float32 -> float32
    wave = wave.float()
    wave = _ensure_mono(wave)

    # 2) resample -> model_sr (dns48: 48 kHz)
    wave, sr = _resample_if_needed(wave, sr, model_sr)

    # 3) denoise (streamowo po blokach, ale dla prostoty całość naraz)
    wave = wave.to(device)
    with torch.no_grad():
        # modele Demucs w denoiser działają w dziedzinie czasu, zwracają odszumiony sygnał
        enhanced = model(wave)[0].cpu()

    # 4) zapis tymczasowy WAV @ model_sr
    out_path = _safe_out_path(in_path, out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp_wav = pathlib.Path(td) / "tmp.wav"
        sf.write(str(tmp_wav), enhanced.squeeze(0).numpy(), model_sr)

        # 5) jeśli rozszerzenie docelowe to mp3 -> koduj mp3; jeśli nie, zapisz wav
        if out_path.suffix.lower() == ".mp3" or in_path.suffix.lower() == ".mp3":
            _write_mp3(tmp_wav, out_path)
        else:
            # zapis bezpośredni WAV
            out_wav = out_path.with_suffix(".wav")
            out_wav.write_bytes(tmp_wav.read_bytes())

    print(f"[green]OK:[/green] {in_path.name} -> {out_path}")
    return 0

@app.command()
def main(
    inputs: List[str] = typer.Argument(..., help="Pliki wejściowe lub wzorce globowe (np. '*.mp3')"),
    o: Optional[str] = typer.Option(None, "--output", "-o", help="Plik wyjściowy lub katalog wyjściowy"),
    model_name: str = typer.Option("dns48", help="Model z PyTorch Hub (np. dns48)"),
    bitrate: str = typer.Option("192k", help="Bitrate MP3 dla wyjścia MP3"),
):
    """
    Proste CLI do odszumiania mowy (Demucs/Denoiser).
    Obsługuje:
      denoise file.mp3            -> file_clean.mp3
      denoise x.mp3 -o y.mp3      -> dokładny plik wyjściowy
      denoise '*.mp3' -o outdir/  -> wsadowo do katalogu
    """
    # Rozwiń wzorce (glob), aby działało też w PowerShell/cmd
    files = []
    for pattern in inputs:
        expanded = glob(pattern)
        if expanded:
            files.extend(expanded)
        else:
            files.append(pattern)

    if not files:
        print("[red]Brak plików do przetworzenia.[/red]")
        raise typer.Exit(code=2)

    model, device = _load_model(model_name=model_name)

    # Przetwarzanie wsadowe
    rc = 0
    for f in track(files, description="Denoising..."):
        try:
            rc |= _process_file(f, o, model, device, model_sr=48000)
        except subprocess.CalledProcessError as e:
            print(f"[red]FFmpeg błąd:[/red] {e}")
            rc |= 1
        except Exception as e:
            print(f"[red]Błąd:[/red] {f} -> {e}")
            rc |= 1

    raise typer.Exit(code=rc)

# Zgodnie z [project.scripts] wywołanie: denoise -> app
app = typer.Typer()
app.command()(main)
