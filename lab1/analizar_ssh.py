#!/usr/bin/env python3
import re
import json
from datetime import datetime
from collections import Counter

# Configuración de rutas
LOG_PATH = "auth.log"
OUTPUT_PATH = "reporte_ssh.json"

def analizar_logs():
    intentos_por_ip = Counter()
    total_fallidos = 0

    try:
        # 1. Leer el archivo auth.log
        with open(LOG_PATH, "r", errors="ignore") as file:
            for linea in file:
                # Filtrar intentos de autenticación fallidos
                if "Failed password" in linea:
                    total_fallidos += 1
                    
                    # 2. Extraer la dirección IP de origen usando Regex
                    # Busca un patrón estándar de IP (ej. 192.168.1.1)
                    match = re.search(r'from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', linea)
                    if match:
                        ip = match.group(1)
                        intentos_por_ip[ip] += 1

    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo {LOG_PATH}")
        return

    # 3. Identificar las 10 IPs con mayor número de intentos fallidos (Ranking ordenado)
    top_10_ips = intentos_por_ip.most_common(10)

    # Preparar la lista para el archivo JSON
    ips_sospechosas_json = []

    print("--- RANKING DE IPS Y ALERTAS ---")
    for ip, intentos in top_10_ips:
        # Determinar si supera los 50 intentos para activar la alerta
        alerta_activa = intentos > 50
        
        # 4. Generar una alerta en consola si alguna IP supera 50 intentos
        if alerta_activa:
            print(f"[ALERTA] IP: {ip} - {intentos} intentos fallidos - Posible ataque de fuerza bruta")
        else:
            print(f"IP: {ip} - Intentos: {intentos}")

        # Guardar estructura para el JSON
        ips_sospechosas_json.append({
            "ip": ip,
            "intentos": intentos,
            "alerta": alerta_activa
        })

    # 5. Exportar el resultado al archivo reporte_ssh.json con la estructura solicitada
    resultado_final = {
        "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_intentos_fallidos": total_fallidos,
        "ips_sospechosas": ips_sospechosas_json
    }

    with open(OUTPUT_PATH, "w") as json_file:
        json.dump(resultado_final, json_file, indent=4, ensure_ascii=False)
        
    print(f"\n[OK] Análisis completado. Reporte guardado en {OUTPUT_PATH}")

if __name__ == "__main__":
    analizar_logs()
