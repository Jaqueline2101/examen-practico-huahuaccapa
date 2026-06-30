#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Rutas e inicialización de variables globales
SSH_JSON = "reporte_ssh.json"
ACCESS_LOG = "access.log"
GRAFICAS_DIR = "graficas"
os.makedirs(GRAFICAS_DIR, exist_ok=True)

print("📊 Iniciando generación de gráficos solicitados...")

# -------------------------------------------------------------------------
# GRAFICO 1: Gráfico de barras — IPs con más intentos fallidos SSH (Estilizado)
# -------------------------------------------------------------------------
try:
    with open(SSH_JSON, "r") as f:
        ssh_data = json.load(f)
    ips_sospechosas = ssh_data.get("ips_sospechosas", [])
    
    if ips_sospechosas:
        # CAMBIO CLAVE: Cambiamos a [:15] para que muestre bastantes IPs en el gráfico
        ips_ordenadas = sorted(ips_sospechosas, key=lambda x: x["intentos"], reverse=True)[:15]
        
        ips = [item["ip"] for item in ips_ordenadas]
        intentos = [item["intentos"] for item in ips_ordenadas]

        # Estilo profesional de cuadrícula blanca
        sns.set_style("whitegrid")
        
        # Generamos una paleta degradada basada en la cantidad exacta de IPs que entren
        custom_colors = sns.color_palette("flare_r", len(ips)) 

        # Ajustamos el tamaño a (11, 7) para que entren cómodamente muchas IPs sin amontonarse
        plt.figure(figsize=(11, 7)) 
        
        # Invertimos los datos con [::-1] para que la IP con MÁS intentos quede arriba del todo
        ax = sns.barplot(
            x=intentos[::-1], 
            y=ips[::-1], 
            hue=ips[::-1], 
            palette=custom_colors, 
            legend=False
        )
        
        plt.title("Top IPs con más intentos fallidos SSH", fontsize=15, fontweight='bold', pad=15)
        plt.xlabel("Número de Intentos", fontsize=12, fontweight='bold')
        plt.ylabel("Direcciones IP", fontsize=12, fontweight='bold')
        
        ax.tick_params(axis='y', labelsize=10)
        plt.tight_layout()
        
        grafica_ssh_path = os.path.join(GRAFICAS_DIR, "top_10_ssh_fallidos.png")
        plt.savefig(grafica_ssh_path, dpi=300)
        plt.close()
        print("✔️ Gráfico 1 (Barras SSH con múltiples IPs) generado.")
except Exception as e:
    print(f"⚠️ Error en Gráfico 1: {e}")

# -------------------------------------------------------------------------
# Procesamiento de access.log para Gráficos 2 y 3
# -------------------------------------------------------------------------
log_data = []
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
                    continue

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
