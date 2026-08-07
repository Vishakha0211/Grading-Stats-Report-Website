import json

with open("data_out.json") as f:
    comp = json.load(f)
with open("chart_data.json") as f:
    chart_data = json.load(f)
with open("template.html", encoding="utf-8") as f:
    html = f.read()

with open("pkg/package/dist/chart.umd.js", encoding="utf-8") as f:
    chartjs_src = f.read()
html = html.replace("/*__CHARTJS_INLINE__*/", chartjs_src)

replacements = {
    "__FRESHIE_TABLE__": comp["freshie_table"],
    "__SOPH_TABLE__": comp["soph_table"],
    "__THIRD_TABLE__": comp["third_table"],
    "__MINORS_24_25_TABLE__": comp["minors_24_25_table"],
    "__MINORS_22_23_TABLE__": comp["minors_22_23_table"],
    "__TOP30_AUTUMN__": comp["top30_autumn_html"],
    "__TOP30_SPRING__": comp["top30_spring_html"],
    "__AP_TABLE__": comp["ap_table_html"],
    "__CHART_DATA_JSON__": json.dumps(chart_data),
}

for k, v in replacements.items():
    if k not in html:
        print("WARNING: placeholder not found:", k)
    html = html.replace(k, v)

out_path = "/mnt/user-data/outputs/Grading_Stats_Report_3_0_Web.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Written:", out_path, "size(kb)=", round(len(html)/1024,1))
