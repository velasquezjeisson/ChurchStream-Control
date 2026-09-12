import obspython as obs
import os
import subprocess
import urllib.request


# ==========================================================
# CHURCHSTREAM CONTROL - AUTO START PARA OBS
# ==========================================================

SERVER_URL = "http://127.0.0.1:8765/"
INICIADO = False


def server_esta_activo():
    """
    Comprueba si ChurchStream Control ya está ejecutándose.
    """

    try:
        urllib.request.urlopen(SERVER_URL, timeout=2)
        return True

    except Exception:
        return False


def iniciar_churchstream():
    """
    Inicia ChurchStream Control una sola vez.
    """

    global INICIADO

    # Evitar ejecuciones múltiples
    if INICIADO:
        return

    INICIADO = True

    # Eliminar el temporizador después de ejecutarse
    obs.timer_remove(iniciar_churchstream)

    obs.script_log(
        obs.LOG_INFO,
        "[ChurchStream] Verificando servidor..."
    )

    # Si ya está funcionando, no hacer nada
    if server_esta_activo():

        obs.script_log(
            obs.LOG_INFO,
            "[ChurchStream] ChurchStream Control ya está ejecutándose."
        )

        return

    # ======================================================
    # UBICACIÓN DEL SCRIPT
    # ======================================================

    script_path = os.path.abspath(__file__)

    obs.script_log(
        obs.LOG_INFO,
        "[ChurchStream] Script ubicado en: " + script_path
    )

    # Carpeta donde está este script
    # Ejemplo:
    # D:\OBS\ChurchStream-Control\obs\
    obs_folder = os.path.dirname(script_path)

    # Carpeta principal del proyecto
    # Ejemplo:
    # D:\OBS\ChurchStream-Control\
    project_folder = os.path.dirname(obs_folder)

    # Ruta de init.bat
    # Ruta de init.vbs
    init_vbs = os.path.join(project_folder, "init.vbs")

    obs.script_log(
        obs.LOG_INFO,
        "[ChurchStream] Buscando init_vbs en: " + init_vbs
    )

    # ======================================================
    # VERIFICAR INIT.BAT
    # ======================================================

    if not os.path.exists(init_vbs):

        obs.script_log(
            obs.LOG_ERROR,
            "[ChurchStream] ERROR: No se encontró init.vbs."
        )

        return

    # ======================================================
    # INICIAR CHURCHSTREAM
    # ======================================================

    try:

        obs.script_log(
            obs.LOG_INFO,
            "[ChurchStream] Iniciando ChurchStream Control..."
        )

        subprocess.Popen(
            ["wscript.exe", init_vbs],
            cwd=project_folder,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        obs.script_log(
            obs.LOG_INFO,
            "[ChurchStream] init.bat ejecutado correctamente."
        )

    except Exception as error:

        obs.script_log(
            obs.LOG_ERROR,
            "[ChurchStream] ERROR al iniciar: " + str(error)
        )


# ==========================================================
# OBS SCRIPT LOAD
# ==========================================================

def script_load(settings):
    """
    Se ejecuta automáticamente cuando OBS carga el script.
    """

    obs.script_log(
        obs.LOG_INFO,
        "=============================================="
    )

    obs.script_log(
        obs.LOG_INFO,
        "ChurchStream Control - AutoStart cargado"
    )

    obs.script_log(
        obs.LOG_INFO,
        "Esperando 3 segundos para iniciar..."
    )

    obs.script_log(
        obs.LOG_INFO,
        "=============================================="
    )

    # Esperar 3 segundos para que OBS termine de iniciar
    obs.timer_add(iniciar_churchstream, 2000)


# ==========================================================
# DESCRIPCIÓN DEL SCRIPT
# ==========================================================

def script_description():

    return """
    <h2>ChurchStream Control - AutoStart</h2>

    <p>
    Inicia automáticamente ChurchStream Control cuando OBS abre.
    </p>

    <p>
    El script busca el archivo <b>init.bat</b> en la carpeta
    principal del proyecto.
    </p>

    <p>
    Antes de iniciar, comprueba si ChurchStream Control ya está
    funcionando en el puerto 8765 para evitar iniciar múltiples
    servidores.
    </p>
    """