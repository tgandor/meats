#!/usr/bin/env python

import argparse
import datetime

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

parser = argparse.ArgumentParser()
parser.add_argument("rate", type=float)
parser.add_argument("--sum", type=float, default=1000.0)
parser.add_argument(
    "--start", default=today.strftime("%Y-%m-%d"), help="start of saving"
)
parser.add_argument(
    "--end", default=tomorrow.strftime("%Y-%m-%d"), help="end of saving"
)
parser.add_argument(
    "--days", type=int, help="specify days number directly (override --start and --end)"
)
parser.add_argument("--tax", type=float, default=19.0, help="capital gains tax (in %)")
args = parser.parse_args()

print(f"rate={args.rate}")

if args.days:
    days = args.days
else:
    start = datetime.date.fromisoformat(args.start)
    print(f"{start=}")
    end = datetime.date.fromisoformat(args.end)
    print(f"{end=}")
    days = (end - start).days

print(f"{days=}")
principal = args.sum
print(f"{principal=}\n")

interest = args.rate / 100 * principal * days / 365
print(f"{interest=:.2f}")
capitalized_before_tax = principal + interest
print(f"{capitalized_before_tax=:.2f}\n")

tax = interest * args.tax / 100
print(f"{tax=:.2f}")
net_interest = interest - tax
print(f"{net_interest=:.2f}")
capitalized = principal + net_interest
print(f"{capitalized=:.2f}")
net_rate = net_interest / principal * 365 / days * 100
print(f"{net_rate=:.2f}")
