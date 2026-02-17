# Copyright (c) 2026 Ismail Hossain
# License: MIT

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Measurement:
    """One hourly measurement row."""
    ts: datetime
    consumption_kwh: float
    production_kwh: float
    temperature_c: float


def parse_float(value: str) -> float:
    """Parse float safely (supports comma or dot)."""
    v = value.strip().replace(",", ".")
    return float(v)


def finnish_decimal(value: float) -> str:
    """Format a number with 2 decimals and decimal comma."""
    return f"{value:.2f}".replace(".", ",")


def format_date_fi(d: date) -> str:
    """Format date as dd.mm.yyyy."""
    return d.strftime("%d.%m.%Y")


def parse_date_fi(s: str) -> date:
    """Parse date from dd.mm.yyyy format into date object."""
    s = s.strip()
    dt = datetime.strptime(s, "%d.%m.%Y")
    return dt.date()


def read_data(filename: str) -> List[Measurement]:
    """
    Reads CSV file and returns hourly measurements.

    Expected columns:
    - timestamp (ISO like 2025-10-13T00:00:00)
    - consumption (net) kWh
    - production (net) kWh
    - temperature (daily avg or hourly, depending on file)
    """
    rows: List[Measurement] = []

    with open(filename, "r", encoding="utf-8") as f:
        header = f.readline()
        if not header:
            return rows

        # Detect separator: ; or ,
        sep = ";" if ";" in header else ","

        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(sep)

            # We expect at least 4 columns
            if len(parts) < 4:
                continue

            ts = datetime.fromisoformat(parts[0].strip())
            consumption = parse_float(parts[1])
            production = parse_float(parts[2])
            temperature = parse_float(parts[3])

            rows.append(
                Measurement(
                    ts=ts,
                    consumption_kwh=consumption,
                    production_kwh=production,
                    temperature_c=temperature,
                )
            )

    return rows


def build_daily_index(data: List[Measurement]) -> Dict[date, List[Measurement]]:
    """Group measurements by day."""
    daily: Dict[date, List[Measurement]] = {}
    for m in data:
        d = m.ts.date()
        daily.setdefault(d, []).append(m)
    return daily


def show_main_menu() -> str:
    """Print main menu and return user selection."""
    print("\nChoose a report type:")
    print("1) Daily summary for a date range")
    print("2) Monthly summary for one month")
    print("3) Full year 2025 summary")
    print("4) Exit the program")
    return input("Select (1-4): ").strip()


def show_next_menu() -> str:
    """Print post-report menu and return user selection."""
    print("\nWhat would you like to do next?")
    print("1) Write the report to the file report.txt")
    print("2) Create a new report")
    print("3) Exit")
    return input("Select (1-3): ").strip()


def compute_range_summary(
    daily: Dict[date, List[Measurement]],
    start: date,
    end: date,
) -> Tuple[float, float, float]:
    """
    Compute totals for [start..end] inclusive.

    Returns:
        total_consumption_kwh, total_production_kwh, avg_temperature_c
    """
    total_cons = 0.0
    total_prod = 0.0
    temp_sum = 0.0
    temp_count = 0

    for d, rows in daily.items():
        if start <= d <= end:
            for m in rows:
                total_cons += m.consumption_kwh
                total_prod += m.production_kwh
                temp_sum += m.temperature_c
                temp_count += 1

    avg_temp = (temp_sum / temp_count) if temp_count > 0 else 0.0
    return total_cons, total_prod, avg_temp


def create_daily_report(data: List[Measurement]) -> List[str]:
    """Build a daily summary report for a selected date range."""
    daily = build_daily_index(data)

    start_str = input("Enter start date (dd.mm.yyyy): ")
    end_str = input("Enter end date (dd.mm.yyyy): ")

    start = parse_date_fi(start_str)
    end = parse_date_fi(end_str)

    if end < start:
        start, end = end, start

    total_cons, total_prod, avg_temp = compute_range_summary(daily, start, end)

    lines: List[str] = []
    lines.append("-" * 53)
    lines.append(f"Report for the period {format_date_fi(start)}–{format_date_fi(end)}")
    lines.append(f"- Total consumption: {finnish_decimal(total_cons)} kWh")
    lines.append(f"- Total production: {finnish_decimal(total_prod)} kWh")
    lines.append(f"- Average temperature: {finnish_decimal(avg_temp)} °C")
    return lines


def month_name(month: int) -> str:
    """Return English month name (as in example)."""
    names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return names[month - 1]


def create_monthly_report(data: List[Measurement]) -> List[str]:
    """Build a monthly summary report for a selected month number."""
    daily = build_daily_index(data)

    month_str = input("Enter month number (1–12): ").strip()
    month = int(month_str)

    total_cons = 0.0
    total_prod = 0.0

    # For “average daily temperature for the month”
    # We compute average temperature per day (avg of all hourly temp values in that day),
    # then average those daily averages across the month.
    daily_avgs: List[float] = []

    for d in sorted(daily.keys()):
        if d.year == 2025 and d.month == month:
            rows = daily[d]
            total_cons += sum(m.consumption_kwh for m in rows)
            total_prod += sum(m.production_kwh for m in rows)

            if rows:
                day_avg = sum(m.temperature_c for m in rows) / len(rows)
                daily_avgs.append(day_avg)

    avg_temp = (sum(daily_avgs) / len(daily_avgs)) if daily_avgs else 0.0

    lines: List[str] = []
    lines.append("-" * 53)
    lines.append(f"Report for the month: {month_name(month)}")
    lines.append(f"- Total consumption: {finnish_decimal(total_cons)} kWh")
    lines.append(f"- Total production: {finnish_decimal(total_prod)} kWh")
    lines.append(f"- Average temperature: {finnish_decimal(avg_temp)} °C")
    return lines


def create_yearly_report(data: List[Measurement]) -> List[str]:
    """Build a full-year 2025 summary report."""
    # All values are for 2025.csv, but we still filter by year to follow the rules
    year_rows = [m for m in data if m.ts.year == 2025]

    total_cons = sum(m.consumption_kwh for m in year_rows)
    total_prod = sum(m.production_kwh for m in year_rows)

    temp_sum = sum(m.temperature_c for m in year_rows)
    temp_count = len(year_rows)
    avg_temp = (temp_sum / temp_count) if temp_count > 0 else 0.0

    lines: List[str] = []
    lines.append("Report for the year: 2025")
    lines.append(f"- Total consumption: {finnish_decimal(total_cons)} kWh")
    lines.append(f"- Total production: {finnish_decimal(total_prod)} kWh")
    lines.append(f"- Average temperature: {finnish_decimal(avg_temp)} °C")
    return lines


def print_report_to_console(lines: List[str]) -> None:
    """Print report lines to the console."""
    print()
    for line in lines:
        print(line)


def write_report_to_file(lines: List[str]) -> None:
    """Write report lines to report.txt (overwrite)."""
    with open("report.txt", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def main() -> None:
    """Main function: reads data, shows menus, and controls report generation."""
    data = read_data("2025.csv")
    last_report: List[str] = []

    while True:
        choice = show_main_menu()

        try:
            if choice == "1":
                last_report = create_daily_report(data)
                print_report_to_console(last_report)

            elif choice == "2":
                last_report = create_monthly_report(data)
                print_report_to_console(last_report)

            elif choice == "3":
                last_report = create_yearly_report(data)
                print_report_to_console(last_report)

            elif choice == "4":
                break

            else:
                print("Invalid selection. Please choose 1–4.")
                continue

        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
            continue

        # post-report menu loop
        while True:
            next_choice = show_next_menu()

            if next_choice == "1":
                write_report_to_file(last_report)
                print("Report written to report.txt (overwritten).")
            elif next_choice == "2":
                break
            elif next_choice == "3":
                return
            else:
                print("Invalid selection. Please choose 1–3.")


if __name__ == "__main__":
    main()
