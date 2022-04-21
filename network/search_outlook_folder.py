# Inspried by:
# https://www.excelcise.org/python-outlook-iterate-through-email-in-outlook-folder-pywin32/

import argparse
import os
import sys

import win32com.client

# Defaults
ITER_FOLDER = "Inbox"
SUBJ_SEARCH_STRING = "Certificate Expiring"


def get_email():
    email = os.path.expanduser("~/.email")
    if os.path.exists(email):
        return open(email).read()
    address = input("Enter your e-mail address: ")
    with open(email, "w") as ef:
        ef.write(address)
    return address


def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default=ITER_FOLDER)
    parser.add_argument("--output", "-o", help="output file")
    parser.add_argument("search", nargs="?", default=SUBJ_SEARCH_STRING)
    return parser.parse_args()


def main():
    args = parse_cli()
    account = get_email()

    out_app = win32com.client.gencache.EnsureDispatch("Outlook.Application")
    out_namespace = out_app.GetNamespace("MAPI")

    out_iter_folder = out_namespace.Folders[account].Folders[args.folder]
    item_count = out_iter_folder.Items.Count

    if item_count == 0:
        print(f"No items found in: {args.folder}")
        return

    if args.output:
        outf = open(args.output, "w")
    else:
        outf = sys.stdout

    for i in range(item_count, 0, -1):
        message = out_iter_folder.Items[i]
        if "_MailItem" in str(type(message)):
            if args.search in message.Subject:
                print(message.Subject, file=outf)

    if args.output:
        outf.close()

if __name__ == "__main__":
    main()
