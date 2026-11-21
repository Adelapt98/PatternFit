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
