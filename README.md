# Grading Stats Report 3.0 — Web Edition

An interactive dashboard for the IIT Bombay Grading Stats Report 3.0, built by the Data Analytics and Visualization (DAV) Team, UGAC.

**Live features:**
- Full grading report with 12 sections (heatmaps, bar charts, radar charts, distribution curves)
- **Department Dashboard** — select any department to view its specific grading stats
- **Dark Mode** toggle with localStorage persistence
- Responsive sidebar navigation with scroll-spy

## Prerequisites

- **Python 3** (no extra packages needed)
- **Node.js + npm** (to install Chart.js)

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/Grading-Stats-Report-Website.git
cd Grading-Stats-Report-Website

# 2. Install Chart.js (needed for inlining into the HTML)
npm install chart.js

# 3. Generate data + build both HTML files
python gen.py
python assemble.py

# 4. Serve locally
python -m http.server 8000
```

Then open **http://localhost:8000/index.html** in your browser.

## Project Structure

```
├── gen.py                    # Data extraction + helper functions
├── template.html             # Main report page template
├── dept_template.html        # Department dashboard template
├── assemble.py               # Build script (combines templates + data + Chart.js)
├── index.html                # Generated: main report (output)
├── dept.html                 # Generated: department dashboard (output)
├── data_out.json             # Generated: HTML table components
├── chart_data.json           # Generated: Chart.js data payload
├── dept_data.json            # Generated: department-specific data
└── node_modules/chart.js/    # Chart.js library (installed via npm)
```

## How the Build Pipeline Works

| Step | Command | What it does |
|------|---------|--------------|
| 1 | `python gen.py` | Reads raw data → produces `data_out.json`, `chart_data.json`, `dept_data.json` |
| 2 | `python assemble.py` | Combines templates + data + inlines Chart.js → outputs `index.html` + `dept.html` |

- **`gen.py`** — Contains all report data as Python data structures, plus helper functions that generate colour-coded HTML heatmaps, course tiles, and JSON payloads for Chart.js.
- **`template.html`** — The main report page with CSS design system, section markup for all 12 topics, and Chart.js calls. Contains placeholders like `__FRESHIE_TABLE__` and `__CHART_DATA_JSON__`.
- **`dept_template.html`** — The department dashboard with a selector grid, sticky section nav, and dynamic charts populated from `dept_data.json`.
- **`assemble.py`** — Reads all JSON files, inlines Chart.js (so the final HTML needs zero internet access), substitutes placeholders, and writes the finished pages.

## Dark Mode

Click the 🌌 button at the bottom of the sidebar (main report) or top-right (department dashboard). Your preference is saved in `localStorage`.

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-change`)
3. Make changes to `template.html`, `dept_template.html`, or `gen.py`
4. Run `python gen.py && python assemble.py` to rebuild
5. Test locally at `http://localhost:8000`
6. Commit and push your changes

## Credits

- **Report by:** Harsh, Ummehani, Vishakha, Zubair
- **Project led by:** Rakshana
- **Web edition:** DAV Team, UGAC
- **Data source:** Internal ASC, IIT Bombay (UG-open courses only)
