# PatternFit

PatternFit is a planned offline workbench for checking how sewing pattern pieces fit together before cutting fabric. This starter measures one pair of straight stitch lines in a synthetic pattern and reports their difference in millimeters.

## Run the starter

Requires Python 3.12 or later. No packages or network access are needed.

```sh
python3 patternfit.py examples/bodice.json
```

The example compares a 120 mm front side seam with a 121.5 mm back side seam. It prints a 1.50 mm difference and exits with status 1 because the difference exceeds the fixture's 1 mm tolerance. A match within tolerance exits with status 0.

The JSON file contains exactly two seams. Each seam has a name and two Cartesian endpoints in millimeters. Endpoints describe the stitch line. The fixture is synthetic and contains no measurements from a person.

## Work still ahead

The central design problem is correspondence along a seam. Two stitch lines can have the same total length while their notches land at different positions. A deliberate length difference can also be distributed across only part of a seam, such as a gathered section.

- **Geometry and matching.** Represent curved and multi-segment stitch lines. Map notches by distance along the seam, handle reversed piece orientation, and support explicit ease between adjacent notches. Check curved lengths against independently computed reference fixtures.
- **Allowances and grading.** Offset curved stitch lines into cut lines, handle corners and report self-intersections. Apply grading rules and report exactly which sizes and notch intervals violate their tolerances.
- **Editor and export.** Build a local browser editor with a piece canvas, paired seam highlighting and an impact panel. Export SVG sheets with registration marks and a printable scale square using bundled assets.
- **End-to-end acceptance.** Load a synthetic five-size bodice and sleeve set. Changing one curve should identify the affected size, seam and notch interval. Across all five sizes, unexplained mismatch must stay within 1 mm, intended ease must be reported separately, and exported sheets must preserve scale and piece identity.

The planned stack is standard-library Python and browser-native HTML, CSS and JavaScript. Geometry, fixtures and exports can all be exercised locally.
