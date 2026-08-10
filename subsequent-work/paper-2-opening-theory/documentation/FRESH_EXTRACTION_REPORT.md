# Fresh-extraction report

## Final result

Evidence: `VERIFIED-BYTE` and `VERIFIED-EXACT`.

The compact archive was extracted into a previously absent short-path directory. Its location-independent PowerShell launcher was invoked from outside the extracted tree with explicit frozen Python and latexmk executables. The run produced:

- `VERIFIED-BYTE` for every closed-world manifest entry;
- `VERIFIED-EXACT` for the locked cofactor, 52-term denominator, endpoint support, signed boundary, ARC1 (4/5), GF1 (-32/15), 15-cell atlas and 16-cone atlas;
- `FALSIFIED` for the deliberately perturbed Hamiltonian, with both the cofactor and moment routes detecting the discrepancy;
- regenerated exact LaTeX tables; and
- a 25-page PDF after a complete pdfLaTeX/Biber stabilisation cycle.

The final log contained no undefined references, undefined citations, empty bibliography, duplicate labels, missing figures or overfull boxes.

## Corrected preliminary attempt

The first extracted invocation exposed a path-assumption defect in `REPRODUCE.ps1`: relative paths were resolved against the caller rather than the script directory. No mathematical command ran. The launchers were corrected, the manifest and archive were regenerated, and the successful test above used a second untouched extraction. The event is retained in `FAILURE_LEDGER.md` rather than erased.

After this report and the gate ledger were added, the final archive was resealed and subjected to the same fresh manifest, exact, falsifier, table and build sequence in a third untouched directory.
