#!/usr/bin/env python3
"""
JSON to CSV Converter

Converts JSON files with nested structures into flattened CSV format.
- Nested objects use dot notation (e.g., user.address.city)
- Arrays are joined with semicolons (e.g., "reading;hiking;gaming")
"""

import json
import csv
import argparse
import sys
from pathlib import Path
from typing import Any


def flatten_json(obj: Any, parent_key: str = "", separator: str = ".") -> dict:
    """
    Flatten a nested JSON object into a single-level dictionary.

    Args:
        obj: The JSON object to flatten
        parent_key: The base key for nested items
        separator: The separator to use between nested keys

    Returns:
        A flattened dictionary with dot-notation keys
    """
    items = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            items.update(flatten_json(value, new_key, separator))
    elif isinstance(obj, list):
        # Join array elements with semicolons for CSV compatibility
        if all(isinstance(item, (str, int, float, bool, type(None))) for item in obj):
            items[parent_key] = ";".join(str(item) for item in obj)
        else:
            # For arrays of objects, flatten each with index
            for i, item in enumerate(obj):
                new_key = f"{parent_key}[{i}]"
                items.update(flatten_json(item, new_key, separator))
    else:
        items[parent_key] = obj

    return items


def json_to_csv(json_data: Any) -> tuple[list[str], list[list[Any]]]:
    """
    Convert JSON data to CSV format.

    Args:
        json_data: The JSON data (can be a single object or list of objects)

    Returns:
        A tuple of (headers, rows) for CSV output
    """
    # Handle both single objects and arrays of objects
    if isinstance(json_data, list):
        records = json_data
    else:
        records = [json_data]

    # Flatten all records
    flattened_records = [flatten_json(record) for record in records]

    # Collect all unique headers
    all_headers = set()
    for record in flattened_records:
        all_headers.update(record.keys())

    # Sort headers for consistent output
    headers = sorted(all_headers)

    # Build rows
    rows = []
    for record in flattened_records:
        row = [record.get(header, "") for header in headers]
        rows.append(row)

    return headers, rows


def convert_file(input_path: str, output_path: str | None = None) -> str:
    """
    Convert a JSON file to CSV.

    Args:
        input_path: Path to the input JSON file
        output_path: Path for the output CSV file (optional)

    Returns:
        The path to the output CSV file
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Default output path
    if output_path is None:
        output_path = str(input_file.with_suffix(".csv"))

    # Read JSON
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Convert to CSV format
    headers, rows = json_to_csv(json_data)

    # Write CSV
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return output_path


def convert_string(json_string: str) -> str:
    """
    Convert a JSON string to CSV string.

    Args:
        json_string: The JSON data as a string

    Returns:
        The CSV data as a string
    """
    json_data = json.loads(json_string)
    headers, rows = json_to_csv(json_data)

    # Build CSV string
    output = []
    output.append(",".join(headers))
    for row in rows:
        # Properly escape values for CSV
        escaped_row = []
        for value in row:
            if value is None:
                escaped_row.append("")
            elif isinstance(value, bool):
                escaped_row.append(str(value).lower())
            elif isinstance(value, str) and ("," in value or '"' in value or "\n" in value):
                escaped_row.append(f'"{value.replace(chr(34), chr(34)+chr(34))}"')
            else:
                escaped_row.append(str(value))
        output.append(",".join(escaped_row))

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON files to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.json                    # Creates input.csv
  %(prog)s input.json -o output.csv      # Specify output file
  %(prog)s input.json --stdout           # Print to stdout
        """
    )
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument("-o", "--output", help="Output CSV file path")
    parser.add_argument("--stdout", action="store_true", help="Print CSV to stdout instead of file")

    args = parser.parse_args()

    try:
        if args.stdout:
            with open(args.input, "r", encoding="utf-8") as f:
                json_string = f.read()
            print(convert_string(json_string))
        else:
            output_path = convert_file(args.input, args.output)
            print(f"Converted: {args.input} -> {output_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
