import csv
import re
from pathlib import Path


input_path = "../../all-data/super-tuesday-raw/2025/CYCLIST COUNTS.csv"

destination = "../../all-data/super-tuesday-normalised/counts-2025.csv"
errors_destination = (
    "../../all-data/super-tuesday-normalised/counts-2025-errors.csv"
)


def parseDescription(description):
    description = description or ""

    total_match = re.search(
        r"\bTotal\s*:?\s*([\d,]+)",
        description,
        flags=re.IGNORECASE,
    )

    # Some descriptions omit "Total" entirely. In those cases, use the
    # first number after the leading image block.
    if total_match is None:
        total_match = re.search(
            r"<img\b[^>]*>\s*(?:<br\s*/?>\s*)*"
            r"(?:Total\s*:?\s*)?([\d,]+)",
            description,
            flags=re.IGNORECASE,
        )

    female_match = re.search(
        r"\bFemales?\s*:\s*([\d,]+)",
        description,
        flags=re.IGNORECASE,
    )

    total_count = (
        int(total_match.group(1).replace(",", ""))
        if total_match is not None
        else None
    )
    female_count = (
        int(female_match.group(1).replace(",", ""))
        if female_match is not None
        else None
    )

    return total_count, female_count


def parse_csv(path, first_output_row):
    parsed_rows = []
    errors = []

    with open(path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {"X", "Y", "description"}
        missing_columns = required_columns - set(reader.fieldnames or [])

        if missing_columns:
            raise ValueError(
                f"{path} is missing columns: {sorted(missing_columns)}"
            )

        for row_number, row in enumerate(reader, start=2):
            total_count, female_count = parseDescription(row["description"])
            output_row = first_output_row + len(parsed_rows)

            for field_name, value in (
                ("total-count", total_count),
                ("female-count", female_count),
            ):
                if value is None:
                    errors.append(
                        {
                            "file": str(path),
                            "input-row": row_number,
                            "output-row": output_row,
                            "cell": field_name,
                            "message": "Missing value",
                        }
                    )

            parsed_rows.append(
                {
                    "y": row["Y"].strip(),
                    "x": row["X"].strip(),
                    "total-count": total_count,
                    "female-count": female_count,
                }
            )

    return parsed_rows, errors


def main():
    all_rows = []
    all_errors = []

    rows, errors = parse_csv(
        input_path,
        first_output_row=len(all_rows) + 2,  # row 1 is the header
    )

    destination_path = Path(destination)
    errors_path = Path(errors_destination)

    destination_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["y", "x", "total-count", "female-count"]

    with destination_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    error_fieldnames = [
        "file",
        "input-row",
        "output-row",
        "cell",
        "message",
    ]

    with errors_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=error_fieldnames)
        writer.writeheader()
        writer.writerows(errors)

    print(f"Wrote {len(rows)} locations to {destination}")
    print(f"Wrote {len(errors)} missing-data errors to {errors_destination}")


if __name__ == "__main__":
    main()