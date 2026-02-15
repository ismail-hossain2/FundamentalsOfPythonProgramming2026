# Copyright (c) 2026 Ismail Hossain
# License: MIT

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date, time


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


@dataclass
class Reservation:
    reservation_id: int
    name: str
    email: str
    phone: str
    date: date
    time: time
    duration: int
    price: float
    confirmed: bool
    resource: str
    created: datetime

    def is_confirmed(self) -> bool:
        return self.confirmed

    def is_long(self) -> bool:
        return self.duration >= 3

    def total_price(self) -> float:
        return self.duration * self.price


def convert_reservation(parts: list[str]) -> Reservation:
    return Reservation(
        reservation_id=int(parts[0]),
        name=parts[1],
        email=parts[2],
        phone=parts[3],
        date=datetime.strptime(parts[4], "%Y-%m-%d").date(),
        time=datetime.strptime(parts[5], "%H:%M").time(),
        duration=int(parts[6]),
        price=float(parts[7]),
        confirmed=parse_bool(parts[8]),
        resource=parts[9],
        created=datetime.strptime(parts[10], "%Y-%m-%d %H:%M:%S"),
    )


def fetch_reservations(filename: str) -> list[Reservation]:
    reservations: list[Reservation] = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            reservations.append(convert_reservation(parts))
    return reservations


def main() -> None:
    reservations = fetch_reservations("reservations.txt")

    print("Confirmed reservations:")
    for r in reservations:
        if r.is_confirmed():
            print(
                f"- {r.name}, {r.resource}, "
                f"{r.date.strftime('%d.%m.%Y')} at {r.time.strftime('%H.%M')}"
            )

    print("\nLong reservations (duration >= 3h):")
    for r in reservations:
        if r.is_long():
            print(f"- {r.name} ({r.duration}h), total {r.total_price():.2f} €")

    revenue = sum(r.total_price() for r in reservations if r.is_confirmed())
    print(f"\nTotal revenue (confirmed): {revenue:.2f} €")


if __name__ == "__main__":
    main()
