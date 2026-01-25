from __future__ import annotations

from datetime import datetime
from pathlib import Path


def parse_reservation(line: str) -> dict:
    parts = [p.strip() for p in line.strip().split("|")]

    reservation_number = int(parts[0])
    booker = parts[1]
    reservation_date = datetime.strptime(parts[2], "%Y-%m-%d").date()
    start_time = datetime.strptime(parts[3], "%H:%M").time()
    hours = int(parts[4])
    hourly_price = float(parts[5])
    paid = parts[6] == "True"
    resource = parts[7]
    phone = parts[8]
    email = parts[9]

    return {
        "reservation_number": reservation_number,
        "booker": booker,
        "date": reservation_date,
        "start_time": start_time,
        "hours": hours,
        "hourly_price": hourly_price,
        "paid": paid,
        "resource": resource,
        "phone": phone,
        "email": email,
    }


def print_reservation_number(r: dict):
    print(f"Reservation number: {r['reservation_number']}")


def print_booker(r: dict):
    print(f"Booker: {r['booker']}")


def print_date(r: dict):
    print(f"Date: {r['date']}")


def print_start_time(r: dict):
    print(f"Start time: {r['start_time'].strftime('%H:%M')}")


def print_hours(r: dict):
    print(f"Number of hours: {r['hours']}")


def print_hourly_price(r: dict):
    print(f"Hourly price: {r['hourly_price']} €")


def print_total_price(r: dict):
    total = r["hours"] * r["hourly_price"]
    print(f"Total price: {total} €")


def print_paid(r: dict):
    print(f"Paid: {r['paid']}")


def print_location(r: dict):
    print(f"Location: {r['resource']}")


def print_phone(r: dict):
    print(f"Phone: {r['phone']}")


def print_email(r: dict):
    print(f"Email: {r['email']}")


def print_reservation(r: dict):
    print_reservation_number(r)
    print_booker(r)
    print_date(r)
    print_start_time(r)
    print_hours(r)
    print_hourly_price(r)
    print_total_price(r)
    print_paid(r)
    print_location(r)
    print_phone(r)
    print_email(r)


def main():
    path = Path(__file__).with_name("reservations.txt")

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                reservation = parse_reservation(line)
                print_reservation(reservation)
                print()


if __name__ == "__main__":
    main()

