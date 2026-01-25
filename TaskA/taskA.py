from datetime import datetime

def euro(amount: float) -> str:
    # 2 decimals + Finnish comma + euro sign
    return f"{amount:.2f}".replace(".", ",") + " €"

def main():
    with open("reservations.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()

    parts = line.split("|")

    reservation_number = int(parts[0])
    booker_name = parts[1]

    reservation_date = datetime.strptime(parts[2], "%Y-%m-%d").date()
    start_time = datetime.strptime(parts[3], "%H:%M").time()

    number_of_hours = int(parts[4])
    hourly_price = float(parts[5])

    paid = parts[6] == "True"   # bool
    resource = parts[7]
    phone_number = parts[8]
    email = parts[9]

    total_price = number_of_hours * hourly_price

    print(f"Reservation number: {reservation_number}")
    print(f"Booker: {booker_name}")
    print(f"Date: {reservation_date.strftime('%d.%m.%Y')}")
    print(f"Start time: {start_time.strftime('%H:%M')}")
    print(f"Number of hours: {number_of_hours}")
    print(f"Hourly price: {euro(hourly_price)}")
    print(f"Total price: {euro(total_price)}")
    print(f"Paid: {'Yes' if paid else 'No'}")
    print(f"Location: {resource}")
    print(f"Phone: {phone_number}")
    print(f"Email: {email}")

if __name__ == "__main__":
    main()
