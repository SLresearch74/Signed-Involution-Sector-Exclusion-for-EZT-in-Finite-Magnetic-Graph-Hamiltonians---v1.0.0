# Source scan report

## Result

The recursive scientific-source recovery completed without a read error.

- files hashed: **3,636**;
- unique SHA-256 byte streams: **932**;
- duplicate-content groups: **631**;
- unique text streams searched: **780**;
- unique PDFs extracted: **20**;
- representative search hits: **6,645**.

These counts are `MEASURED` with the sample sizes stated. The machine-readable inventory is in `DATA/FULL_SOURCE_INVENTORY.csv`; duplicate groups are in `DATA/DUPLICATE_CONTENT_GROUPS.json`; PDF extraction is in `DATA/PDF_SOURCE_SCAN.csv`.

## Method

Every readable byte of each unique relevant text file was searched for theorem language, evidence labels, corrections, release identifiers, scope warnings, moment/amplitude distinctions, fixed/moving distinctions, real/complex qualifications, citations and reproducibility markers. Byte-identical texts were searched once and linked to every path by SHA-256. PDFs were deduplicated by hash and independently extracted with `pypdf`.

Excluded directory classes were `.git`, dependency caches, `node_modules`, bundled TinyTeX trees, `__pycache__`, rendered-PDF scratch directories, the `_PAPERII_WORK` scratch tree and this new release tree. Those exclusions remove vendor or generated material, not scientific source bundles.

## Authority rule

Authority follows content and correction history, not filename copy numbers. A later corrected theorem statement supersedes an earlier prose summary even when the earlier file is named `FINAL`. The key example is ARC1: the colleague clarification narrows real non-cancellation to real-analytic Hermitian data with real leading constants.

The label `TFP` was not found as an authoritative release identifier in the scientific sources. `TF1` is the supported label. `TFP` is therefore treated as an unsupported alias, not invented into the paper.

