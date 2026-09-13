#!/bin/bash

# Colores para que la terminal se vea profesional
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # Sin color

echo -e "${GREEN}=== Instalando Organizador de Archivos ===${NC}"

# 1. Verificar si Zenity está instalado
if ! command -v zenity &> /dev/null; then
    echo "Instalando dependencia: zenity..."
    sudo apt install zenity -y
fi

# 2. Crear la carpeta de instalación en el sistema del usuario
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications

# 3. Copiar los scripts y la configuración
echo "Copiando archivos..."
cp ~/organizador_gui.py ~/.local/bin/organizador_gui.py

# Copiar la configuración solo si no existe (para no sobrescribir la del usuario)
if [ ! -f ~/config.json ]; then
    cp ~/config.json ~/config.json
fi

# 4. Crear el acceso directo en el menú de aplicaciones del sistema
cat << EOF > ~/.local/share/applications/organizador.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Organizador de Archivos
Comment=Ordena automáticamente tus carpetas
Exec=python3 $HOME/.local/bin/organizador_gui.py
Icon=folder
Terminal=false
Categories=Utility;
EOF

# 5. Dar permisos de ejecución
chmod +x ~/.local/bin/organizador_gui.py
chmod +x ~/.local/share/applications/organizador.desktop

echo -e "${GREEN}¡Instalación completada con éxito!${NC}"
echo "Busca 'Organizador' en tu menú de aplicaciones para usarlo."
