Deploy en Render (pasos rápidos)
=================================

1) Subir el repo a GitHub
- Si aún no está en GitHub, inicializa y sube el repo:

```bash
git init
git add .
git commit -m "Proyecto_Seguridad: preparar despliegue en Render"
git branch -M main
git remote add origin <TU_REPO_URL>
git push -u origin main
```

2) Archivos importantes en el repo
- `requirements.txt` — dependencias (`Flask`, `gunicorn`).
- `Procfile` — comando de inicio: `web: gunicorn app:app --log-file -`.
- `runtime.txt` — opcional para fijar versión de Python.
- `contactos.json` — archivo de datos (si lo necesitas persistente, render ofrece discos efímeros; considera usar DB externa si es crítico).

3) Crear servicio en Render
- Entra a render.com y crea una cuenta (o entra con GitHub).
- New → Web Service → Connect a GitHub
- Selecciona tu repo `Proyecto_Seguridad`
- Branch: `main`
- Build Command: dejar vacío o usar `pip install -r requirements.txt` (Render suele detectarlo)
- Start Command: `gunicorn app:app --log-file -`

4) Variables de entorno
- En `Environment` / `Variables` agrega `SECRET_KEY` con un valor seguro (cadena larga aleatoria). `app.py` usa `os.environ.get('SECRET_KEY')`.

5) Archivos estáticos / persistencia
- Render proporciona almacenamiento efímero: `contactos.json` se mantendrá mientras la instancia viva. Para producción, usa una base de datos (Postgres, SQLite en disco compartido no recomendado).

6) Revisar logs y dominio
- Una vez desplegado, Render mostrará logs de build y runtime. Usa la URL que Render asigna para probar la app en producción.

Comandos para probar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:8000 app:app
# Abrir http://127.0.0.1:8000
```

Notas de seguridad
- No dejes el `SECRET_KEY` embebido en el código en producción.
- Render permite configurar `Environment` variables en la UI.
