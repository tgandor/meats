#!/usr/bin/env python3

import os
import sys

def compare_size(archivo1, archivo2):
    if not os.path.isfile(archivo1) or not os.path.isfile(archivo2):
        print("Error: Ambos argumentos deben ser archivos válidos.")
        return

    size1 = os.path.getsize(archivo1)
    size2 = os.path.getsize(archivo2)

    if size1 == 0 or size2 == 0:
        print("Error: Uno o ambos archivos tienen un tamaño de 0 bytes.")
        return

    x = (size1 / size2) * 100
    y = (size2 / size1) * 100

    print(f"{archivo1} es {x:.2f}% ({x-100:.2f}% más grande) de {archivo2}")
    print(f"{archivo2} es {y:.2f}% ({y-100:.2f}% más grande) de {archivo1}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        compare_size(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python compare_size.py archivo1 archivo2")
