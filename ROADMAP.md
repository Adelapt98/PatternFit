# PatternFit roadmap

## Goal

Build an offline workbench for inspecting and editing sewing patterns before cutting fabric. A maker should be able to load a five-size bodice and sleeve set, trace a fit problem to the exact pair of notches that bounds it, edit the stitch line, and print the corrected pieces at actual size.

The main challenge is correspondence along a seam. Two seams can have identical total lengths and still disagree between notches. Designers also add ease deliberately, so the tool needs to distinguish an intended length difference from an error.

## Current baseline

The Python command compares the total length of two stitch lines. It supports straight seams and continuous paths of line and quadratic Bézier segments. It includes a legacy straight-seam fixture, a curved fixture and tests against an analytic curve length. There is no pattern document editor yet.

## Milestones

### 1. Define the pattern document and seam pairings

- Define a versioned JSON format for pieces, stitch outlines, named spans along those outlines, seam pairs, and notch positions anchored to segments.
- Preserve stable piece and segment IDs when editing coordinates. Add an explicit conversion from the current demo format.
- Report invalid references, discontinuous outlines and missing pair endpoints with piece or seam identifiers.
- **Acceptance** — a synthetic bodice and sleeve sample round-trips through save and load without changing IDs or geometry. Tests cover dangling references and malformed paths.

### 2. Walk paired seams by notch interval

- Add arc-length lookup and its inverse so a point on either path can be located by distance along the seam. Normalize traversal direction at the pairing level so reversed pieces compare correctly.
- Match explicit notch IDs, then measure each interval between matched notches, including the start and end intervals.
- Store intended ease per interval with a signed convention. Report measured lengths, intended ease and remaining mismatch separately.
- **Acceptance** — fixtures cover reversed paths, a seam split across several segments, missing or misordered notches, equal totals with mismatched intervals, and intentional ease. A failing result identifies the piece, seam and bounding notches.

### 3. Generate cut lines and seam allowances

- Offset closed stitch outlines outward with configurable allowances by edge. Define corner behavior for joins with different allowances.
- Detect collapsed segments and self-intersections, and retain the relationship between stitch lines and generated cut lines so notches can be projected onto the export geometry.
- **Acceptance** — rectangle and curved fixtures verify offset distances, convex and concave joins and notch projection. Invalid offsets identify the source piece and region and block its print export.

### 4. Grade the pattern across five sizes

- Define grading rules for anchors and control points. Recompute derived geometry after each size is generated.
- Compare all paired intervals per size and flag where a rule creates a fit regression. Keep the base geometry editable and derived sizes reproducible.
- **Acceptance** — a fixed five-size fixture produces identical geometry from the same input. A deliberately broken grading rule identifies only the affected sizes and notch intervals.

### 5. Build the local browser editor

- Serve a local editor with a scaled piece canvas, zoom and pan, selection, curve handles, notch labels and paired seam highlighting.
- Add undo and redo, local document save and load, and a panel that jumps to the problem interval from a diagnostic.
- **Acceptance** — from a fresh local browser session, open the fixture, edit a handle, inspect the resulting mismatch, undo the edit and reopen the saved document. Verify that piece IDs and seam pairings survive the workflow.

### 6. Export printable pattern sheets

- Export vector sheets with explicit millimeter dimensions, piece labels, size labels, grain lines and a calibration square.
- Tile large pieces for A4 and Letter. Include overlap and registration marks so pages can be assembled at full scale.
- **Acceptance** — check exported dimensions from vector coordinates, verify alignment across tiles, and confirm that piece and size identities remain visible. Include a synthetic export for checking browser print preview at 100%.

## Release check

Use a synthetic five-size bodice and sleeve set. Open it in the editor and change one curve. Check that the tool identifies the affected sizes, seam and notch intervals. After correction, every paired interval must be within 1 mm after accounting for its declared ease. Save and reopen the document, then export the pattern and verify a 50 mm calibration square in the vector output.

## Environment

Use Python's standard library for geometry, validation, tests and the local server. Use browser-native HTML, CSS, JavaScript and SVG for the editor. Keep fixtures and assets in the repository and run the workflow offline with Python 3.12 and Chrome. A later milestone can introduce a dependency if it is available in the workspace and improves a specific part of the implementation.
