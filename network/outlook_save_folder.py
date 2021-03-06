import argparse
import json

# This program requires microsoft windows.
import win32com.client

parser = argparse.ArgumentParser()
parser.add_argument("--folder", "-f")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

outlook = win32com.client.Dispatch("outlook.application")
mapi = outlook.GetNamespace("MAPI")

inbox = mapi.GetDefaultFolder(6)

if args.folder:
    inbox = inbox.Folders[args.folder]

data = []

for message in inbox.items:
    data.append(
        {
            "subject": message.subject,
            "sender": str(getattr(message, "sender", "unknown sender")),
            "date": message.senton.strftime("%Y-%m-%d %H:%M:%S"),
            "body": message.body,
        }
    )
    if args.verbose:
        print(f"{len(data)}\t{message.senton}\t{message.subject}")

json_file = f"{args.folder or 'Inbox'}.json"

with open(json_file, "w") as jsf:
    jsf.write(json.dumps(data, indent=2))
