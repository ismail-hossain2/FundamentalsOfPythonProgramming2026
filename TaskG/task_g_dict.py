# Copyright (c) 2026 Ismail Hossain
# License: MIT

from __future__ import annotations
from datetime import datetime
from typing import Any


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def convert_reservation(parts: list[str]) -> dict[str, Any]:
    # parts order comes from reservations.txt  [oai_citation:3‡reservations.txt](sediment://file_00000000fbd07246a462a2a0bba2edf4)
    return {
        "id": int(parts[0]),
        "name": parts[1],
        "email": parts[2],
        "phone": parts[3],
        "date": datetime.strptime(parts[4], "%Y-%m-%d").date(),
        "time": datetime.strptime(parts[5], "%H:%M").time(),
        "duration": int(parts[6]),
        "price": float(parts[7]),
        "confirmed": parse_bool(parts[8]),
        "resource": parts[9],
        "created": datetime.strptime(parts[10], "%Y-%m-%d %H:%M:%S"),
    }


def fetch_reservations(filename: str) -> list[dict[str, Any]]:
    reservations: list[dict[str, Any]] = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            reservations.append(convert_reservation(parts))

    return reservations


def is_long(r: dict[str, Any]) -> bool:
    return r["duration"] >= 3


def total_price(r: dict[str, Any]) -> float:
    return r["duration"] * r["price"]


def main() -> None:
    reservations = fetch_reservations("reservations.txt")

    print("Confirmed reservations:")
    for r in reservations:
        if r["confirmed"]:
            print(
                f"- {r['name']}, {r['resource']}, "
                f"{r['date'].strftime('%d.%m.%Y')} at {r['time'].strftime('%H.%M')}"
            )

    print("\nLong reservations (duration >= 3h):")
    for r in reservations:
        if is_long(r):
            print(f"- {r['name']} ({r['duration']}h), total {total_price(r):.2f} €")

    revenue = sum(total_price(r) for r in reservations if r["confirmed"])
    print(f"\nTotal revenue (confirmed): {revenue:.2f} €")


if __name__ == "__main__":
    main()