#!/usr/bin/env python3
import random

# Lista de IPs falsas que quieres que aparezcan en tu gráfica
ips_falsas = [
    "192.168.1.50", "10.0.0.15", "172.16.5.88", "185.220.101.5", 
    "45.33.32.11", "193.32.162.1", "91.240.118.5", "8.8.8.8",
    "200.48.5.12", "147.242.19.1", "115.88.85.2", "183.17.75.9"
]

print("💉 Inyectando registros de intentos fallidos en auth.log...")

with open("auth.log", "a") as f:
    for ip in ips_falsas:
        # Genera un número aleatorio de intentos entre 10 y 150 por cada IP
        intentos = random.randint(10, 150)
        for _ in range(intentos):
            # Formato estándar que tu script 'analizar_ssh.py' reconoce usando "Failed password" y "from <IP>"
            linea = f"Jun 30 15:00:00 huahuaccapa sshd[12345]: Failed password for invalid user root from {ip} port 54321 ssh2\n"
            f.write(linea)

print("✅ ¡Inyección completada con éxito!")
