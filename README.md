"# examen-practico-huahuaccapa" 
Aquí tienes tu **README.md completo en formato código listo para copiar y pegar sin modificar nada** 👇

````markdown
# 🛡️ Laboratorio 1: Análisis Forense de Logs con Python

Este proyecto corresponde al desarrollo del **Lab1**, enfocado en el análisis de logs de un servidor Linux (SSH) y un servidor web (Apache), con el objetivo de detectar posibles ataques y generar visualizaciones.

---

## 📂 Estructura del Proyecto

Directorio: `~/examen-practico-huahuaccapa/lab1`

```text
lab1/
├── access.log
├── auth.log
├── analizar_ssh.py
├── analizar_web.py
├── visualizar.py
├── generar_ataques_falsos.py
├── reporte_ssh.json
├── reporte_web.json
├── evidencias/
└── graficas/
    ├── heatmap_peticiones.png
    ├── peticiones_por_hora.png
    └── top_10_ssh_fallidos.png
````

---

## ⚙️ Requisitos

* Python 3
* Librerías necesarias:

```bash
pip install matplotlib seaborn pandas
```
![Imagen](lab1/evidencias/instalacion%20de%20pandas.png)
---

## 🚀 Ejecución del Proyecto

### 1. Dar permisos a los scripts

```bash
chmod +x analizar_ssh.py analizar_web.py visualizar.py
```
![Imagen](lab1/evidencias/Permiso%20a%20los%20scrips.png)
---

### 2. (Opcional) Generar ataques de prueba

```bash
sudo python3 generar_ataques_falsos.py
```
![Imagen](lab1/evidencias/Ataques.png)
---

### 3. Ejecutar análisis de logs

#### 🔐 Análisis SSH

```bash
python3 analizar_ssh.py
```

✔ Detecta intentos fallidos (`Failed password`)
✔ Cuenta intentos por IP
✔ Genera ranking de IPs
✔ Alerta si hay más de 50 intentos
✔ Exporta `reporte_ssh.json`

---
![Imagen](lab1/evidencias/Analisis.png)
#### 🌐 Análisis Web

```bash
python3 analizar_web.py
```

✔ Detecta escaneo de directorios (>20 rutas en <60s)
✔ Agrupa códigos HTTP (2xx, 3xx, 4xx, 5xx)
✔ Detecta posibles SQL Injection (`UNION`, `SELECT`, `--`)
✔ Genera `reporte_web.json`

---
![Imagen](lab1/evidencias/Analizar_web.png)
### 4. Generar visualizaciones

```bash
python3 visualizar.py
```
![Imagen](lab1/evidencias/Visualizar.png)
Se generan las siguientes gráficas en `graficas/`:

* 📊 **top_10_ssh_fallidos.png** → Top 10 IPs con más intentos fallidos
* 📈 **peticiones_por_hora.png** → Número de peticiones HTTP por hora
* 🔥 **heatmap_peticiones.png** → Peticiones por hora vs código HTTP

---

## 📊 Descripción de Resultados

### 🔐 SSH (auth.log)

* Identificación de ataques de fuerza bruta
* Ranking de IPs más sospechosas
* Alertas automáticas por comportamiento anómalo

### 🌐 WEB (access.log)

* Detección de escaneo de directorios
* Identificación de ataques SQL Injection
* Análisis de tráfico HTTP por estado de respuesta

### 📉 Visualización

* Análisis gráfico del comportamiento del servidor
* Identificación rápida de patrones sospechosos

---

## 📁 Archivos Generados

* `reporte_ssh.json` → Resultados del análisis SSH
* `reporte_web.json` → Resultados del análisis WEB
* `graficas/*.png` → Evidencias visuales

---

## 🧪 Evidencias

Las capturas y pruebas adicionales pueden almacenarse en:

```text
evidencias/
```

---

## 🎯 Conclusión

Este laboratorio permite:

* Detectar ataques reales en logs
* Automatizar análisis de seguridad
* Generar evidencia visual clara
* Aplicar técnicas de ciberseguridad en entornos reales

---

## 👩‍💻 Autor

**Jaqueline Huahuaccapa Ccama**
Ingeniería de Sistemas – UPeU

```

---

Si quieres, en el siguiente paso te puedo hacer versión **más pro (nivel GitHub)** con:
- badges
- portada
- imágenes de tus gráficas
- y formato para que impresione al profesor 😎
```
