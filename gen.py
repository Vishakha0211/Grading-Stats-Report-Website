#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a single self-contained HTML file reproducing the
"Grading Stats Report 3.0" PDF as a browsable, downloadable web page.
All data below was extracted directly from the source PDF (text layer +
pixel-level verification of the radar charts and stacked bars).
"""
import json

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

freshie_courses = ["BB101","CH111","CH117","CS101","MA105","MA110","MS101","PH110","PH117"]
freshie = {
 "BB101":[8.20,8.30,7.86], "CH111":[6.50,6.79,6.75], "CH117":[9.46,9.60,9.54],
 "CS101":[7.57,7.59,7.28], "MA105":[6.52,8.08,6.77], "MA110":[6.31,7.25,6.24],
 "MS101":[8.53,8.66,8.53], "PH110":[7.48,7.02,6.91], "PH117":[8.20,7.92,8.37],
}
freshie_years = [2023,2024,2025]

core_depts = ["AE","CE","CL","CS","EE","EN","EP","ES","IEOR","ME","MM"]
soph = {"AE":[7.21,7.27],"CE":[7.08,7.37],"CL":[7.07,7.01],"CS":[7.23,7.22],"EE":[7.56,7.40],
 "EN":[7.31,6.78],"EP":[6.96,7.02],"ES":[7.66,7.86],"IEOR":[None,8.33],"ME":[7.44,7.34],"MM":[7.44,7.03]}
third = {"AE":[7.35,7.42],"CE":[7.15,7.48],"CL":[7.12,6.95],"CS":[7.30,7.28],"EE":[7.62,7.55],
 "EN":[7.38,7.10],"EP":[7.02,7.05],"ES":[7.72,7.92],"IEOR":[None,None],"ME":[7.25,7.41],"MM":[7.51,7.18]}

# electives autumn/spring: dept -> [ [avg24,n24], [avg25,n25] ]
elec_autumn_g1 = {
 "AE":[[7.21,33],[6.63,31]], "BB":[[8.20,29],[8.42,28]], "CE":[[7.55,46],[7.73,49]],
 "CH":[[7.99,31],[7.99,31]], "CL":[[6.98,29],[7.57,27]], "CS":[[8.29,29],[7.73,39]],
 "EC":[[7.78,13],[7.85,16]], "EE":[[7.49,51],[7.83,54]], "EN":[[7.32,22],[7.55,26]],
 "ENT":[[8.29,10],[8.48,9]],
}
elec_autumn_g2 = {
 "ES":[[7.31,22],[7.60,22]], "GP":[[8.90,47],[8.45,42]], "HS":[[8.50,40],[8.15,38]],
 "IDC":[[8.40,80],[8.68,92]], "IEOR":[[7.75,13],[7.61,13]], "MA":[[7.86,41],[7.59,39]],
 "ME":[[7.45,38],[7.18,34]], "MG":[[7.93,53],[8.03,47]], "MM":[[8.08,34],[7.57,41]],
 "PH":[[7.65,25],[7.85,29]],
}
elec_spring_g1 = {
 "AE":[[6.85,26],[7.02,34]], "BB":[[7.80,22],[7.96,26]], "CE":[[7.52,35],[7.78,43]],
 "CH":[[7.61,32],[7.81,35]], "CL":[[7.18,14],[7.13,22]], "CS":[[7.52,27],[7.45,39]],
 "EC":[[7.41,11],[7.55,14]], "EE":[[7.85,44],[7.86,54]], "EN":[[7.65,19],[7.38,22]],
 "ENT":[[8.37,11],[8.54,14]],
}
elec_spring_g2 = {
 "ES":[[8.23,19],[8.19,23]], "GP":[[8.44,36],[8.48,37]], "HS":[[8.41,21],[7.65,33]],
 "IDC":[[8.64,60],[8.54,72]], "IEOR":[[7.45,7],[7.17,11]], "MA":[[7.10,30],[7.62,39]],
 "ME":[[7.75,34],[7.63,42]], "MG":[[8.33,39],[7.42,37]], "MM":[[7.89,24],[7.61,39]],
 "PH":[[7.78,25],[8.04,29]],
}

elec_sd_order = ["AE","BB","CE","CH","CL","CS","EC","EE","EN","ENT","ES","GP","HS","IDC","IEOR","MA","ME","MG","MM","PH"]
elec_sd_2025 = [1.263,0.814,0.807,1.098,1.182,0.904,0.728,0.809,0.979,0.469,0.920,0.790,1.061,0.625,1.195,1.044,0.984,0.585,1.131,1.018]
elec_sd_2024 = [1.087,0.979,0.979,1.111,1.120,0.887,0.668,0.973,1.017,0.457,0.828,0.742,0.878,0.726,1.363,1.053,0.867,0.725,0.991,1.154]

dept_sd_order = ["AE","CE","CH","CL","CS","EC","EE","EN","ENT","ES","GP","HS","IDC","IEOR","MA","ME","MG","MM","PH"]
dept_sd_2025 = [1.210,0.818,1.109,1.122,0.886,0.827,0.783,1.048,0.537,0.968,0.790,1.058,0.623,1.177,1.047,0.953,0.610,1.103,1.073]
dept_sd_2024 = [1.033,0.936,1.123,1.083,1.194,0.738,0.982,0.980,0.481,0.848,0.742,0.884,0.723,1.310,1.221,0.847,0.755,0.950,1.082]

# minors: dept -> [ [avg,n]|None  for A24,S24,A25,S25 ]
minors_24_25_order = ["AE","BB","CS","DH","OS","EC","EE","ENT","ES","HSS","MA","MG","MM","PH","Robotics","SysCon","SI"]
minors_24_25 = {
 "AE":[[6.91,8],[6.29,4],[6.23,4],[6.45,4]],
 "BB":[[7.95,4],[8.47,6],[7.56,7],[7.81,4]],
 "CS":[[7.19,5],[5.76,4],[7.52,4],[6.42,4]],
 "DH":[[7.92,4],[8.02,2],[7.65,5],[8.85,4]],
 "OS":[[7.08,2],[7.32,2],[6.88,1],[7.51,2]],
 "EC":[[5.76,1],None,[5.30,1],None],
 "EE":[[6.54,4],[5.91,5],[6.64,4],None],
 "ENT":[[7.65,8],[7.88,9],[8.31,8],[8.25,12]],
 "ES":[[5.80,1],[10.00,1],[8.67,1],None],
 "HSS":[[9.06,1],None,[8.08,1],[8.21,3]],
 "MA":[[6.57,2],[7.16,2],[7.21,2],[6.58,2]],
 "MG":[[7.46,4],[5.89,1],[7.25,3],[7.12,2]],
 "MM":[None,None,None,[8.00,1]],
 "PH":[[7.67,2],[7.27,1],[6.97,2],[5.96,2]],
 "Robotics":[[6.53,4],None,[5.02,2],[7.61,3]],
 "SysCon":[[7.12,9],[7.17,3],[7.85,10],[8.06,7]],
 "SI":[[7.38,2],[8.27,2],[8.76,2],[8.19,2]],
}
minors_22_23_order = ["AE","BB","CS","DH","DS","EC","EE","ENT","ES","HSS","MA","MG","MM","PH","Robotics","SysCon","SI"]
minors_22_23 = {
 "AE":[[5.58,7],[5.08,6],[5.54,8],[5.32,5]],
 "BB":[[7.13,5],[9.06,5],[7.64,6],[8.12,5]],
 "CS":[[7.14,3],[6.91,3],[6.48,3],[7.04,4]],
 "DH":[[9.00,2],[6.00,3],[8.74,3],[7.16,4]],
 "DS":[[8.21,1],[7.29,1],[7.82,1],[6.79,2]],
 "EC":[None,None,None,None],
 "EE":[[7.63,2],[6.63,3],[7.19,2],[6.13,3]],
 "ENT":[[8.27,3],[7.38,3],[8.43,4],[7.65,5]],
 "ES":[[8.88,2],[8.00,1],[8.65,2],[7.17,2]],
 "HSS":[[7.48,2],[8.27,2],[8.60,1],[8.50,1]],
 "MA":[[5.74,2],[6.71,2],[7.44,2],[6.58,2]],
 "MG":[[7.72,2],[7.27,3],[7.80,2],[6.98,1]],
 "MM":[[10.00,2],[8.00,2],None,None],
 "PH":[[7.89,2],[7.38,1],[7.46,2],[5.71,1]],
 "Robotics":[None,None,None,None],
 "SysCon":[[6.29,8],[8.04,10],[7.82,9],[7.61,11]],
 "SI":[[7.38,2],[8.27,2],[7.14,2],None],
}

top30_autumn = [["DE6103",96],["DE348",96],["DE334",94],["DE343",91],["EE721",87],["EE789",78],
 ["ES451",62],["HS472",61],["SOM622",59],["DE347",58],["PS635",56],["CL461",54],
 ["ES657",49],["DE335",46],["CL443",44],["DE353",43],["DE205",40],["GS527",39],
 ["DE203",39],["GS421",39],["HS471",37],["DE201",37],["DE113",36],["DE111",36],
 ["MM751",34],["ENT623",32],["BB653",32],["CH801",31],["BB619",28],["SC650",15]]
top30_spring = [["DE344",82],["DE614",70],["DE612",69],["CM801",68],["SOM725",63],["CM703",56],
 ["DH308",56],["DE335",48],["DE342",47],["GS540",45],["CL445",43],["ENT606",41],
 ["GS538",39],["GS438",39],["MM739",39],["ME770",38],["GS450",38],["DE118",38],
 ["DE126",37],["TD626",37],["DE203",37],["DE138",37],["ENT624",37],["DE112",35],
 ["GP516",35],["MM674",33],["DE114",32],["ENT605",32],["TD642",31],["ME761",19]]

overall_g1_order = ["AE","BB","CE","CH","CL","CS","EC","EE","EN","ENT"]
overall_g1 = {
 "AE":[6.92,7.09,7.26,7.07], "BB":[8.20,8.27,8.04,7.89], "CE":[7.20,7.04,7.28,7.49],
 "CH":[7.65,7.94,7.87,8.17], "CL":[7.03,7.08,7.31,7.24], "CS":[7.57,7.57,7.72,7.55],
 "EC":[7.64,7.72,7.79,7.77], "EE":[7.58,7.75,7.79,7.70], "EN":[7.18,7.13,7.49,7.35],
 "ENT":[8.70,8.31,8.31,8.40],
}
overall_g2_order = ["ES","GP","IDC","IEOR","MA","ME","MG","MM","PH"]
overall_g2 = {
 "ES":[7.75,7.71,7.83,7.78], "GP":[8.09,7.88,8.44,8.38], "IDC":[8.20,8.67,8.61,8.54],
 "IEOR":[7.22,7.09,7.15,7.61], "MA":[6.67,6.73,7.54,6.78], "ME":[7.61,7.49,7.33,7.54],
 "MG":[7.77,7.84,7.86,7.94], "MM":[7.19,7.34,7.49,7.17], "PH":[7.46,7.61,7.39,7.54],
}
overall_years = [2022,2023,2024,2025]

# autumn vs spring: dept -> [A24,A25,S24,S25]
avs_g1_order = ["AE","BB","CE","CH","CL","CS","EC","EE","EN","ENT"]
avs_g1 = {
 "AE":[7.34,7.06,7.13,7.09], "BB":[8.25,7.96,7.68,7.80], "CE":[7.28,7.53,7.30,7.45],
 "CH":[7.74,8.32,8.06,8.02], "CL":[7.24,7.11,7.40,7.37], "CS":[7.83,7.56,7.56,7.54],
 "EC":[7.80,7.81,7.30,7.61], "EE":[7.74,7.62,7.84,7.79], "EN":[7.51,7.33,7.47,7.38],
 "ENT":[8.35,8.45,8.27,8.39],
}
avs_g2_order = ["ES","GP","IDC","IEOR","MA","ME","MG","MM","PH"]
avs_g2 = {
 "ES":[7.71,7.92,7.97,7.63], "GP":[8.53,8.31,8.39,8.43], "IDC":[8.55,8.54,8.64,8.54],
 "IEOR":[7.18,7.68,7.06,7.54], "MA":[7.71,6.91,7.36,6.65], "ME":[7.24,7.30,7.45,7.74],
 "MG":[7.69,7.89,8.05,7.99], "MM":[7.45,7.32,7.56,7.02], "PH":[7.47,7.67,7.34,7.44],
}

ap_depts = ["AE","BB","CE","CH","CL","CS","EE","EN","ENT","ES","IDC","IEOR","MA","ME","MG","MM","PH"]
ap_dist = {
 "AE":[13.91,12.14,7.66,12.39], "BB":[50.30,34.13,68.63,47.27], "CE":[17.57,23.46,20.46,21.86],
 "CH":[45.56,23.92,22.55,27.23], "CL":[28.14,21.58,27.46,38.25], "CS":[40.04,37.64,45.91,35.02],
 "EE":[29.00,21.32,27.40,27.32], "EN":[0.00,7.63,0.00,10.94], "ENT":[50.44,72.57,76.02,69.08],
 "ES":[0.00,3.43,20.16,16.75], "IDC":[0.00,0.00,5.34,4.88], "IEOR":[9.88,26.39,13.85,13.79],
 "MA":[49.69,50.73,37.80,29.61], "ME":[24.82,23.79,16.44,12.77], "MG":[11.98,3.64,4.34,7.83],
 "MM":[17.70,19.82,23.89,33.58], "PH":[26.15,17.45,22.16,19.82],
}

aa_buckets = ["0-10%","10-20%","20-30%","30-40%","40-50%","50-60%","60-70%","70-80%","80-90%","90-100%"]
aa_2024 = [459,492,259,108,71,40,37,19,15,2]
aa_2025 = [496,542,288,134,72,47,34,32,16,4]

kde_minors = [
 {"year":2022,"sd":1.146,"n":57,"mode":7.79},
 {"year":2023,"sd":0.987,"n":56,"mode":7.57},
 {"year":2024,"sd":1.044,"n":62,"mode":7.22},
 {"year":2025,"sd":1.216,"n":68,"mode":7.25},
]
courses_dist = {
 2024:{"n":1824,"mean":7.799,"sd":1.378,"median":7.947},
 2025:{"n":1997,"mean":7.804,"sd":1.379,"median":8.000},
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def color_for_grade(v, lo=6.0, hi=10.0):
    """Green (low) -> deep pink/red (high) scale similar to source heatmaps."""
    if v is None:
        return "#f4f4f4"
    t = max(0.0, min(1.0, (v - lo) / (hi - lo)))
    # interpolate light green -> amber -> deep rose
    stops = [(0.0,(198,239,206)),(0.5,(255,235,156)),(1.0,(248,105,107))]
    for i in range(len(stops)-1):
        t0,c0 = stops[i]; t1,c1 = stops[i+1]
        if t0 <= t <= t1:
            f = 0 if t1==t0 else (t-t0)/(t1-t0)
            r = round(c0[0]+(c1[0]-c0[0])*f); g = round(c0[1]+(c1[1]-c0[1])*f); b = round(c0[2]+(c1[2]-c0[2])*f)
            return f"rgb({r},{g},{b})"
    return "#f4f4f4"

def color_for_pct(v, lo=0, hi=100):
    """Yellow -> pink -> deep magenta scale (matches AP heatmap)."""
    t = max(0.0, min(1.0, (v - lo) / (hi - lo)))
    stops = [(0.0,(255,247,204)),(0.5,(250,159,140)),(1.0,(190,30,90))]
    for i in range(len(stops)-1):
        t0,c0 = stops[i]; t1,c1 = stops[i+1]
        if t0 <= t <= t1:
            f = 0 if t1==t0 else (t-t0)/(t1-t0)
            r = round(c0[0]+(c1[0]-c0[0])*f); g = round(c0[1]+(c1[1]-c0[1])*f); b = round(c0[2]+(c1[2]-c0[2])*f)
            return f"rgb({r},{g},{b})"
    return "#f4f4f4"

def color_for_enroll(v, lo, hi):
    t = max(0.0, min(1.0, (v - lo) / (hi - lo))) if hi>lo else 0
    stops = [(0.0,(255,247,204)),(0.55,(250,159,110)),(1.0,(199,21,110))]
    for i in range(len(stops)-1):
        t0,c0 = stops[i]; t1,c1 = stops[i+1]
        if t0 <= t <= t1:
            f = 0 if t1==t0 else (t-t0)/(t1-t0)
            r = round(c0[0]+(c1[0]-c0[0])*f); g = round(c0[1]+(c1[1]-c0[1])*f); b = round(c0[2]+(c1[2]-c0[2])*f)
            return f"rgb({r},{g},{b})"
    return "#f4f4f4"

def txt_color(rgb_str):
    # crude luminance check to choose black/white text
    nums = rgb_str.replace("rgb(","").replace(")","").split(",")
    r,g,b = [int(x) for x in nums]
    lum = 0.299*r+0.587*g+0.114*b
    return "#1a1330" if lum > 150 else "#ffffff"

def fmt(v):
    return "—" if v is None else f"{v:.2f}"

def heatmap_table(depts, data, years, unit=""):
    head = "".join(f"<th>{y}</th>" for y in years)
    rows = []
    for d in depts:
        cells = ""
        for v in data[d]:
            if v is None:
                cells += '<td class="hm-cell hm-empty">—</td>'
            else:
                bg = color_for_grade(v)
                cells += f'<td class="hm-cell" style="background:{bg};color:{txt_color(bg)}">{v:.2f}</td>'
        rows.append(f"<tr><th class='rowlabel'>{d}</th>{cells}</tr>")
    return f"""<table class="heatmap"><thead><tr><th></th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"""

def minors_table(order, data, label):
    cols = ["Autumn 2024","Spring 2024","Autumn 2025","Spring 2025"] if "24" in label else ["Autumn 2022","Spring 2022","Autumn 2023","Spring 2023"]
    head = "".join(f"<th>{c}</th>" for c in cols)
    rows = []
    for d in order:
        cells = ""
        for entry in data[d]:
            if entry is None:
                cells += '<td class="hm-cell hm-empty">—</td>'
            else:
                v,n = entry
                bg = color_for_grade(v, lo=5.0, hi=10.0)
                cells += f'<td class="hm-cell" style="background:{bg};color:{txt_color(bg)}"><b>{v:.2f}</b><br><span class="n-tag">n={n}</span></td>'
        rows.append(f"<tr><th class='rowlabel'>{d}</th>{cells}</tr>")
    return f"""<table class="heatmap minors"><thead><tr><th></th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"""

def ap_table():
    head = "".join(f"<th>{y}</th>" for y in [2022,2023,2024,2025])
    rows = []
    for d in ap_depts:
        cells = ""
        for v in ap_dist[d]:
            bg = color_for_pct(v)
            cells += f'<td class="hm-cell" style="background:{bg};color:{txt_color(bg)}">{v:.2f}</td>'
        rows.append(f"<tr><th class='rowlabel'>{d}</th>{cells}</tr>")
    return f"""<table class="heatmap"><thead><tr><th></th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"""

def top30_grid(items):
    vals = [v for _,v in items]
    lo, hi = min(vals), max(vals)
    cells = []
    for code, v in items:
        bg = color_for_enroll(v, lo, hi)
        cells.append(f'<div class="course-tile" style="background:{bg};color:{txt_color(bg)}"><div class="course-code">{code}</div><div class="course-n">{v}</div></div>')
    return f'<div class="course-grid">{"".join(cells)}</div>'

def js_arr(a):
    return json.dumps(a)

# ---------------------------------------------------------------------------
# BUILD SUB-COMPONENTS
# ---------------------------------------------------------------------------

freshie_rows = []
for c in freshie_courses:
    cells = "".join(f"<td class='hm-cell' style='background:{color_for_grade(v)};color:{txt_color(color_for_grade(v))}'>{v:.2f}</td>" for v in freshie[c])
    freshie_rows.append(f"<tr><th class='rowlabel'>{c}</th>{cells}</tr>")
freshie_table = f"""<table class="heatmap"><thead><tr><th></th>{''.join(f'<th>{y}</th>' for y in freshie_years)}</tr></thead><tbody>{''.join(freshie_rows)}</tbody></table>"""

soph_table = heatmap_table(core_depts, soph, [2024,2025])
third_table = heatmap_table(core_depts, third, [2024,2025])
minors_24_25_table = minors_table(minors_24_25_order, minors_24_25, "24_25")
minors_22_23_table = minors_table(minors_22_23_order, minors_22_23, "22_23")
top30_autumn_html = top30_grid(top30_autumn)
top30_spring_html = top30_grid(top30_spring)
ap_table_html = ap_table()

with open("data_out.json","w") as f:
    json.dump({
        "freshie_table": freshie_table,
        "soph_table": soph_table,
        "third_table": third_table,
        "minors_24_25_table": minors_24_25_table,
        "minors_22_23_table": minors_22_23_table,
        "top30_autumn_html": top30_autumn_html,
        "top30_spring_html": top30_spring_html,
        "ap_table_html": ap_table_html,
    }, f)

# ---------------------------------------------------------------------------
# JS chart data payload
# ---------------------------------------------------------------------------

def dept_val_n(d):
    labels = list(d.keys())
    v24 = [d[k][0][0] for k in labels]
    n24 = [d[k][0][1] for k in labels]
    v25 = [d[k][1][0] for k in labels]
    n25 = [d[k][1][1] for k in labels]
    return {"labels":labels,"v24":v24,"n24":n24,"v25":v25,"n25":n25}

chart_data = {
    "elecAutumnG1": dept_val_n(elec_autumn_g1),
    "elecAutumnG2": dept_val_n(elec_autumn_g2),
    "elecSpringG1": dept_val_n(elec_spring_g1),
    "elecSpringG2": dept_val_n(elec_spring_g2),
    "elecSD": {"labels": elec_sd_order, "y2025": elec_sd_2025, "y2024": elec_sd_2024},
    "deptSD": {"labels": dept_sd_order, "y2025": dept_sd_2025, "y2024": dept_sd_2024},
    "overallG1": {"labels": overall_g1_order, "years": overall_years,
                  "data": {y: [overall_g1[k][i] for k in overall_g1_order] for i,y in enumerate(overall_years)}},
    "overallG2": {"labels": overall_g2_order, "years": overall_years,
                  "data": {y: [overall_g2[k][i] for k in overall_g2_order] for i,y in enumerate(overall_years)}},
    "avsG1": {"labels": avs_g1_order,
              "a24":[avs_g1[k][0] for k in avs_g1_order], "a25":[avs_g1[k][1] for k in avs_g1_order],
              "s24":[avs_g1[k][2] for k in avs_g1_order], "s25":[avs_g1[k][3] for k in avs_g1_order]},
    "avsG2": {"labels": avs_g2_order,
              "a24":[avs_g2[k][0] for k in avs_g2_order], "a25":[avs_g2[k][1] for k in avs_g2_order],
              "s24":[avs_g2[k][2] for k in avs_g2_order], "s25":[avs_g2[k][3] for k in avs_g2_order]},
    "aa": {"labels": aa_buckets, "y2024": aa_2024, "y2025": aa_2025},
    "kdeMinors": kde_minors,
    "coursesDist": courses_dist,
}

with open("chart_data.json","w") as f:
    json.dump(chart_data, f)

print("all data generated")

