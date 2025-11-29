from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import logging
import re
from typing import List, Dict, Any, Optional

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "contactos.json")


# ---------- Utilidades de persistencia segura sobre JSON ----------

def cargar_contactos() -> List[Dict[str, Any]]:
    """Lee el archivo JSON y devuelve una lista de contactos.
    Si el archivo no existe o está vacío, devuelve una lista vacía.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except Exception as e:
        logging.exception("Error al leer contactos.json")
        # No revelamos detalles al usuario: devolvemos lista vacía
        return []


def guardar_contactos(contactos: List[Dict[str, Any]]) -> None:
    """Sobrescribe el archivo JSON de contactos de forma segura."""
    try:
        tmp_file = DATA_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(contactos, f, ensure_ascii=False, indent=2)
        os.replace(tmp_file, DATA_FILE)
    except Exception:
        logging.exception("Error al guardar contactos.json")
        # No levantamos la excepción hacia la vista para no exponer detalles.


def siguiente_id(contactos: List[Dict[str, Any]]) -> int:
    """Obtiene el siguiente ID entero para un nuevo contacto."""
    if not contactos:
        return 1
    return max(c.get("id", 0) for c in contactos) + 1


# ---------- Validación de entradas ----------

# Regex ancladas
NOMBRE_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{1,80}$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TELEFONO_REGEX = re.compile(r"^\+?[0-9 ]+$")

ETIQUETAS_VALIDAS = {"", "familia", "trabajo", "amigos", "otro"}


def validar_nombre(nombre: str) -> Optional[str]:
    if not nombre:
        return "El nombre es obligatorio."
    if len(nombre) > 80:
        return "El nombre no debe exceder 80 caracteres."
    if not NOMBRE_REGEX.match(nombre):
        return "El nombre solo puede contener letras, espacios y acentos."
    return None


def validar_correo(correo: str) -> Optional[str]:
    if not correo:
        return "El correo es obligatorio."
    if len(correo) > 120:
        return "El correo no debe exceder 120 caracteres."
    if not EMAIL_REGEX.match(correo):
        return "El formato de correo no es válido."
    return None


def validar_telefono(telefono: str) -> Optional[str]:
    if not telefono:
        return "El teléfono es obligatorio."
    # Eliminamos espacios para contar solo dígitos
    solo_digitos = re.sub(r"\D", "", telefono)
    if len(solo_digitos) < 7 or len(solo_digitos) > 15:
        return "El teléfono debe tener entre 7 y 15 dígitos."
    if not TELEFONO_REGEX.match(telefono):
        return "El teléfono solo puede contener dígitos, espacios y un '+' inicial."
    return None


def validar_etiqueta(etiqueta: str) -> Optional[str]:
    if etiqueta not in ETIQUETAS_VALIDAS:
        return "La etiqueta no es válida."
    return None


def validar_notas(notas: str) -> Optional[str]:
    if not notas:
        return None
    if len(notas) > 500:
        return "Las notas no deben exceder 500 caracteres."
    # No permitimos etiquetas HTML sencillas
    if "<" in notas or ">" in notas:
        return "Las notas no deben contener etiquetas HTML."
    return None


def validar_contacto_formulario(data: Dict[str, str]) -> Dict[str, str]:
    """Valida todos los campos del formulario. Devuelve dict de errores por campo."""
    errores = {}

    nombre = data.get("nombre", "").strip()
    correo = data.get("correo", "").strip()
    telefono = data.get("telefono", "").strip()
    etiqueta = data.get("etiqueta", "").strip()
    notas = data.get("notas", "").strip()

    err = validar_nombre(nombre)
    if err:
        errores["nombre"] = err

    err = validar_correo(correo)
    if err:
        errores["correo"] = err

    err = validar_telefono(telefono)
    if err:
        errores["telefono"] = err

    err = validar_etiqueta(etiqueta)
    if err:
        errores["etiqueta"] = err

    err = validar_notas(notas)
    if err:
        errores["notas"] = err

    return errores


# ---------- Rutas ----------

@app.route("/")
def index():
    return redirect(url_for("lista_contactos"))


@app.route("/contactos")
def lista_contactos():
    contactos = cargar_contactos()
    # Revalidamos antes de mostrar por seguridad defensiva
    contactos_validos = []
    for c in contactos:
        data = {
            "nombre": c.get("nombre", ""),
            "correo": c.get("correo", ""),
            "telefono": c.get("telefono", ""),
            "etiqueta": c.get("etiqueta", ""),
            "notas": c.get("notas", ""),
        }
        errores = validar_contacto_formulario(data)
        if errores:
            logging.warning("Contacto con datos inválidos no mostrado. ID=%s", c.get("id"))
            continue
        contactos_validos.append(c)

    return render_template("lista.html", contactos=contactos_validos)


@app.route("/contactos/nuevo", methods=["GET", "POST"])
def nuevo_contacto():
    if request.method == "POST":
        form_data = {
            "nombre": request.form.get("nombre", ""),
            "correo": request.form.get("correo", ""),
            "telefono": request.form.get("telefono", ""),
            "etiqueta": request.form.get("etiqueta", ""),
            "notas": request.form.get("notas", ""),
        }
        errores = validar_contacto_formulario(form_data)
        if errores:
            for campo, mensaje in errores.items():
                flash(f"{campo.capitalize()}: {mensaje}", "error")
            return render_template("formulario.html", contacto=form_data, modo="nuevo")
        try:
            contactos = cargar_contactos()
            nuevo = {
                "id": siguiente_id(contactos),
                "nombre": form_data["nombre"].strip(),
                "correo": form_data["correo"].strip(),
                "telefono": form_data["telefono"].strip(),
                "etiqueta": form_data["etiqueta"].strip(),
                "notas": form_data["notas"].strip(),
            }
            contactos.append(nuevo)
            guardar_contactos(contactos)
            flash("Contacto creado correctamente.", "exito")
            return redirect(url_for("lista_contactos"))
        except Exception:
            logging.exception("Error inesperado al crear contacto")
            flash("Ocurrió un error interno. Intenta de nuevo más tarde.", "error")
            return render_template("formulario.html", contacto=form_data, modo="nuevo")
    # GET
    contacto_vacio = {"nombre": "", "correo": "", "telefono": "", "etiqueta": "", "notas": ""}
    return render_template("formulario.html", contacto=contacto_vacio, modo="nuevo")


def obtener_contacto_por_id(contactos: List[Dict[str, Any]], contacto_id: int) -> Optional[Dict[str, Any]]:
    for c in contactos:
        if c.get("id") == contacto_id:
            return c
    return None


@app.route("/contactos/<int:contacto_id>/editar", methods=["GET", "POST"])
def editar_contacto(contacto_id: int):
    contactos = cargar_contactos()
    contacto = obtener_contacto_por_id(contactos, contacto_id)
    if not contacto:
        flash("Contacto no encontrado.", "error")
        return redirect(url_for("lista_contactos"))

    if request.method == "POST":
        form_data = {
            "nombre": request.form.get("nombre", ""),
            "correo": request.form.get("correo", ""),
            "telefono": request.form.get("telefono", ""),
            "etiqueta": request.form.get("etiqueta", ""),
            "notas": request.form.get("notas", ""),
        }
        errores = validar_contacto_formulario(form_data)
        if errores:
            for campo, mensaje in errores.items():
                flash(f"{campo.capitalize()}: {mensaje}", "error")
            return render_template("formulario.html", contacto=form_data, modo="editar")

        try:
            contacto["nombre"] = form_data["nombre"].strip()
            contacto["correo"] = form_data["correo"].strip()
            contacto["telefono"] = form_data["telefono"].strip()
            contacto["etiqueta"] = form_data["etiqueta"].strip()
            contacto["notas"] = form_data["notas"].strip()
            guardar_contactos(contactos)
            flash("Contacto actualizado correctamente.", "exito")
            return redirect(url_for("lista_contactos"))
        except Exception:
            logging.exception("Error inesperado al actualizar contacto")
            flash("Ocurrió un error interno. Intenta de nuevo más tarde.", "error")
            return render_template("formulario.html", contacto=form_data, modo="editar")

    # GET
    return render_template("formulario.html", contacto=contacto, modo="editar")


@app.route("/contactos/<int:contacto_id>/eliminar", methods=["GET", "POST"])
def eliminar_contacto(contacto_id: int):
    contactos = cargar_contactos()
    contacto = obtener_contacto_por_id(contactos, contacto_id)
    if not contacto:
        flash("Contacto no encontrado.", "error")
        return redirect(url_for("lista_contactos"))

    if request.method == "POST":
        try:
            contactos = [c for c in contactos if c.get("id") != contacto_id]
            guardar_contactos(contactos)
            flash("Contacto eliminado correctamente.", "exito")
            return redirect(url_for("lista_contactos"))
        except Exception:
            logging.exception("Error inesperado al eliminar contacto")
            flash("Ocurrió un error interno. Intenta de nuevo más tarde.", "error")
            return redirect(url_for("lista_contactos"))

    # GET: mostrar página de confirmación
    return render_template("confirmar_eliminar.html", contacto=contacto)


# Manejadores de error genéricos
@app.errorhandler(500)
def error_500(e):
    logging.exception("Error 500 no controlado")
    return render_template("error.html"), 500


@app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html"), 404


if __name__ == "__main__":
    # Ejecutar con: python app.py
    # Luego abrir http://127.0.0.1:5000/contactos
    app.run(debug=False)
