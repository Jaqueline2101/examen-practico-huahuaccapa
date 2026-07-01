import pandas as pd
import joblib
import os

model = joblib.load('modelo_anomalias.pkl')
scaler = joblib.load('scaler.pkl')

def monitorear_log(archivo_log):
    df = pd.read_csv(archivo_log)
    # ... (aplicar mismo feature engineering que en el entrenamiento) ...
    features = df.select_dtypes(include=['float64', 'int64'])
    df_scaled = scaler.transform(features)
    
    df['prediccion'] = model.predict(df_scaled)
    anomalias = df[df['prediccion'] == -1]
    
    if not anomalias.empty:
        with open('alerta_seguridad.txt', 'a') as f:
            for _, row in anomalias.iterrows():
                mensaje = f"ALERTA: Anomalía detectada en IP {row['src_ip']} - {pd.Timestamp.now()}\n"
                f.write(mensaje)
        print("¡Alerta generada en alerta_seguridad.txt!")

monitorear_log('ulogd_procesado.csv')