import re
import json

log_path = "auth.log"

failed = 0
accepted = 0
ips = {}

with open(log_path, "r", errors="ignore") as file:
    for line in file:
        if "Failed password" in line:
            failed += 1
            ip = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            if ip:
                ip = ip[0]
                ips[ip] = ips.get(ip, 0) + 1

        elif "Accepted password" in line:
            accepted += 1

reporte = {
    "failed_logins": failed,
    "successful_logins": accepted,
    "top_ips": sorted(ips.items(), key=lambda x: x[1], reverse=True)[:5]
}

with open("reporte_ssh.json", "w") as f:
    json.dump(reporte, f, indent=4)

print("✅ Reporte SSH generado correctamente")
