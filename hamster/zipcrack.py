import argparse
import glob
import pathlib
import zipfile


def try_extract(zf: zipfile.ZipFile, password: str = None, v: bool = False):
    try:
        if password:
            zf.setpassword(password.encode())
        zf.extractall()
        if v:
            print(f"{zf} OK, password was {password}")
        return True
    except RuntimeError:
        return False


def _get_passwords(args: argparse.Namespace):
    passwords = [None]
    if args.password_file:
        passwords.extend(args.password_file.read_text().strip().split('\n'))
    if args.password:
        passwords.append(args.password)
    return passwords


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--password', '-p')
    parser.add_argument('--password-file', '-i', type=pathlib.Path)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    for filename in (x for g in args.files for x in glob.glob(g)):
        zf = zipfile.ZipFile(filename, 'r')
        for password in _get_passwords(args):
            if try_extract(zf, password, args.verbose):
                break


if __name__ == '__main__':
    main()
