# Agenda de Contactos — CRUD con Validación Segura

Descripción
-----------
Esta aplicación es una agenda de contactos mínima construida con Flask. Permite crear, listar, editar y eliminar contactos; los datos se almacenan en un fichero JSON local (`contactos.json`). Incluye validación para nombre, correo, teléfono, etiqueta y notas, y usa plantillas Jinja2 para renderizar la interfaz.

Las operaciones principales son:
- Listar todos los contactos válidos
- Crear un nuevo contacto (con validación)
- Editar un contacto existente (con validación)
- Eliminar un contacto con confirmación

Tecnologías usadas
------------------
- Python 3.9+
- Flask
- Jinja2
- Bootstrap 5
- JSON (almacenamiento simple en `contactos.json`)

**Requisitos**
- Python 3.9 o superior
- Flask
  
## Instrucciones de instalación y ejecución

Sigue la sección correspondiente a tu sistema operativo y shell.

**macOS / Linux (zsh, bash)**

```bash
# Sitúate en la raíz del proyecto
cd "/ruta/a/tu/proyecto/Proyecto_Seguridad"

# Crear y activar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install flask

# Ejecutar la aplicación
python app.py

# Abrir en el navegador
# http://127.0.0.1:5000/contactos
```

**Windows (PowerShell)**

```powershell
# Sitúate en la raíz del proyecto
cd "C:\ruta\a\tu\proyecto\Proyecto_Seguridad"

# Crear y activar el entorno virtual (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt  # si tienes requirements.txt
# ó, si no tienes requirements.txt
pip install flask

# Ejecutar la aplicación
python app.py
```

**Windows (CMD)**

```cmd
cd C:\ruta\a\tu\proyecto\Proyecto_Seguridad
python -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```


# Abrir en el navegador
http://127.0.0.1:5000/contactos
