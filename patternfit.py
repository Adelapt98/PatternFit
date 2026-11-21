"""Compare a pair of straight stitch lines in a local JSON fixture."""

import argparse
import json
import math
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, help="Path to the JSON fixture")
    args = parser.parse_args()

    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        first, second = fixture["seams"]
        tolerance = float(fixture["tolerance_mm"])
        lengths = []
        for seam in (first, second):
            start_x, start_y = seam["start"]
            end_x, end_y = seam["end"]
            length = math.dist((start_x, start_y), (end_x, end_y))
            if not math.isfinite(length) or length <= 0:
                raise ValueError("seam length must be positive and finite")
            lengths.append(length)
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        names = (first["name"], second["name"])
    except (OSError, KeyError, TypeError, ValueError, OverflowError) as error:
        parser.error(f"invalid fixture: {error}")

    difference = abs(lengths[0] - lengths[1])
    for name, length in zip(names, lengths):
        print(f"{name}: {length:.2f} mm")
    print(f"Difference: {difference:.2f} mm (tolerance: {tolerance:.2f} mm)")
    within_tolerance = difference <= tolerance
    print("Within tolerance" if within_tolerance else "Outside tolerance")
    return 0 if within_tolerance else 1


if __name__ == "__main__":
    raise SystemExit(main())
