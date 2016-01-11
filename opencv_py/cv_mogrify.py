#!/usr/bin/env python

import cv2
import inspect
import sys

# specific operations: begin


def otsu(target):
    image = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
    value, result = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print('Determined threshold value: {0}'.format(value))
    return result


def adaptive_gauss(target):
    image = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
    # last 2 parameters: window size, bias from mean
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 25)


# specific operations: end


def _get_command(command):
    functions = dict(inspect.getmembers(sys.modules[__name__], inspect.isfunction))
    if command not in functions:
        print('Error. Unknown command: {0}'.format(command))
        return None
    return functions[command]


def _main():
    if len(sys.argv) < 2:
        print('Usage: {0} <command> <image_file...>'.format(sys.argv[0]))
        exit()

    command = _get_command(sys.argv[1])
    if not command:
        exit()

    for target in sys.argv[2:]:
        result = command(target)
        cv2.imwrite(target, result)


if __name__ == '__main__':
    _main()
