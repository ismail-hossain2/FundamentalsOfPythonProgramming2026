from pathlib import Path
from datetime import datetime


def parse_reservation(line: str) -> dict:
    parts = line.strip().split("|")
    return {
        "reservation_number": int(parts[0]),
        "booker": parts[1],
        "date": datetime.strptime(parts[2], "%Y-%m-%d").date(),     # convert
        "start_time": datetime.strptime(parts[3], "%H:%M").time(),  # convert
        "hours": int(parts[4]),
        "hourly_rate": float(parts[5].replace(",", ".")),           # safe if comma exists
        "paid": parts[6].strip().lower() in ("yes", "true", "1"),
        "venue": parts[7],
        "phone": parts[8],
        "email": parts[9],
    }


def fmt_date(d) -> str:
    return d.strftime("%d.%m.%Y")


def fmt_time(t) -> str:
    return t.strftime("%H.%M")


def fmt_money(x: float) -> str:
    return f"{x:.2f}".replace(".", ",") + " €"


def print_reservation_number(r: dict) -> None:
    print(f"Reservation number: {r['reservation_number']}")


def print_booker(r: dict) -> None:
    print(f"Booker: {r['booker']}")


def print_date(r: dict) -> None:
    print(f"Date: {fmt_date(r['date'])}")


def print_start_time(r: dict) -> None:
    print(f"Start time: {fmt_time(r['start_time'])}")


def print_hours(r: dict) -> None:
    print(f"Number of hours: {r['hours']}")


def print_hourly_rate(r: dict) -> None:
    print(f"Hourly rate: {fmt_money(r['hourly_rate'])}")


def print_total_price(r: dict) -> None:
    total = r["hours"] * r["hourly_rate"]
    print(f"Total price: {fmt_money(total)}")


def print_paid(r: dict) -> None:
    print(f"Paid: {'Yes' if r['paid'] else 'No'}")


def print_venue(r: dict) -> None:
    print(f"Venue: {r['venue']}")


def print_phone(r: dict) -> None:
    print(f"Phone: {r['phone']}")


def print_email(r: dict) -> None:
    print(f"Email: {r['email']}")


def print_reservation(r: dict) -> None:
    print_reservation_number(r)
    print_booker(r)
    print_date(r)
    print_start_time(r)
    print_hours(r)
    print_hourly_rate(r)
    print_total_price(r)
    print_paid(r)
    print_venue(r)
    print_phone(r)
    print_email(r)
    print()  # blank line between reservations


def main() -> None:
    path = Path(__file__).with_name("reservations.txt")
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = parse_reservation(line)
                print_reservation(r)


if __name__ == "__main__":
    main()