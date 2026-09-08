import http.server
import json
import os
import socketserver
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import threading

# ============================================================
# ChurchStream Control
# Servidor local + Proxy para OpenLP
# ============================================================


def strip_accents(value):
    """
    Elimina tildes y acentos para facilitar la comparación
    de referencias bíblicas.
    """
    return "".join(
        char
        for char in unicodedata.normalize("NFD", value)
        if unicodedata.category(char) != "Mn"
    )


# ============================================================
# CONFIGURACIÓN
# ============================================================

ROOT = os.path.dirname(os.path.abspath(__file__))

# OpenLP Web API
OPENLP = os.environ.get(
    "OPENLP_URL",
    "http://127.0.0.1:4316"
).rstrip("/")

# Puerto del servidor ChurchStream
PORT = int(os.environ.get("PORT", "8765"))

# Por seguridad se ejecuta localmente.
# Si necesitas acceso desde otro equipo de la red:
# set CHURCHSTREAM_HOST=0.0.0.0
HOST = os.environ.get(
    "CHURCHSTREAM_HOST",
    "127.0.0.1"
)

OPENLP_TIMEOUT = int(
    os.environ.get("OPENLP_TIMEOUT", "5")
)
# ============================================================
# ESTADO DEL OVERLAY
# ============================================================

OVERLAY_STATE = {
    "mode": "hidden",

    "bible": {
        "reference": "",
        "version": "",
        "text": ""
    },

    "lowerThird": {
        "eyebrow": "",
        "title": "",
        "subtitle": ""
    },

    "branding": {
        "organization": "ChurchStream",
        "tagline": "",
        "logo": ""
    }
}
STATE_LOCK = threading.Lock()
# ============================================================
# LIBROS DE LA BIBLIA
# ============================================================
#
# Clave:
# nombre normalizado en español sin tildes
#
# Valores:
# canonical = nombre bonito en español
# english   = nombre utilizado por algunas Biblias/OpenLP
#
# ============================================================

BOOKS = {
    # ANTIGUO TESTAMENTO

    "genesis": {
        "canonical": "Génesis",
        "english": "Genesis"
    },
    "exodo": {
        "canonical": "Éxodo",
        "english": "Exodus"
    },
    "levitico": {
        "canonical": "Levítico",
        "english": "Leviticus"
    },
    "numeros": {
        "canonical": "Números",
        "english": "Numbers"
    },
    "deuteronomio": {
        "canonical": "Deuteronomio",
        "english": "Deuteronomy"
    },
    "josue": {
        "canonical": "Josué",
        "english": "Joshua"
    },
    "jueces": {
        "canonical": "Jueces",
        "english": "Judges"
    },
    "rut": {
        "canonical": "Rut",
        "english": "Ruth"
    },
    "1 samuel": {
        "canonical": "1 Samuel",
        "english": "1 Samuel"
    },
    "2 samuel": {
        "canonical": "2 Samuel",
        "english": "2 Samuel"
    },
    "1 reyes": {
        "canonical": "1 Reyes",
        "english": "1 Kings"
    },
    "2 reyes": {
        "canonical": "2 Reyes",
        "english": "2 Kings"
    },
    "1 cronicas": {
        "canonical": "1 Crónicas",
        "english": "1 Chronicles"
    },
    "2 cronicas": {
        "canonical": "2 Crónicas",
        "english": "2 Chronicles"
    },
    "esdras": {
        "canonical": "Esdras",
        "english": "Ezra"
    },
    "nehemias": {
        "canonical": "Nehemías",
        "english": "Nehemiah"
    },
    "ester": {
        "canonical": "Ester",
        "english": "Esther"
    },
    "job": {
        "canonical": "Job",
        "english": "Job"
    },
    "salmos": {
        "canonical": "Salmos",
        "english": "Psalms"
    },
    "proverbios": {
        "canonical": "Proverbios",
        "english": "Proverbs"
    },
    "eclesiastes": {
        "canonical": "Eclesiastés",
        "english": "Ecclesiastes"
    },
    "cantares": {
        "canonical": "Cantares",
        "english": "Song of Solomon"
    },
    "isaias": {
        "canonical": "Isaías",
        "english": "Isaiah"
    },
    "jeremias": {
        "canonical": "Jeremías",
        "english": "Jeremiah"
    },
    "lamentaciones": {
        "canonical": "Lamentaciones",
        "english": "Lamentations"
    },
    "ezequiel": {
        "canonical": "Ezequiel",
        "english": "Ezekiel"
    },
    "daniel": {
        "canonical": "Daniel",
        "english": "Daniel"
    },
    "oseas": {
        "canonical": "Oseas",
        "english": "Hosea"
    },
    "joel": {
        "canonical": "Joel",
        "english": "Joel"
    },
    "amos": {
        "canonical": "Amós",
        "english": "Amos"
    },
    "abdias": {
        "canonical": "Abdías",
        "english": "Obadiah"
    },
    "jonas": {
        "canonical": "Jonás",
        "english": "Jonah"
    },
    "miqueas": {
        "canonical": "Miqueas",
        "english": "Micah"
    },
    "nahum": {
        "canonical": "Nahúm",
        "english": "Nahum"
    },
    "habacuc": {
        "canonical": "Habacuc",
        "english": "Habakkuk"
    },
    "sofonias": {
        "canonical": "Sofonías",
        "english": "Zephaniah"
    },
    "hageo": {
        "canonical": "Hageo",
        "english": "Haggai"
    },
    "zacarias": {
        "canonical": "Zacarías",
        "english": "Zechariah"
    },
    "malaquias": {
        "canonical": "Malaquías",
        "english": "Malachi"
    },

    # NUEVO TESTAMENTO

    "mateo": {
        "canonical": "Mateo",
        "english": "Matthew"
    },
    "marcos": {
        "canonical": "Marcos",
        "english": "Mark"
    },
    "lucas": {
        "canonical": "Lucas",
        "english": "Luke"
    },
    "juan": {
        "canonical": "Juan",
        "english": "John"
    },
    "hechos": {
        "canonical": "Hechos",
        "english": "Acts"
    },
    "romanos": {
        "canonical": "Romanos",
        "english": "Romans"
    },
    "1 corintios": {
        "canonical": "1 Corintios",
        "english": "1 Corinthians"
    },
    "2 corintios": {
        "canonical": "2 Corintios",
        "english": "2 Corinthians"
    },
    "galatas": {
        "canonical": "Gálatas",
        "english": "Galatians"
    },
    "efesios": {
        "canonical": "Efesios",
        "english": "Ephesians"
    },
    "filipenses": {
        "canonical": "Filipenses",
        "english": "Philippians"
    },
    "colosenses": {
        "canonical": "Colosenses",
        "english": "Colossians"
    },
    "1 tesalonicenses": {
        "canonical": "1 Tesalonicenses",
        "english": "1 Thessalonians"
    },
    "2 tesalonicenses": {
        "canonical": "2 Tesalonicenses",
        "english": "2 Thessalonians"
    },
    "1 timoteo": {
        "canonical": "1 Timoteo",
        "english": "1 Timothy"
    },
    "2 timoteo": {
        "canonical": "2 Timoteo",
        "english": "2 Timothy"
    },
    "tito": {
        "canonical": "Tito",
        "english": "Titus"
    },
    "filemon": {
        "canonical": "Filemón",
        "english": "Philemon"
    },
    "hebreos": {
        "canonical": "Hebreos",
        "english": "Hebrews"
    },
    "santiago": {
        "canonical": "Santiago",
        "english": "James"
    },
    "1 pedro": {
        "canonical": "1 Pedro",
        "english": "1 Peter"
    },
    "2 pedro": {
        "canonical": "2 Pedro",
        "english": "2 Peter"
    },
    "1 juan": {
        "canonical": "1 Juan",
        "english": "1 John"
    },
    "2 juan": {
        "canonical": "2 Juan",
        "english": "2 John"
    },
    "3 juan": {
        "canonical": "3 Juan",
        "english": "3 John"
    },
    "judas": {
        "canonical": "Judas",
        "english": "Jude"
    },
    "apocalipsis": {
        "canonical": "Apocalipsis",
        "english": "Revelation"
    }
}


# ============================================================
# NORMALIZACIÓN DE REFERENCIAS
# ============================================================


def get_book_and_rest(reference):
    """
    Detecta el libro bíblico dentro de una referencia.

    Ejemplos:
        Juan 3:16
        Génesis 1:1
        1 Corintios 13:4
        Genesis 1:1
    """

    original = reference.strip()
    normalized = strip_accents(original.lower())

    # Los nombres largos deben evaluarse primero.
    for book in sorted(BOOKS.keys(), key=len, reverse=True):

        if normalized == book:
            return book, ""

        if normalized.startswith(book + " "):
            rest = original[len(book):].strip()
            return book, rest

    return None, None


def build_reference_candidates(reference):
    """
    Construye diferentes variantes de una referencia para
    aumentar la compatibilidad con diferentes Biblias de OpenLP.

    Ejemplo:

        "Genesis 1:1"

    puede probar:

        Genesis 1:1
        Génesis 1:1

    y una referencia en español puede probar también
    su equivalente en inglés.
    """

    reference = reference.strip()

    if not reference:
        return []

    candidates = []

    def add(value):
        value = value.strip()

        if not value:
            return

        normalized = value.lower()

        if normalized not in {
            item.lower() for item in candidates
        }:
            candidates.append(value)

    # 1. Referencia exactamente como fue escrita.
    add(reference)

    # 2. Referencia sin tildes.
    add(strip_accents(reference))

    book, rest = get_book_and_rest(reference)

    if book and book in BOOKS:

        data = BOOKS[book]

        suffix = f" {rest}" if rest else ""

        # 3. Nombre canónico en español.
        add(data["canonical"] + suffix)

        # 4. Nombre en inglés.
        add(data["english"] + suffix)

    return candidates


# ============================================================
# CONEXIÓN HTTP
# ============================================================


def opener():
    """
    Crea un opener sin proxy del sistema.

    Esto evita problemas en algunos equipos donde localhost
    intenta pasar por un proxy corporativo o configurado en Windows.
    """

    return urllib.request.build_opener(
        urllib.request.ProxyHandler({})
    )


# ============================================================
# SERVIDOR HTTP
# ============================================================


class ChurchStreamHandler(
    http.server.SimpleHTTPRequestHandler
):

    # --------------------------------------------------------
    # ARCHIVOS ESTÁTICOS
    # --------------------------------------------------------

    def translate_path(self, path):

        parsed = urllib.parse.urlparse(path)
        path = parsed.path

        if path in ("", "/"):
            path = "/controller.html"

        # Evitar traversal fuera de la carpeta del proyecto.
        path = urllib.parse.unquote(path)

        parts = [
            part
            for part in path.split("/")
            if part not in ("", ".", "..")
        ]

        return os.path.join(
            ROOT,
            *parts
        )

    # --------------------------------------------------------
    # RESPUESTAS JSON
    # --------------------------------------------------------

    def send_json(self, status, obj):

        raw = json.dumps(
            obj,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.end_headers()

        self.wfile.write(raw)

    # --------------------------------------------------------
    # RESPUESTAS BINARIAS
    # --------------------------------------------------------

    def send_bytes(
        self,
        status,
        raw,
        content_type="application/json; charset=utf-8"
    ):

        self.send_response(status)

        self.send_header(
            "Content-Type",
            content_type
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.end_headers()

        self.wfile.write(raw)

    # --------------------------------------------------------
    # PROXY CAPTURE
    # --------------------------------------------------------

    def proxy_capture(
        self,
        method,
        suffix,
        query="",
        body=None
    ):

        target = (
            OPENLP
            + "/"
            + suffix
            + (("?" + query) if query else "")
        )

        data = None

        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "ChurchStream-Control/1.0"
        }

        if body is not None:

            data = json.dumps(
                body,
                ensure_ascii=False
            ).encode("utf-8")

            headers[
                "Content-Type"
            ] = "application/json; charset=utf-8"

        try:

            request = urllib.request.Request(
                target,
                data=data,
                headers=headers,
                method=method
            )

            with opener().open(
                request,
                timeout=OPENLP_TIMEOUT
            ) as response:

                return response.read()

        except Exception:

            return None

    # --------------------------------------------------------
    # PROXY OPENLP
    # --------------------------------------------------------

    def proxy(
        self,
        method,
        suffix,
        query="",
        body=None
    ):

        target = (
            OPENLP
            + "/"
            + suffix
            + (("?" + query) if query else "")
        )

        data = None

        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "ChurchStream-Control/1.0"
        }

        if body is not None:

            data = json.dumps(
                body,
                ensure_ascii=False
            ).encode("utf-8")

            headers[
                "Content-Type"
            ] = "application/json; charset=utf-8"

        try:

            request = urllib.request.Request(
                target,
                data=data,
                headers=headers,
                method=method
            )

            with opener().open(
                request,
                timeout=OPENLP_TIMEOUT
            ) as response:

                response_bytes = response.read()

                self.send_response(response.status)

                self.send_header(
                    "Content-Type",
                    response.headers.get(
                        "Content-Type",
                        "application/json"
                    )
                )

                self.send_header(
                    "Access-Control-Allow-Origin",
                    "*"
                )

                self.send_header(
                    "Cache-Control",
                    "no-store"
                )

                self.end_headers()

                if response_bytes:
                    self.wfile.write(response_bytes)

        except urllib.error.HTTPError as error:

            detail = error.read().decode(
                "utf-8",
                "replace"
            )

            self.send_json(
                error.code,
                {
                    "error":
                        f"OpenLP HTTP {error.code}",
                    "detail":
                        detail
                }
            )

        except Exception as error:

            self.send_json(
                502,
                {
                    "error":
                        "No se pudo conectar con OpenLP",
                    "openlp":
                        OPENLP,
                    "detail":
                        str(error)
                }
            )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def do_GET(self):

        parsed = urllib.parse.urlparse(
            self.path
        )
        # ====================================================
        # ESTADO ACTUAL DEL OVERLAY
        # ====================================================

        if parsed.path == "/api/state":

            with STATE_LOCK:

                state = json.loads(
                    json.dumps(
                        OVERLAY_STATE
                    )
                )

            self.send_json(
                200,
                state
            )

            return  

        # ====================================================
        # PROXY OPENLP
        # ====================================================

        if parsed.path.startswith("/openlp/"):

            suffix = parsed.path[
                len("/openlp/"):
            ]

            query = parsed.query

            # =================================================
            # BÚSQUEDA BÍBLICA INTELIGENTE
            # =================================================

            if suffix == (
                "api/v2/plugins/bibles/search"
            ):

                params = urllib.parse.parse_qs(
                    query,
                    keep_blank_values=True
                )

                original = params.get(
                    "text",
                    [""]
                )[0]

                if original:

                    candidates = (
                        build_reference_candidates(
                            original
                        )
                    )

                    last_query = query
                    last_result = None

                    for reference in candidates:

                        params["text"] = [reference]

                        candidate_query = (
                            urllib.parse.urlencode(
                                params,
                                doseq=True
                            )
                        )

                        last_query = candidate_query

                        result = self.proxy_capture(
                            "GET",
                            suffix,
                            candidate_query
                        )

                        if result is None:
                            continue

                        last_result = result

                        try:

                            data = json.loads(
                                result.decode("utf-8")
                            )

                        except Exception:

                            data = None

                        # Una lista con resultados
                        # significa búsqueda exitosa.
                        if (
                            isinstance(data, list)
                            and len(data) > 0
                        ):

                            self.send_bytes(
                                200,
                                result
                            )

                            return

                    # Si OpenLP respondió pero ninguna
                    # variante encontró resultados,
                    # devolvemos la última respuesta.
                    if last_result is not None:

                        self.send_bytes(
                            200,
                            last_result
                        )

                        return

                    # Intento final para devolver
                    # el error original de OpenLP.
                    self.proxy(
                        "GET",
                        suffix,
                        last_query
                    )

                    return

            # =================================================
            # CUALQUIER OTRO ENDPOINT DE OPENLP
            # =================================================

            self.proxy(
                "GET",
                suffix,
                query
            )

            return

        # ====================================================
        # ARCHIVOS LOCALES
        # ====================================================

        super().do_GET()

    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    def do_POST(self):

        parsed = urllib.parse.urlparse(
            self.path
        )

        # ====================================================
        # ACTUALIZAR ESTADO DEL OVERLAY
        # ====================================================

        if parsed.path == "/api/state":

            global OVERLAY_STATE

            length = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

            raw = (
                self.rfile.read(length)
                if length
                else b""
            )

            try:

                data = (
                    json.loads(
                        raw.decode("utf-8")
                    )
                    if raw
                    else {}
                )

            except Exception:

                self.send_json(
                    400,
                    {"error": "JSON inválido"}
                )

                return


            with STATE_LOCK:

                if "mode" in data:

                    OVERLAY_STATE["mode"] = data["mode"]


                if "bible" in data:

                    OVERLAY_STATE["bible"].update(
                        data["bible"]
                    )


                if "lowerThird" in data:

                    OVERLAY_STATE["lowerThird"].update(
                        data["lowerThird"]
                    )


                if "branding" in data:

                    OVERLAY_STATE["branding"].update(
                        data["branding"]
                    )


                state = json.loads(
                    json.dumps(
                        OVERLAY_STATE
                    )
                )


            self.send_json(
                200,
                {
                    "ok": True,
                    "state": state
                }
            )

            return
        if parsed.path.startswith("/openlp/"):

            suffix = parsed.path[
                len("/openlp/"):
            ]

            length = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

            raw = (
                self.rfile.read(length)
                if length
                else b""
            )

            try:

                body = (
                    json.loads(
                        raw.decode("utf-8")
                    )
                    if raw
                    else None
                )

            except Exception:

                self.send_json(
                    400,
                    {
                        "error": "JSON inválido"
                    }
                )

                return

            self.proxy(
                "POST",
                suffix,
                parsed.query,
                body
            )

            return

        self.send_error(404)


# ============================================================
# SERVIDOR REUTILIZABLE
# ============================================================


class ChurchStreamServer(
    socketserver.ThreadingTCPServer
):

    allow_reuse_address = True


# ============================================================
# INICIO
# ============================================================


if __name__ == "__main__":

    print()
    print("=" * 58)
    print("              CHURCHSTREAM CONTROL")
    print("=" * 58)
    print()
    print("Servidor iniciado correctamente.")
    print()
    print(f"Control:")
    print(f"http://{HOST}:{PORT}/")
    print()
    print("Overlay:")
    print(f"http://{HOST}:{PORT}/overlay.html")
    print()
    print("OpenLP:")
    print(OPENLP)
    print()
    print("Mantén esta ventana abierta mientras utilizas")
    print("ChurchStream Control.")
    print()
    print("Presiona Ctrl+C para detener el servidor.")
    print("=" * 58)
    print()

    try:

        with ChurchStreamServer(
            (HOST, PORT),
            ChurchStreamHandler
        ) as server:

            server.serve_forever()

    except KeyboardInterrupt:

        print()
        print("ChurchStream Control detenido.")

    except OSError as error:

        print()
        print("ERROR AL INICIAR EL SERVIDOR")
        print("-" * 58)
        print(str(error))
        print()
        print(
            f"Verifica que el puerto {PORT} "
            "no esté siendo utilizado."
        )