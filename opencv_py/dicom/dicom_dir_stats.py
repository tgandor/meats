import os
import sys
import argparse
import pydicom
from pydicom.errors import InvalidDicomError
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(
        description="Skrypt do analizy i grupowania plików DICOM według serii."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Ścieżki do katalogów lub pojedynczych plików .dcm"
    )
    return parser.parse_args()


def collect_dicom_files(paths):
    """Zbiera wszystkie ścieżki do plików z przekazanych argumentów."""
    files_to_process = []
    for path in paths:
        if os.path.isfile(path):
            files_to_process.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    files_to_process.append(os.path.join(root, file))
        else:
            print(f"[OSTRZEŻENIE] Ścieżka nie istnieje: {path}")
    return files_to_process


def get_transfer_syntax_info(ds):
    """Rozpoznaje Transfer Syntax UID i sprawdza, czy występuje kompresja."""
    ts_uid = getattr(ds.file_meta, 'TransferSyntaxUID', None)
    if not ts_uid:
        return "Brak danych o Transfer Syntax"
    
    name = ts_uid.name
    is_compressed = ts_uid.is_compressed
    
    if is_compressed:
        return f"Kompresja: {name} (UID: {ts_uid})"
    else:
        return f"Brak kompresji: {name} (UID: {ts_uid})"


def analyze_dicoms(file_paths):
    """Wczytuje pliki DICOM i grupuje je według SeriesInstanceUID."""
    series_data = defaultdict(list)
    skipped_files = 0

    for file_path in file_paths:
        try:
            # Wczytujemy nagłówek i tagi (stop_before_pixels=True przyspiesza działanie)
            ds = pydicom.dcmread(file_path, stop_before_pixels=True, force=False)
            
            # Weryfikacja czy plik ma SeriesInstanceUID
            series_uid = getattr(ds, 'SeriesInstanceUID', 'Brak_SeriesInstanceUID')
            series_data[series_uid].append(ds)

        except (InvalidDicomError, IsADirectoryError, PermissionError):
            skipped_files += 1
            continue
        except Exception as e:
            skipped_files += 1
            continue

    return series_data, skipped_files


def calculate_bbox(ipp_list):
    """Oblicza Bounding Box (min/max X, Y, Z) z listy pozycji IPP."""
    if not ipp_list:
        return None
    
    xs = [ipp[0] for ipp in ipp_list]
    ys = [ipp[1] for ipp in ipp_list]
    zs = [ipp[2] for ipp in ipp_list]

    return {
        'min': (min(xs), min(ys), min(zs)),
        'max': (max(xs), max(ys), max(zs)),
        'extent': (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    }


def print_report(series_data, skipped_files):
    """Wyświetla sformatowane podsumowanie w konsoli."""
    print("=" * 80)
    print(f" PODSUMOWANIE ANALIZY DICOM")
    print(f" Znaleziono unikalnych serii: {len(series_data)}")
    print(f" Pominięto plików (nie-DICOM lub błędy): {skipped_files}")
    print("=" * 80)

    for idx, (series_uid, datasets) in enumerate(series_data.items(), 1):
        sample = datasets[0]  # Metadane reprezentatywne dla serii

        # --- Tagi Badania (Study) ---
        patient_id = getattr(sample, 'PatientID', 'N/A')
        study_date = getattr(sample, 'StudyDate', 'N/A')
        study_description = getattr(sample, 'StudyDescription', 'N/A')
        modality = getattr(sample, 'Modality', 'N/A')
        series_description = getattr(sample, 'SeriesDescription', 'N/A')
        series_number = getattr(sample, 'SeriesNumber', 'N/A')

        # --- Transfer Syntax ---
        ts_info = get_transfer_syntax_info(sample)

        # --- Pixel Spacing ---
        pixel_spacing = getattr(sample, 'PixelSpacing', None)
        slice_thickness = getattr(sample, 'SliceThickness', None)
        if pixel_spacing:
            spacing_str = f"Row: {pixel_spacing[0]} mm, Col: {pixel_spacing[1]} mm"
            if slice_thickness:
                spacing_str += f" (Grubość plastra: {slice_thickness} mm)"
        else:
            spacing_str = "Brak (PixelSpacing nieobecne)"

        # --- Rozmiar Rastrowy (Rozdzielczość) ---
        rows = getattr(sample, 'Rows', 'N/A')
        cols = getattr(sample, 'Columns', 'N/A')
        num_frames = len(datasets)
        raster_size_str = f"{cols} x {rows} px (Liczba plików/plastrów: {num_frames})"

        # --- Rozmiar Fizyczny & Bounding Box Image Position Patient (IPP) ---
        ipp_list = []
        for ds in datasets:
            ipp = getattr(ds, 'ImagePositionPatient', None)
            if ipp is not None and len(ipp) == 3:
                ipp_list.append([float(x) for x in ipp])

        bbox = calculate_bbox(ipp_list)

        # Obliczanie fizycznych wymiarów pojedynczej macierzy (2D)
        if pixel_spacing and rows != 'N/A' and cols != 'N/A':
            phys_width = float(cols) * float(pixel_spacing[1])
            phys_height = float(rows) * float(pixel_spacing[0])
            phys_size_2d_str = f"{phys_width:.2f} mm x {phys_height:.2f} mm (pojedynczy plaster)"
        else:
            phys_size_2d_str = "Nie można obliczyć"

        # Wydruk sekcji dla serii
        print(f"\n[SERIA {idx}/{len(series_data)}] UID: {series_uid}")
        print(f"  ├── Modality / Opis Serii  : {modality} | Seria #{series_number}: {series_description}")
        print(f"  ├── Tagi Badania (Study)  : ID Pacjenta: {patient_id} | Data: {study_date} | Opis: {study_description}")
        print(f"  ├── Transfer Syntax       : {ts_info}")
        print(f"  ├── Pixel Spacing         : {spacing_str}")
        print(f"  ├── Rozmiar Rastrowy      : {raster_size_str}")
        print(f"  ├── Rozmiar Fizyczny (2D) : {phys_size_2d_str}")

        if bbox:
            print(f"  └── Bounding Box (IPP)    :")
            print(f"      ├── Min (X, Y, Z)     : ({bbox['min'][0]:.2f}, {bbox['min'][1]:.2f}, {bbox['min'][2]:.2f}) mm")
            print(f"      ├── Max (X, Y, Z)     : ({bbox['max'][0]:.2f}, {bbox['max'][1]:.2f}, {bbox['max'][2]:.2f}) mm")
            print(f"      └── Zakres (dx,dy,dz) : ({bbox['extent'][0]:.2f}, {bbox['extent'][1]:.2f}, {bbox['extent'][2]:.2f}) mm")
        else:
            print(f"  └── Bounding Box (IPP)    : Brak tagów ImagePositionPatient w serii")

    print("\n" + "=" * 80)


def main():
    args = parse_args()
    files = collect_dicom_files(args.paths)
    
    if not files:
        print("Nie znaleziono żadnych plików do przetworzenia.")
        sys.exit(1)

    print(f"Skanowanie {len(files)} plików...")
    series_data, skipped_files = analyze_dicoms(files)
    
    if not series_data:
        print("Nie udało się odczytać prawidłowych plików DICOM.")
        sys.exit(1)

    print_report(series_data, skipped_files)


if __name__ == "__main__":
    main()
