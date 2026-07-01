import sys
import pandas as pd
import joblib

# Cargar archivos (Asegúrate de que existan en la misma carpeta)
try:
    model = joblib.load('modelo_anomalias.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError as e:
    print(f"Error: No se encontraron los archivos del modelo/scaler. {e}")
    sys.exit(1)

def predecir(archivo_csv):
    """
    Realiza la carga, feature engineering y predicción de anomalías.
    """
    try:
        df = pd.read_csv(archivo_csv)
        
        # 1. Replicar el mismo feature engineering del entrenamiento
        df['ratio_bytes'] = df['bytes_sent'] / (df['bytes_recv'] + 1)
        df['bytes_por_segundo'] = df['bytes_sent'] / (df['duration_sec'] + 1)
        
        # 2. Seleccionar y normalizar (usando el scaler guardado)
        features = df.select_dtypes(include=['float64', 'int64'])
        df_scaled = scaler.transform(features)
        
        # 3. Clasificar
        preds = model.predict(df_scaled)
        df['prediccion'] = preds
        
        # 4. Filtrar y mostrar anomalías
        anomalias = df[df['prediccion'] == -1]
        
        if not anomalias.empty:
            print("--- Anomalías detectadas ---")
            print(anomalias[['src_ip', 'dst_ip', 'prediccion']])
        else:
            print("No se detectaron anomalías en el archivo.")
            
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo: {e}")

if __name__ == "__main__":
    # Verifica si se pasó un argumento desde la terminal
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        # Valor por defecto si no se pasa nada
        archivo = 'network_traffic.csv'
        print("No se proporcionó archivo. Usando 'network_traffic.csv' por defecto.")
    
    predecir(archivo)