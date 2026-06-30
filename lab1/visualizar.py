import json
import matplotlib.pyplot as plt

# SSH
with open("reporte_ssh.json") as f:
    ssh = json.load(f)

labels = ["Failed", "Success"]
values = [ssh["failed_logins"], ssh["successful_logins"]]

plt.bar(labels, values)
plt.title("Intentos SSH")
plt.savefig("graficas/ssh.png")
plt.clf()

# WEB
with open("reporte_web.json") as f:
    web = json.load(f)

labels = ["Total", "Errores"]
values = [web["total_requests"], web["error_requests"]]

plt.bar(labels, values)
plt.title("Peticiones Web")
plt.savefig("graficas/web.png")

print("✅ Gráficas generadas")
