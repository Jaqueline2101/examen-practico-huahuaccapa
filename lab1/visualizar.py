#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Rutas e inicialización
SSH_JSON = "reporte_ssh.json"
ACCESS_LOG = "access.log"
GRAFICAS_DIR = "graficas"
os.makedirs(GRAFICAS_DIR, exist_ok=True)

print("📊 Iniciando generación de gráficos solicitados...")

# -------------------------------------------------------------------------
# GRAFICO 1: Gráfico de barras — Top 10 IPs con más intentos fallidos SSH
# -------------------------------------------------------------------------
try:
    with open(SSH_JSON, "r") as f:
        ssh_data = json.load(f)
    ips_sospechosas = ssh_data.get("ips_sospechosas", [])
    
    if ips_sospechosas:
        ips = [item["ip"] for item in ips_sospechosas[:10]]
        intentos = [item["intentos"] for item in ips_sospechosas[:10]]
        
        plt.figure(figsize=(10, 5))
        # Se asigna 'hue' para solucionar la advertencia de la biblioteca
        sns.barplot(x=intentos, y=ips, hue=ips, palette="Reds_r", legend=False)
        plt.title("Top 10 IPs con más intentos fallidos SSH")
        plt.xlabel("Número de Intentos")
        plt.tight_layout()
        plt.savefig(os.path.join(GRAFICAS_DIR, "top_10_ssh_fallidos.png"))
        plt.close()
        print("✔️ Gráfico 1 (Barras SSH) generado.")
except Exception as e:
    print(f"⚠️ Error en Gráfico 1: {e}")

# Parsing robusto de access.log para Gráficos 2 y 3
log_data = []
# Captura la IP [grupo 1], la fecha [grupo 2] y el código de estado [grupo 3] de forma segura
LOG_MINIMAL_REGEX = r'^(\S+) \S+ \S+ \[(.*?)\] ".*?" (\d{3})'

if os.path.exists(ACCESS_LOG):
    with open(ACCESS_LOG, "r", errors="ignore") as f:
        for linea in f:
            match = re.search(LOG_MINIMAL_REGEX, linea)
            if match:
                try:
                    _, timestamp_str, status = match.groups()
                    time_part = timestamp_str.split()[0]
                    dt = datetime.strptime(time_part, "%d/%b/%Y:%H:%M:%S")
                    log_data.append({"Hora": dt.hour, "Status": int(status)})
                except Exception:
                    continue # Omite líneas con formatos de fecha corruptos

df = pd.DataFrame(log_data)

if not df.empty:
    # -------------------------------------------------------------------------
    # GRAFICO 2: Línea de tiempo — Número de peticiones HTTP por hora
    # -------------------------------------------------------------------------
    try:
        peticiones_por_hora = df.groupby("Hora").size().reindex(range(24), fill_value=0)
        
        plt.figure(figsize=(10, 4))
        plt.plot(peticiones_por_hora.index, peticiones_por_hora.values, marker='o', color='b', linestyle='-')
        plt.title("Número de peticiones HTTP por hora durante el día")
        plt.xlabel("Hora del Día")
        plt.ylabel("Cantidad de Peticiones")
        plt.xticks(range(24))
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(GRAFICAS_DIR, "peticiones_por_hora.png"))
        plt.close()
        print("✔️ Gráfico 2 (Línea de tiempo HTTP) generado.")
    except Exception as e:
        print(f"⚠️ Error en Gráfico 2: {e}")

    # -------------------------------------------------------------------------
    # GRAFICO 3: Mapa de calor (heatmap) — Peticiones HTTP por hora y código
    # -------------------------------------------------------------------------
    try:
        codigos_requeridos = [200, 301, 404, 500]
        df_filtrado = df[df["Status"].isin(codigos_requeridos)]
        
        pivot_df = pd.crosstab(df_filtrado["Status"], df_filtrado["Hora"])
        pivot_df = pivot_df.reindex(index=codigos_requeridos, columns=range(24), fill_value=0)
        
        plt.figure(figsize=(12, 5))
        sns.heatmap(pivot_df, annot=True, fmt="d", cmap="YlOrRd", linewidths=.5)
        plt.title("Mapa de Calor: Peticiones HTTP por Hora y Código de Respuesta")
        plt.xlabel("Hora del Día")
        plt.ylabel("Código de Respuesta")
        plt.tight_layout()
        plt.savefig(os.path.join(GRAFICAS_DIR, "heatmap_peticiones.png"))
        plt.close()
        print("✔️ Gráfico 3 (Heatmap) generado.")
    except Exception as e:
        print(f"⚠️ Error en Gráfico 3: {e}")
else:
    print("⚠️ No hay datos válidos procesados desde access.log para los gráficos.")

print("\n🚀 ¡Todos los pasos de visualización completados con éxito!")
