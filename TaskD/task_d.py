from datetime import datetime


def parse_int(value: str) -> int:
    """Convert a numeric string into int safely (supports spaces)."""
    return int(value.strip())


def read_data(filename: str) -> list[tuple[str, float, float]]:
    """
    Reads the CSV file and returns a list of:
    (weekday, consumption_kwh, production_kwh)

    Consumption = phase1 + phase2 + phase3 (Wh) -> kWh
    Production  = phase1 + phase2 + phase3 (Wh) -> kWh
    """
    rows: list[tuple[str, float, float]] = []

    with open(filename, "r", encoding="utf-8") as file:
        next(file, None)  # skip header safely

        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(";")
            if len(parts) != 7:
                continue  # invalid line

            ts = datetime.fromisoformat(parts[0].strip())

            c1 = parse_int(parts[1])
            c2 = parse_int(parts[2])
            c3 = parse_int(parts[3])

            p1 = parse_int(parts[4])
            p2 = parse_int(parts[5])
            p3 = parse_int(parts[6])

            consumption_kwh = (c1 + c2 + c3) / 1000
            production_kwh = (p1 + p2 + p3) / 1000

            weekday = ts.strftime("%A")
            rows.append((weekday, consumption_kwh, production_kwh))

    return rows


def calculate_daily_totals(rows: list[tuple[str, float, float]]) -> dict[str, tuple[float, float]]:
    """
    Calculates totals per weekday.
    Returns: { weekday: (consumption_total_kwh, production_total_kwh) }
    """
    totals: dict[str, list[float]] = {}

    for weekday, cons_kwh, prod_kwh in rows:
        if weekday not in totals:
            totals[weekday] = [0.0, 0.0]
        totals[weekday][0] += cons_kwh
        totals[weekday][1] += prod_kwh

    return {day: (vals[0], vals[1]) for day, vals in totals.items()}


def print_results(totals: dict[str, tuple[float, float]]) -> None:
    """Prints the results as a clear console report with decimal comma."""
    print("Week 42 electricity consumption and production (kWh)\n")

    weekdays_order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    for day in weekdays_order:
        if day not in totals:
            continue

        consumption, production = totals[day]

        cons_str = f"{consumption:.2f}".replace(".", ",")
        prod_str = f"{production:.2f}".replace(".", ",")

        print(f"{day:<10} consumption: {cons_str:>8}  production: {prod_str:>8}")


def main() -> None:
    filename = "week42.csv"
    rows = read_data(filename)
    totals = calculate_daily_totals(rows)
    print_results(totals)


if __name__ == "__main__":
    main()