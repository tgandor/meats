#!/usr/bin/env python
"""
Sensor monitoring tool with ASCII plots and min/max tracking.
Displays CPU, GPU, chipset, and RAM temperatures in a console.
"""

import subprocess
import re
import time
import sys
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Optional


class SensorReader:
    """Read temperature data from lm-sensors."""

    def __init__(self):
        self.use_sensors = self._check_sensors_available()

    def _check_sensors_available(self) -> bool:
        """Check if 'sensors' command is available."""
        try:
            subprocess.run(['sensors', '-v'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def read_temperatures(self) -> Dict[str, float]:
        """Read current temperatures from sensors."""
        temps = {}

        if self.use_sensors:
            temps = self._read_from_sensors()
        else:
            temps = self._read_from_thermal()

        return temps

    def _read_from_sensors(self) -> Dict[str, float]:
        """Parse output from 'sensors' command."""
        temps = {}
        try:
            result = subprocess.run(['sensors'], capture_output=True, text=True, check=True)
            output = result.stdout

            # Parse temperature lines like: "Core 0:        +45.0°C"
            # or "temp1:        +42.0°C"
            current_chip = None
            for line in output.split('\n'):
                # Track which chip/adapter we're reading
                if line and not line.startswith(' ') and ':' not in line:
                    current_chip = line.strip()

                # Look for temperature readings
                match = re.search(r'([\w\s]+):\s*\+?([-\d.]+)°C', line)
                if match:
                    label = match.group(1).strip()
                    temp = float(match.group(2))

                    # Create a unique key with chip name if available
                    if current_chip:
                        key = f"{current_chip}:{label}"
                    else:
                        key = label

                    temps[key] = temp

        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return temps

    def _read_from_thermal(self) -> Dict[str, float]:
        """Read from /sys/class/thermal as fallback."""
        temps = {}
        try:
            import glob

            for thermal_zone in glob.glob('/sys/class/thermal/thermal_zone*/temp'):
                try:
                    with open(thermal_zone, 'r') as f:
                        temp = int(f.read().strip()) / 1000.0

                    # Get the zone name
                    zone_dir = thermal_zone.rsplit('/', 1)[0]
                    try:
                        with open(f"{zone_dir}/type", 'r') as f:
                            zone_name = f.read().strip()
                    except:
                        zone_name = thermal_zone.split('/')[-2]

                    temps[zone_name] = temp
                except:
                    pass

        except Exception:
            pass

        return temps


class ASCIIPlot:
    """Render ASCII line plots for temperature history."""

    def __init__(self, width: int = 60, height: int = 10):
        self.width = width
        self.height = height

    def render(self, data: List[float], min_val: float, max_val: float,
               current: float) -> List[str]:
        """Render an ASCII plot of the data."""
        if not data or len(data) < 2:
            return [' ' * self.width for _ in range(self.height)]

        # Ensure we have a reasonable range
        if max_val - min_val < 1:
            max_val = min_val + 10

        # Create the plot grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Scale data to fit the plot
        data_to_plot = list(data)[-self.width:]  # Take last width points

        for i, temp in enumerate(data_to_plot):
            # Calculate position
            x = i
            # Invert y so higher temps are at top
            normalized = (temp - min_val) / (max_val - min_val)
            y = int((1 - normalized) * (self.height - 1))
            y = max(0, min(self.height - 1, y))

            # Draw point
            if x < self.width:
                grid[y][x] = '●'

        # Convert grid to strings
        lines = [''.join(row) for row in grid]

        return lines


class SensorMonitor:
    """Main monitoring application."""

    def __init__(self, update_interval: float = 2.0, history_size: int = 60):
        self.reader = SensorReader()
        self.update_interval = update_interval
        self.history_size = history_size

        # Temperature history for each sensor
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=history_size))

        # Min/max tracking
        self.min_temps: Dict[str, float] = {}
        self.max_temps: Dict[str, float] = {}

        # Select key sensors to plot
        self.key_sensors: List[str] = []

        # Terminal size
        self.term_width = 80
        self.term_height = 24
        self._update_terminal_size()

    def _update_terminal_size(self):
        """Get current terminal size."""
        try:
            import os
            size = os.get_terminal_size()
            self.term_width = size.columns
            self.term_height = size.lines
        except:
            pass

    def _select_key_sensors(self, all_sensors: Dict[str, float]):
        """Select the most interesting sensors to plot."""
        if not self.key_sensors:
            # Priority keywords for sensor selection
            priorities = [
                ('CPU', ['Core', 'CPU', 'Tccd', 'Tctl']),
                ('GPU', ['GPU', 'edge', 'junction']),
                ('Chipset', ['chipset', 'PCH', 'SB-TSI']),
                ('RAM', ['DIMM', 'RAM', 'Memory']),
            ]

            selected = []
            for category, keywords in priorities:
                for sensor in all_sensors.keys():
                    if any(kw.lower() in sensor.lower() for kw in keywords):
                        if sensor not in selected:
                            selected.append(sensor)
                            break

            # If we found key sensors, use them. Otherwise use first few
            if selected:
                self.key_sensors = selected[:4]
            else:
                self.key_sensors = list(all_sensors.keys())[:4]

    def update(self):
        """Read sensors and update history."""
        temps = self.reader.read_temperatures()

        if not temps:
            return False

        # Select key sensors on first run
        if not self.key_sensors:
            self._select_key_sensors(temps)

        # Update history and min/max
        for sensor, temp in temps.items():
            self.history[sensor].append(temp)

            if sensor not in self.min_temps:
                self.min_temps[sensor] = temp
                self.max_temps[sensor] = temp
            else:
                self.min_temps[sensor] = min(self.min_temps[sensor], temp)
                self.max_temps[sensor] = max(self.max_temps[sensor], temp)

        return True

    def render(self) -> str:
        """Render the full display."""
        self._update_terminal_size()

        lines = []
        lines.append("=" * self.term_width)
        lines.append("  SENSOR MONITOR - Press Ctrl+C to exit".center(self.term_width))
        lines.append("=" * self.term_width)
        lines.append("")

        # Display all current temperatures
        temps = {k: v[-1] if v else 0 for k, v in self.history.items() if v}

        if temps:
            lines.append("Current Temperatures:")
            lines.append("-" * self.term_width)

            for sensor in sorted(temps.keys()):
                temp = temps[sensor]
                min_t = self.min_temps.get(sensor, temp)
                max_t = self.max_temps.get(sensor, temp)

                # Truncate long sensor names
                display_name = sensor[:35] if len(sensor) > 35 else sensor

                line = f"  {display_name:35s}  {temp:5.1f}°C  (min: {min_t:5.1f}°C, max: {max_t:5.1f}°C)"
                lines.append(line)

            lines.append("")

        # Plot key sensors
        if self.key_sensors:
            lines.append("Temperature History:")
            lines.append("-" * self.term_width)
            lines.append("")

            plot_width = min(60, self.term_width - 20)
            plot_height = 8
            plotter = ASCIIPlot(width=plot_width, height=plot_height)

            for sensor in self.key_sensors:
                if sensor in self.history and len(self.history[sensor]) > 1:
                    data = list(self.history[sensor])
                    current = data[-1]
                    min_t = self.min_temps.get(sensor, current)
                    max_t = self.max_temps.get(sensor, current)

                    # Sensor header
                    display_name = sensor[:30] if len(sensor) > 30 else sensor
                    lines.append(f"  {display_name} - Current: {current:.1f}°C")

                    # Plot
                    plot_lines = plotter.render(data, min_t - 2, max_t + 2, current)  # type: ignore

                    # Add axis labels
                    lines.append(f"    {max_t:4.1f}°C ┤ " + plot_lines[0])
                    for plot_line in plot_lines[1:-1]:
                        lines.append(f"           │ " + plot_line)
                    lines.append(f"    {min_t:4.1f}°C ┤ " + plot_lines[-1])
                    lines.append(f"           └" + "─" * plot_width)
                    lines.append("")

        return '\n'.join(lines)

    def clear_screen(self):
        """Clear screen and move cursor to top."""
        # ANSI escape codes: clear screen and move to home
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()

    def run(self):
        """Main loop."""
        try:
            # Hide cursor
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()

            while True:
                if not self.update():
                    print("Error: Could not read sensor data.")
                    print("Make sure 'sensors' command is available (install lm-sensors package)")
                    print("or that /sys/class/thermal is accessible.")
                    break

                self.clear_screen()
                output = self.render()
                print(output)

                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            print("\n\nExiting...")

        finally:
            # Show cursor again
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()


def main():
    """Entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Monitor system temperatures with ASCII plots'
    )
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=2.0,
        help='Update interval in seconds (default: 2.0)'
    )
    parser.add_argument(
        '-s', '--history-size',
        type=int,
        default=60,
        help='Number of data points to keep in history (default: 60)'
    )

    args = parser.parse_args()

    monitor = SensorMonitor(
        update_interval=args.interval,
        history_size=args.history_size
    )
    monitor.run()


if __name__ == '__main__':
    main()
