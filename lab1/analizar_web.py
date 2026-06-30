#!/usr/bin/env python3
import re
import json
from datetime import datetime
from collections import defaultdict

LOG_PATH = "access.log"
OUTPUT_PATH = "reporte_web.json"

# Expresión regular para el formato Combined de Apache
LOG_REGEX = r'^(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+)\s*.*?" (\d{3}) (\S+)'

def analizar_web():
    errores_por_ip = defaultdict(int)
    peticiones_por_ip_tiempo = defaultdict(list)
    ips_con_escaneo = set()
    intentos_sqli = 0
    
    # Patrones de SQL Injection
    sqli_patterns = [r"UNION", r"SELECT", r"--", r"OR\s+1=1", r"'"]
    sqli_regex = re.compile("|".join(sqli_patterns), re.IGNORECASE)

    try:
        with open(LOG_PATH, "r", errors="ignore") as file:
            for linea in file:
                match = re.match(LOG_REGEX, linea)
                if not match:
                    continue
                
                ip, timestamp_str, metodo, url, status, _ = match.groups()
                status_code = int(status)
                
                # Convertir timestamp a objeto datetime
                # Ejemplo: 30/Jun/2026:15:10:15 -0500 -> se remueve el offset para simplificar
                time_part = timestamp_str.split()[0]
                dt = datetime.strptime(time_part, "%d/%b/%Y:%H:%M:%S")
                timestamp_epoch = dt.timestamp()
                
                # Requerimiento 2: Detectar escaneo de directorios (>20 peticiones en <60s)
                peticiones_por_ip_tiempo[ip].append(timestamp_epoch)
                # Filtrar peticiones en la ventana de los últimos 60 segundos
                recientes = [t for t in peticiones_por_ip_tiempo[ip] if timestamp_epoch - t <= 60]
                peticiones_por_ip_tiempo[ip] = recientes
                if len(recientes) > 20:
                    ips_con_escaneo.add(ip)
                
                # Requerimiento 3: Identificar códigos 4xx y 5xx agrupados por IP
                if status.startswith(('4', '5')):
                    errores_por_ip[ip] += 1
                
                # Requerimiento 4: Detectar intentos de SQL Injection en la URL
                if sqli_regex.search(url):
                    intentos_sqli += 1

    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo {LOG_PATH}")
        return

    # Estructurar hallazgos
    reporte = {
        "escaneo_directorios": list(ips_con_escaneo),
        "errores_por_ip": dict(errores_por_ip),
        "intentos_sql_injection": intentos_sqli
    }

    # Requerimiento 5: Guardar el archivo json
    with open(OUTPUT_PATH, "w") as json_file:
        json.dump(reporte, json_file, indent=4, ensure_ascii=False)
        
    print("✅ Reporte WEB generado con éxito.")

if __name__ == "__main__":
    analizar_web()
