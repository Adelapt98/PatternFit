# PatternFit

PatternFit is a planned offline workbench for checking how sewing pattern pieces fit together before cutting fabric. This starter measures one pair of stitch lines in a synthetic pattern and reports their difference in millimeters.

## Run the starter

Requires Python 3.12 or later. No packages or network access are needed.

```sh
python3 patternfit.py examples/bodice.json
```

The example compares a 120 mm front side seam with a 121.5 mm back side seam. It prints a 1.50 mm difference and exits with status 1 because the difference exceeds the fixture's 1 mm tolerance. A match within tolerance exits with status 0.

The JSON fixture contains exactly two named seams. A straight seam can use `start` and `end`. A multi-segment seam uses `start` and an ordered `segments` list. Each segment supplies an `end` and a `kind` of `line` or `quadratic`. Quadratic segments also supply a `control` point. All coordinates are in millimeters.

Run the curved example and the tests:

```sh
python3 patternfit.py examples/curved.json
python3 -m unittest -v
```

The curved example compares a two-segment path with a straight reference strip of the same length. Fixtures without pairing data compare total lengths.

## Compare seams by notch

```sh
python3 patternfit.py examples/notched.json
```

This example intentionally exits with status 1. Both seams are 100 mm long, but the interval from the shoulder notch to the end is 10 mm shorter on the second seam. The first interval passes because its 10 mm difference is declared as intended ease.

- Each seam can list `notches` with an `id` and a `distance_mm` measured along that seam from its authored start. List them in increasing distance. IDs must be unique within each seam. The checker supplies the reserved endpoints `start` and `end`.
- Set `pairing.reverse_second` to `true` when the second seam is authored in the opposite direction. In sewing order, the two seams must have the same sequence of IDs.
- Each optional `pairing.ease` entry names adjacent boundaries with `from` and `to` in sewing order and an `ease_mm` value. Positive ease means the second seam is expected to be longer. The residual is the measured second length minus the first length minus intended ease. Each interval must pass the fixture tolerance.

See [ROADMAP.md](ROADMAP.md) for the remaining work.

## Example outcomes

| Fixture | What it demonstrates | Exit code |
| --- | --- | --- |
| `examples/bodice.json` | Straight seams differ by 1.50 mm and exceed tolerance. | 1 |
| `examples/curved.json` | A curve joined to a line matches the reference length. | 0 |
| `examples/notched.json` | Equal total lengths hide a failing notch interval. | 1 |
| `examples/notched-with-ease.json` | A 10 mm difference is intentional and both intervals pass. | 0 |
| `examples/notched-missing-counterpart.json` | A missing matching notch makes the pairing invalid. | 2 |
