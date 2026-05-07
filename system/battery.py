#!/usr/bin/env python

import argparse
import glob
import datetime

fields_of_interest = [
    "POWER_SUPPLY_ENERGY_FULL",
    "POWER_SUPPLY_ENERGY_NOW",
    "POWER_SUPPLY_POWER_NOW",
    "POWER_SUPPLY_CAPACITY",
    "POWER_SUPPLY_LOST_CAPACITY",
]


alternatives = {
    "POWER_SUPPLY_POWER_NOW": lambda data: data.get("POWER_SUPPLY_VOLTAGE_NOW", 0)
    * data.get("POWER_SUPPLY_CURRENT_NOW", 0)
    / 1e12,
    "POWER_SUPPLY_ENERGY_FULL": lambda data: data.get(
        "POWER_SUPPLY_VOLTAGE_MIN_DESIGN", 0
    )
    * data.get("POWER_SUPPLY_CHARGE_FULL", 0)
    / 1e12,
    "POWER_SUPPLY_ENERGY_FULL_DESIGN": lambda data: data.get(
        "POWER_SUPPLY_VOLTAGE_MIN_DESIGN", 0
    )
    * data.get("POWER_SUPPLY_CHARGE_FULL_DESIGN", 0)
    / 1e12,
    "POWER_SUPPLY_ENERGY_NOW": lambda data: data.get("POWER_SUPPLY_VOLTAGE_NOW", 0)
    * data.get("POWER_SUPPLY_CHARGE_NOW", 0)
    / 1e12,
    "POWER_SUPPLY_LOST_CAPACITY": lambda data: (
        data.get("POWER_SUPPLY_ENERGY_FULL", data.get("POWER_SUPPLY_CHARGE_FULL", 0))
        / data.get(
            "POWER_SUPPLY_ENERGY_FULL_DESIGN",
            data.get("POWER_SUPPLY_CHARGE_FULL_DESIGN", 1),
        )
        - 1
    )
    * 100,
}


class BattDict(dict):
    def __setitem__(self, key, val):
        try:
            val = int(val)
        except:
            pass
        super(BattDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        if key not in self and key in alternatives:
            return alternatives[key](self)
        return super(BattDict, self).__getitem__(key)


def unit(field):
    if "_VOLTAGE_" in field:
        return " V"
    elif "_POWER_" in field:
        return " W"
    elif "_ENERGY_" in field:
        return " Wh"
    elif "_CAPACITY" in field:
        return " %"
    return ""


def power_supply_data():
    batteries = glob.glob("/sys/class/power_supply/BAT?/uevent")
    if not batteries:
        print("Batteries not found.")
        exit(1)
    raw = open(batteries[0]).read()
    result = BattDict()
    for line in raw.split("\n"):
        parts = line.split("=")
        if len(parts) == 2:
            result[parts[0]] = parts[1]
    return result


def format(data, field):
    # TODO: specific precisions per field?
    if type(data[field]) is int:
        return str(data[field])

    return "{:.3f}".format(data[field])


def format_fields_of_interest(data):
    return "  ".join(
        format(data, field) + unit(field) if field is not None else ""
        for field in fields_of_interest
    )


def format_json(data):
    import json

    return json.dumps({field: data[field] for field in fields_of_interest})


def friendly_report(data):
    if data.get("POWER_SUPPLY_STATUS", "N/A") == "Charging":
        eta = (
            data["POWER_SUPPLY_ENERGY_FULL"] - data["POWER_SUPPLY_ENERGY_NOW"]
        ) / data["POWER_SUPPLY_POWER_NOW"] * 3600
        arrival = (datetime.datetime.now() + datetime.timedelta(seconds=eta)).strftime(
            "%H:%M:%S"
        )
        eta_str = str(datetime.timedelta(seconds=eta))[:-7]
        eta_percent = 100 * (
            1 - data["POWER_SUPPLY_ENERGY_NOW"] / data["POWER_SUPPLY_ENERGY_FULL"]
        )
        eta_percent_str = "{:.1f}%".format(eta_percent)
        eta_report = f"{arrival} ({eta_str}, {eta_percent_str} to go)"
    elif data.get("POWER_SUPPLY_STATUS", "N/A") == "Discharging":
        critical = 0.05
        if (
            data["POWER_SUPPLY_ENERGY_NOW"] / data["POWER_SUPPLY_ENERGY_FULL"]
            < critical
        ):
            eta_report = "CRITICAL: {:.1f}% remaining".format(
                100 * data["POWER_SUPPLY_ENERGY_NOW"] / data["POWER_SUPPLY_ENERGY_FULL"]
            )
        else:
            eta = (
                data["POWER_SUPPLY_ENERGY_NOW"]
                - critical * data["POWER_SUPPLY_ENERGY_FULL"]
            ) / data["POWER_SUPPLY_POWER_NOW"] * 3600
            arrival = (datetime.datetime.now() + datetime.timedelta(seconds=eta)).strftime(
                "%H:%M:%S"
            )
            eta_str = str(datetime.timedelta(seconds=eta))[:-7]
            eta_percent = (
                100 * data["POWER_SUPPLY_ENERGY_NOW"] / data["POWER_SUPPLY_ENERGY_FULL"]
            )
            eta_percent_str = "{:.1f}%".format(eta_percent)
            eta_report = f"{arrival} ({eta_str}, {eta_percent_str} to go)"
    else:
        eta_report = "N/A"
    return (
        "Battery: {}% ({} at {:<.3f} W), energy: {:<.3f} Wh (of {:<.3f} Wh)\n"
        "ETA: {}\n"
        "lost: {:<.3f}% capacity\n"
    ).format(
        data.get("POWER_SUPPLY_CAPACITY", "N/A"),
        data.get("POWER_SUPPLY_STATUS", "N/A"),
        data["POWER_SUPPLY_POWER_NOW"],
        data["POWER_SUPPLY_ENERGY_NOW"],
        data["POWER_SUPPLY_ENERGY_FULL"],
        eta_report,
        data["POWER_SUPPLY_LOST_CAPACITY"],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument(
        "--short", action="store_true", help="Output in legacy short format"
    )
    args = parser.parse_args()

    data = power_supply_data()
    if args.json:
        print(format_json(data))
    elif args.short:
        print(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            format_fields_of_interest(data),
        )
    else:
        print(friendly_report(data))


if __name__ == "__main__":
    main()

# one example (using charge not watthours):
"""
POWER_SUPPLY_NAME=BAT0
POWER_SUPPLY_STATUS=Discharging
POWER_SUPPLY_PRESENT=1
POWER_SUPPLY_TECHNOLOGY=Li-ion
POWER_SUPPLY_CYCLE_COUNT=0
POWER_SUPPLY_VOLTAGE_MIN_DESIGN=14800000
POWER_SUPPLY_VOLTAGE_NOW=14410000
POWER_SUPPLY_CURRENT_NOW=2758000
POWER_SUPPLY_CHARGE_FULL_DESIGN=4068000
POWER_SUPPLY_CHARGE_FULL=3804000
POWER_SUPPLY_CHARGE_NOW=1482000
POWER_SUPPLY_CAPACITY=38
POWER_SUPPLY_CAPACITY_LEVEL=Normal
POWER_SUPPLY_MODEL_NAME=BAT
POWER_SUPPLY_MANUFACTURER=Notebook
POWER_SUPPLY_SERIAL_NUMBER=0001
"""
