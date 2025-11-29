# Agenda de Contactos — CRUD con Validación Segura

Aplicación web sencilla en Flask que implementa un CRUD de contactos con:

- Persistencia en archivo JSON (`contactos.json`)
- Validación estricta de entradas
- Manejo de errores sin filtrar trazas al usuario
- Salida HTML escapada por defecto (plantillas Jinja2)

## Requisitos

- Python 3.9+
- Paquetes: `flask`

Instalación rápida:

```bash
pip install flask
```

## Ejecución

```bash
cd agenda_contactos_json
python app.py
```

Luego abre en tu navegador:

- http://127.0.0.1:5000/contactos
