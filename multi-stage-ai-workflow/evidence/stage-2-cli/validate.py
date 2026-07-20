#!/usr/bin/env python3
"""
validate.py — generic CSV validator driven by a JSON ruleset.

Generated in Stage 2 (CLI-based AI) from the JSON contract produced in
Stage 1 (chat-based AI). See ../stage1-chat/validation_rules.json for the
rules and ../README.md for the full workflow.

Usage:
    python3 validate.py <rules.json> <data.csv>

Exit codes:
    0 - every row passed validation
    1 - at least one row failed validation, or the input files were invalid
"""

import csv
import json
import re
import sys

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_rules(rules_path):
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_field(value, field):
    """Return a list of error strings for a single field value (empty = ok)."""
    errors = []
    name = field["name"]
    ftype = field["type"]
    required = field.get("required", False)

    value = (value or "").strip()

    if required and value == "":
        return [f"'{name}' is required but empty"]

    if value == "":
        return errors  # optional and absent, nothing else to check

    if ftype == "string":
        pass  # non-empty string already satisfied above

    elif ftype == "integer":
        try:
            n = int(value)
        except ValueError:
            return [f"'{name}' must be an integer, got '{value}'"]
        if "min" in field and n < field["min"]:
            errors.append(f"'{name}' = {n} is below minimum {field['min']}")
        if "max" in field and n > field["max"]:
            errors.append(f"'{name}' = {n} is above maximum {field['max']}")

    elif ftype == "email":
        if not EMAIL_RE.match(value):
            errors.append(f"'{name}' = '{value}' is not a valid email")

    elif ftype == "enum":
        allowed = field.get("values", [])
        if value not in allowed:
            errors.append(f"'{name}' = '{value}' not in allowed values {allowed}")

    else:
        errors.append(f"'{name}' has unknown rule type '{ftype}'")

    return errors


def validate_csv(rules, csv_path):
    fields = rules["fields"]
    total = 0
    valid_count = 0
    results = []

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            total += 1
            row_errors = []
            for field in fields:
                row_errors.extend(validate_field(row.get(field["name"]), field))

            ok = len(row_errors) == 0
            if ok:
                valid_count += 1
            results.append((i, row, ok, row_errors))

    return total, valid_count, results


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <rules.json> <data.csv>", file=sys.stderr)
        sys.exit(1)

    rules_path, csv_path = sys.argv[1], sys.argv[2]

    try:
        rules = load_rules(rules_path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to load rules file '{rules_path}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        total, valid_count, results = validate_csv(rules, csv_path)
    except OSError as e:
        print(f"Failed to read CSV file '{csv_path}': {e}", file=sys.stderr)
        sys.exit(1)

    for i, row, ok, errors in results:
        status = "PASS" if ok else "FAIL"
        print(f"Row {i} [{status}]: {row}")
        for err in errors:
            print(f"    - {err}")

    print(f"\nSummary: {valid_count}/{total} rows valid")

    sys.exit(0 if valid_count == total else 1)


if __name__ == "__main__":
    main()
