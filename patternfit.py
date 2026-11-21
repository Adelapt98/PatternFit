"""Compare a pair of stitch lines in a local JSON fixture."""

import argparse
import json
import math
from pathlib import Path


def midpoint(a, b):
    return tuple(x / 2 + y / 2 for x, y in zip(a, b))


def quadratic_length(start, control, end, error, depth=0):
    lower = math.dist(start, end)
    upper = math.dist(start, control) + math.dist(control, end)
    if not math.isfinite(upper):
        raise ValueError("curve length must be finite")
    if upper - lower <= 2 * error:
        return lower + (upper - lower) / 2
    if depth == 18:
        raise ValueError("curve exceeded the subdivision limit")
    left = midpoint(start, control)
    right = midpoint(control, end)
    split = midpoint(left, right)
    return (
        quadratic_length(start, left, split, error / 2, depth + 1)
        + quadratic_length(split, right, end, error / 2, depth + 1)
    )


def point(value):
    x, y = value
    if not (math.isfinite(x) and math.isfinite(y)):
        raise ValueError("coordinates must be finite")
    return x, y


def seam_length(seam):
    if "segments" not in seam:
        length = math.dist(point(seam["start"]), point(seam["end"]))
    else:
        if "end" in seam:
            raise ValueError("use either an end point or a segment list")
        segments = seam["segments"]
        if not isinstance(segments, list) or not segments:
            raise ValueError("segments must be a nonempty list")
        start = point(seam["start"])
        error_per_segment = 0.0001 / len(segments)
        lengths = []
        for segment in segments:
            end = point(segment["end"])
            kind = segment["kind"]
            if kind == "line":
                lengths.append(math.dist(start, end))
            elif kind == "quadratic":
                control = point(segment["control"])
                lengths.append(quadratic_length(start, control, end, error_per_segment))
            else:
                raise ValueError(f"unknown segment kind: {kind}")
            start = end
        length = math.fsum(lengths)
    if not math.isfinite(length) or length <= 0:
        raise ValueError("seam length must be positive and finite")
    return length


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, help="Path to the JSON fixture")
    args = parser.parse_args()

    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        first, second = fixture["seams"]
        tolerance = float(fixture["tolerance_mm"])
        lengths = (seam_length(first), seam_length(second))
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
