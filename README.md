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

The curved example compares a two-segment path with a straight reference strip of the same length. The checker compares total lengths. See [ROADMAP.md](ROADMAP.md) for the rest of the project.
