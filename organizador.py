import os
import shutil

# 1. Definimos la carpeta que vamos a ordenar (Descargas)
carpeta_origen = os.path.expanduser('~/Descargas')

# 2. Definimos qué tipo de archivos van a cada carpeta
tipos_archivos = {
    'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Musica': ['.mp3', '.wav'],
    'Comprimidos': ['.zip', '.rar', '.7z']
}

# 3. Creamos las carpetas si no existen
for categoria in tipos_archivos:
    ruta_categoria = os.path.join(carpeta_origen, categoria)
    if not os.path.exists(ruta_categoria):
        os.makedirs(ruta_categoria)

print("Iniciando organización...")

# 4. Revisamos cada archivo en la carpeta de Descargas
for archivo in os.listdir(carpeta_origen):
    ruta_archivo = os.path.join(carpeta_origen, archivo)
    
    if os.path.isdir(ruta_archivo):
        continue

    _, extension = os.path.splitext(archivo)
    extension = extension.lower()

    movido = False
    for categoria, extensiones in tipos_archivos.items():
        if extension in extensiones:
            # Ruta base de la carpeta destino
            carpeta_destino = os.path.join(carpeta_origen, categoria)
            ruta_final = os.path.join(carpeta_destino, archivo)
            
            # --- NUEVO: Lógica para evitar sobrescribir archivos ---
            if os.path.exists(ruta_final):
                nombre_base, ext = os.path.splitext(archivo)
                contador = 1
                # Mientras el archivo exista, le sumamos 1 al contador y probamos un nombre nuevo
                while os.path.exists(ruta_final):
                    nuevo_nombre = f"{nombre_base}_{contador}{ext}"
                    ruta_final = os.path.join(carpeta_destino, nuevo_nombre)
                    contador += 1
            # ---------------------------------------------------------

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
            
        # Aplicamos la misma lógica de renombre para la carpeta "Otros"
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
