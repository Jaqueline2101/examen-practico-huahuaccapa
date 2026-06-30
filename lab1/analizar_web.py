import json

log_path = "access.log"

total = 0
errors = 0

with open(log_path, "r", errors="ignore") as file:
    for line in file:
        total += 1
        if "404" in line or "500" in line:
            errors += 1

reporte = {
    "total_requests": total,
    "error_requests": errors
}

with open("reporte_web.json", "w") as f:
    json.dump(reporte, f, indent=4)

print("✅ Reporte WEB generado")
