# Copyright (c) 2026 Ismail Hossain
# License: MIT

from __future__ import annotations

from datetime import datetime, date
from typing import Dict, List, Tuple


FIN_WEEKDAYS: list[str] = [
    "maanantai",
    "tiistai",
    "keskiviikko",
    "torstai",
    "perjantai",
    "lauantai",
    "sunnuntai",
]


def parse_int(value: str) -> int:
    """Convert numeric string to int safely."""
    return int(value.strip())


def wh_to_kwh(value_wh: float) -> float:
    """Convert watt-hours (Wh) to kilowatt-hours (kWh)."""
    return value_wh / 1000.0


def read_week_data(filename: str) -> Dict[date, Tuple[float, float]]:
    """
    Read one week's CSV file and return per-day totals.

    Returns:
        dict mapping date -> (consumption_kwh_total, production_kwh_total)
    """
    daily: Dict[date, List[float]] = {}

    with open(filename, "r", encoding="utf-8") as f:
        next(f, None)  # skip header

        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(";")
            if len(parts) != 7:
                continue  # invalid line, skip

            ts = datetime.fromisoformat(parts[0].strip())
            day = ts.date()

            c1 = parse_int(parts[1])
            c2 = parse_int(parts[2])
            c3 = parse_int(parts[3])
            p1 = parse_int(parts[4])
            p2 = parse_int(parts[5])
            p3 = parse_int(parts[6])

            # sum all three phases
            consumption_kwh = wh_to_kwh(c1 + c2 + c3)
            production_kwh = wh_to_kwh(p1 + p2 + p3)

            if day not in daily:
                daily[day] = [0.0, 0.0]

            daily[day][0] += consumption_kwh
            daily[day][1] += production_kwh

    # convert inner lists to tuples
    return {d: (vals[0], vals[1]) for d, vals in daily.items()}


def format_kwh(value: float) -> str:
    """Format kWh value using Finnish decimal comma and two decimals."""
    return f"{value:.2f}".replace(".", ",")


def format_date(d: date) -> str:
    """Format date as dd.mm.yyyy."""
    return d.strftime("%d.%m.%Y")


def write_week_report(
    file,
    week_number: int,
    daily: Dict[date, Tuple[float, float]],
) -> Tuple[float, float]:
    """
    Write one week's daily data to an open file.

    Returns:
        (total_consumption_kwh, total_production_kwh) for the week.
    """
    file.write(f"Week {week_number} electricity consumption and production (kWh)\n")
    file.write("päivä        pvm         kulutus (kWh)  tuotanto (kWh)\n")

    week_cons = 0.0
    week_prod = 0.0

    for d in sorted(daily.keys()):
        weekday_name = FIN_WEEKDAYS[d.weekday()]
        cons, prod = daily[d]

        week_cons += cons
        week_prod += prod

        file.write(
            f"{weekday_name:<11} {format_date(d):<10}  "
            f"{format_kwh(cons):>8}        {format_kwh(prod):>8}\n"
        )

    file.write(
        f"{'Yhteensä':<21}  "
        f"{format_kwh(week_cons):>8}        {format_kwh(week_prod):>8}\n"
    )
    file.write("\n")

    return week_cons, week_prod


def main() -> None:
    """Main entry point: process three weeks and write summary.txt."""
    week_files = [
        (41, "week41.csv"),
        (42, "week42.csv"),
        (43, "week43.csv"),
    ]

    total_cons_all = 0.0
    total_prod_all = 0.0

    with open("summary.txt", "w", encoding="utf-8") as out:
        for week_no, filename in week_files:
            daily = read_week_data(filename)
            week_cons, week_prod = write_week_report(out, week_no, daily)
            total_cons_all += week_cons
            total_prod_all += week_prod

        out.write("All three weeks total (kWh)\n")
        out.write(f"{'Total consumption:':<22} {format_kwh(total_cons_all)}\n")
        out.write(f"{'Total production:':<22} {format_kwh(total_prod_all)}\n")


if __name__ == "__main__":
    main()
