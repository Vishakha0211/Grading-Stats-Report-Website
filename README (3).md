# Grading Stats Report 3.0 — Web Build Source

These three files are the actual source used to generate the final
`Grading_Stats_Report_3_0_Web.html` file.

## How it fits together

1. **gen.py** — Holds all the report data (extracted and verified against
   the source PDF) as plain Python data structures, plus helper functions
   that turn that data into:
   - Colour-coded HTML heatmap tables (freshie grades, sophomore/thirdie
     core courses, minors, AP distribution)
   - A `course-grid` of colour-scaled tiles (Top-30 CBS courses)
   - A single `chart_data.json` payload consumed by Chart.js in the browser

   Run it first: `python3 gen.py`
   → produces `data_out.json` and `chart_data.json`

2. **template.html** — The full page: CSS design system (colour tokens,
   card/heatmap/radar styles, responsive sidebar nav), the section markup
   for all 12 topics, and the `<script>` block with the Chart.js calls
   (`groupedBar`, `radarChart`, `fourYearBar`, `butterflyChart`, etc.)
   that render every chart from `CHART_DATA`. It contains placeholder
   tokens like `__FRESHIE_TABLE__` and `__CHART_DATA_JSON__` that get
   substituted at build time.

3. **assemble.py** — Reads `data_out.json` + `chart_data.json`, inlines
   the Chart.js library itself (so the final file needs zero internet
   access to render charts), substitutes all placeholders into
   `template.html`, and writes the finished, self-contained
   `Grading_Stats_Report_3_0_Web.html`.

   Run it second: `python3 assemble.py`

## To rebuild from scratch

```bash
pip install pdf2image pytesseract  # only needed if re-extracting from the PDF
npm pack chart.js@4.4.4            # downloads chart.js-4.4.4.tgz
mkdir -p pkg && tar -xzf chart.js-4.4.4.tgz -C pkg
python3 gen.py
python3 assemble.py
```

The Chart.js UMD bundle (`pkg/package/dist/chart.umd.js`) is the one
piece not included here since it's a third-party library, not code I
wrote — grab it via `npm pack chart.js@4.4.4` as shown above, or swap
`assemble.py` back to a CDN `<script src="...">` tag if you're fine with
an internet-dependent version.
