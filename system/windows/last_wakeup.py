import argparse
import json
import subprocess

ps = r"""
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;
Get-WinEvent -FilterHashtable @{
LogName='System';
ProviderName='Microsoft-Windows-Power-Troubleshooter','Microsoft-Windows-Kernel-Power';
Id=1,506,507
} -MaxEvents {n} | Select-Object @{
Name='TimeCreated';
Expression={$_.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss')}
},Id,Message | ConvertTo-Json -Depth 3
"""


def _format_event(event):
    message = " ".join(event["Message"].split())
    print(f"ID: {event['Id']}, {event['TimeCreated']}, {message}")


def powershell_fallback(n: int = 1):
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps.replace("{n}", str(n))],
        capture_output=True,
        text=False,
        check=True,
    )
    data = json.loads(result.stdout)
    if isinstance(data, list):
        for event in data:
            _format_event(event)
    else:
        _format_event(data)


def get_last_wakeup(n: int = 1):
    try:
        import win32evtlog
    except ImportError:
        print("Missing win32evtlog, please install pywin32 package")
        powershell_fallback(n)
        return
    server = "localhost"
    logtype = "System"
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    found = 0

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break
        for event in events:
            if (
                event.EventID == 1
                and event.SourceName == "Microsoft-Windows-Power-Troubleshooter"
            ):
                print(f"Deep Sleep Wakeup: {event.TimeGenerated.Format()}")  # type: ignore
                found += 1
            elif (
                event.EventID == 507
                and event.SourceName == "Microsoft-Windows-Kernel-Power"
            ):
                print(f"Wakeup Time: {event.TimeGenerated.Format()}")  # type: ignore
                found += 1
            elif (
                event.EventID == 506
                and event.SourceName == "Microsoft-Windows-Kernel-Power"
            ):
                print(f"Sleep Time: {event.TimeGenerated.Format()}")  # type: ignore
                found += 1

            if found == n:
                return
    print("No wakeup event found.")


def main():
    parser = argparse.ArgumentParser(
        description="Get last system wake-up time on Windows."
    )
    parser.add_argument(
        "--powershell",
        "-ps",
        action="store_true",
        help="Use PowerShell fallback method",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of wake-up events to retrieve",
    )
    args = parser.parse_args()
    if args.powershell:
        powershell_fallback(args.count)
    else:
        get_last_wakeup(args.count)


if __name__ == "__main__":
    main()
