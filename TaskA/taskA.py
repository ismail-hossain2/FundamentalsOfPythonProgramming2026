# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task

from datetime import datetime

"""
Program that reads reservation details from a file
and prints them to the console:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly price: 19,95 €
Total price: 39,90 €
Paid: Yes
Location: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com
"""

#  modified by Mazharul Islam according to instructions

def main():
    # Define the file name directly in the code
    reservations = "reservations.txt"

    # Open the file and read its contents
    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip()

    # Print the reservation to the console
    #print(reservation)

    # Try these
    # print(reservation.split('|'))

    reservationId = int(reservation.split('|')[0])
    print(f"Reservation number: {reservationId}")

    booker = reservation.split('|')[1]
    # print(type(booker))
    print(f"Booker: {booker}")

    day = datetime.strptime(reservation.split('|')[2], "%Y-%m-%d").date()
    finnish_day = day.strftime("%d.%m.%Y")
    print(f"Date: {finnish_day}")

    time = datetime.strptime(reservation.split('|')[3], "%H:%M").time()
    finnish_time = time.strftime("%H:%M")
    print(f"Start time: {finnish_time}")

    number_of_hours = int(reservation.split('|')[4])
    print(f"Number of hours: {number_of_hours}")

    hourly_price = float(reservation.split('|')[5])
    print("Hourly price: {:.2f}".format(hourly_price).replace('.', ',') + " €")

    total_price = number_of_hours * hourly_price
    print("Total price: {:.2f}".format(total_price).replace('.', ',') + " €")

    paid = reservation.split('|')[6] == "True"
    print(f"Paid: {'Yes' if paid else 'No'}")

    resource = reservation.split('|')[7]
    print(f"Location: {resource}")

    phone = reservation.split('|')[8]
    print(f"Phone: {phone}")

    email = reservation.split('|')[9]
    print(f"Email: {email}")


"""
The above should have printed the number 123,
which is by default text.

You can also try changing [0] to [1]
and test what changes.
"""

if __name__ == "__main__":
    main()
