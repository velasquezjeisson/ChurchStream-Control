import obspython as obs
import os
import subprocess
import urllib.request


# ==========================================================
# CHURCHSTREAM CONTROL - AUTO START PARA OBS
# ==========================================================

SERVER_URL = "http://127.0.0.1:8765/"


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
    Inicia init.bat solamente si el servidor no está activo.
    """

    # Si el servidor ya funciona, no hacemos nada
    if server_esta_activo():

        obs.script_log(
            obs.LOG_INFO,
            "[ChurchStream] El servidor ya está ejecutándose."
        )

        return

    # Obtener la ubicación de este script
    script_path = os.path.abspath(__file__)

    # Carpeta /obs
    obs_folder = os.path.dirname(script_path)

    # Carpeta principal del proyecto
    project_folder = os.path.dirname(obs_folder)

    # Ruta de init.bat
    init_bat = os.path.join(project_folder, "init.bat")

    # Verificar que existe
    if not os.path.exists(init_bat):

        obs.script_log(
            obs.LOG_ERROR,
            "[ChurchStream] No se encontró init.bat en: " + init_bat
        )

        return

    try:

        obs.script_log(
            obs.LOG_INFO,
            "[ChurchStream] Iniciando ChurchStream Control..."
        )

        # Ejecutar init.bat
        subprocess.Popen(
            ["cmd.exe", "/c", init_bat],
            cwd=project_folder,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        obs.script_log(
            obs.LOG_INFO,
            "[ChurchStream] init.bat ejecutado correctamente."
        )

    except Exception as error:

        obs.script_log(
            obs.LOG_ERROR,
            "[ChurchStream] Error al iniciar: " + str(error)
        )


def obs_script_load(settings):
    """
    Esta función se ejecuta automáticamente cuando OBS carga el script.
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
        "=============================================="
    )

    # Esperamos unos segundos para que OBS termine de iniciar
    obs.timer_add(iniciar_churchstream, 3000)


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
    Antes de iniciar, comprueba si ChurchStream ya está funcionando
    en el puerto 8765 para evitar iniciar múltiples servidores.
    </p>
    """