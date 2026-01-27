from pathlib import Path


def main():
    print("Task C started")

    file_path = Path(__file__).with_name("reservations.txt")

    lines = file_path.read_text(encoding="utf-8").splitlines()

    print("Total reservations:", len(lines))

    confirmed = []
    not_confirmed = []

    for line in lines:
        parts = line.split("|")

        if parts[5].lower() == "yes":
            confirmed.append(parts)
        else:
            not_confirmed.append(parts)

    print("\nConfirmed reservations:")
    for r in confirmed:
        print(r)

    print("\nNot confirmed reservations:")
    for r in not_confirmed:
        print(r)


if __name__ == "__main__":
    main()