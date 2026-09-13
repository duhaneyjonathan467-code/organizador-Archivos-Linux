import os
import shutil
import subprocess
import json
import sys

# 1. Definimos la ruta del archivo de configuración
CONFIG_FILE = os.path.expanduser('~/config.json')

def cargar_configuracion():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: No se encontró el archivo de configuración en {CONFIG_FILE}")
        sys.exit()

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# 2. Usamos Zenity para abrir una ventana y elegir la carpeta
try:
    carpeta_origen = subprocess.check_output(
        ['zenity', '--file-selection', '--directory', '--title=Selecciona la carpeta a organizar']
    ).decode('utf-8').strip()
except subprocess.CalledProcessError:
    print("Cancelado por el usuario.")
    sys.exit()

if not carpeta_origen:
    print("No se seleccionó ninguna carpeta.")
    sys.exit()

print(f"Organizando la carpeta: {carpeta_origen}")

# 3. Cargamos las reglas desde el archivo config.json
tipos_archivos = cargar_configuracion()

# 4. Creamos las carpetas si no existen
for categoria in tipos_archivos:
    ruta_categoria = os.path.join(carpeta_origen, categoria)
    if not os.path.exists(ruta_categoria):
        os.makedirs(ruta_categoria)

# 5. Revisamos cada archivo en la carpeta seleccionada
for archivo in os.listdir(carpeta_origen):
    ruta_archivo = os.path.join(carpeta_origen, archivo)
    
    if os.path.isdir(ruta_archivo):
        continue

    _, extension = os.path.splitext(archivo)
    extension = extension.lower()

    movido = False
    for categoria, extensiones in tipos_archivos.items():
        if extension in extensiones:
            carpeta_destino = os.path.join(carpeta_origen, categoria)
            ruta_final = os.path.join(carpeta_destino, archivo)
            
            if os.path.exists(ruta_final):
                nombre_base, ext = os.path.splitext(archivo)
                contador = 1
                while os.path.exists(ruta_final):
                    nuevo_nombre = f"{nombre_base}_{contador}{ext}"
                    ruta_final = os.path.join(carpeta_destino, nuevo_nombre)
                    contador += 1

            try:
                shutil.move(ruta_archivo, ruta_final)
                print(f"Movido: {archivo} -> {categoria}/")
                movido = True
            except Exception as e:
                print(f"Error moviendo {archivo}: {e}")
            break
            
    if not movido:
        carpeta_otros = os.path.join(carpeta_origen, 'Otros')
        if not os.path.exists(carpeta_otros):
            os.makedirs(carpeta_otros)
            
        ruta_final_otros = os.path.join(carpeta_otros, archivo)
        if os.path.exists(ruta_final_otros):
            nombre_base, ext = os.path.splitext(archivo)
            contador = 1
            while os.path.exists(ruta_final_otros):
                nuevo_nombre = f"{nombre_base}_{contador}{ext}"
                ruta_final_otros = os.path.join(carpeta_otros, nuevo_nombre)
                contador += 1
                
        shutil.move(ruta_archivo, ruta_final_otros)
        print(f"Movido: {archivo} -> Otros/")

print("¡Organización completada con éxito!")
