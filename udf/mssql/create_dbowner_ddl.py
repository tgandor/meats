import argparse
import datetime
import random
import string

import pyperclip

parser = argparse.ArgumentParser()
parser.add_argument("login")
parser.add_argument("database")
parser.add_argument("--strength", "-n", type=int, default=32)
args = parser.parse_args()

password = "".join(random.sample(string.ascii_letters + string.digits, args.strength))
secret_file = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{args.login}_secret.txt"
with open(secret_file, "w") as secret:
    secret.write(password)

# parts from: https://dba.stackexchange.com/questions/54389/sql-server-grant-user-dbo-permission-on-database
script = f"""
use master
GO

CREATE LOGIN {args.login} WITH PASSWORD = '{password}'
GO

use {args.database}
GO

CREATE USER [{args.login}] FROM LOGIN [{args.login}];
exec sp_addrolemember 'db_owner', '{args.login}';
GO
"""

pyperclip.copy(script)
print(script)

print(f"\n  (script copied to clipboard, secret saved to {secret_file}")
