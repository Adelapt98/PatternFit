"""Match named notches along two measured stitch lines."""

import math


def seam_boundaries(notches, length, *, reverse=False):
    """Return the seam endpoints and notches in sewing order."""
    boundaries = [("start", 0.0)]
    seen = {"start", "end"}
    for notch in notches:
        name = notch["id"]
        distance = notch["distance_mm"]
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError(f"invalid or duplicate notch ID: {name!r}")
        if not math.isfinite(distance) or not boundaries[-1][1] < distance < length:
            raise ValueError(f"notch {name!r} must be ordered and inside the seam")
        boundaries.append((name, distance))
        seen.add(name)
    if reverse:
        boundaries = [("start", 0.0)] + [
            (name, length - distance) for name, distance in reversed(boundaries[1:])
        ]
    return [*boundaries, ("end", length)]


def paired_intervals(first, second):
    """Yield bounding IDs and measured lengths for each paired interval."""
    if [name for name, _ in first] != [name for name, _ in second]:
        raise ValueError("paired seams must have the same notch IDs in sewing order")
    for (start, a_start), (end, a_end), (_, b_start), (_, b_end) in zip(
        first, first[1:], second, second[1:]
    ):
        yield start, end, a_end - a_start, b_end - b_start


def compare_intervals(first, second, ease_by_interval):
    """Yield each interval's measurements, intended ease and residual mismatch."""
    intervals = list(paired_intervals(first, second))
    unknown = ease_by_interval.keys() - {(start, end) for start, end, _, _ in intervals}
    if unknown:
        raise ValueError(f"ease references unknown intervals: {sorted(unknown)!r}")
    for start, end, a_length, b_length in intervals:
        ease = ease_by_interval.get((start, end), 0.0)
        if not math.isfinite(ease):
            raise ValueError(f"ease for {start!r} to {end!r} must be finite")
        yield start, end, a_length, b_length, ease, (b_length - a_length) - ease
