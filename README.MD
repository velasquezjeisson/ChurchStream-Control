# 🎥 ChurchStream Control

### Control local para transmisiones en vivo con OBS + OpenLP

**ChurchStream Control** es una herramienta local diseñada para facilitar la operación de transmisiones de iglesias y organizaciones.

Permite controlar desde una interfaz web:

- 📖 Pasajes bíblicos conectados a OpenLP.
- 🎬 Lower Thirds personalizables.
- 💾 Presets para guardar títulos frecuentes.
- 🖼️ Logo personalizado de la iglesia u organización.
- ⚙️ Configuración de identidad institucional.
- 🖥️ Un único Overlay para OBS.
- 🚫 Ocultar todos los elementos rápidamente.

El sistema funciona completamente de forma local y está pensado para ser sencillo de instalar y utilizar durante una transmisión.

---

# ✨ Características

## 📖 Biblia integrada con OpenLP

ChurchStream Control se conecta con la API de **OpenLP** para buscar y mostrar pasajes bíblicos.

Características:

- Selección de la versión bíblica activa.
- Búsqueda de referencias bíblicas.
- Compatibilidad con nombres de libros en español.
- Búsqueda tolerante con y sin tildes.
- Compatibilidad con equivalencias en inglés cuando OpenLP utiliza nombres diferentes.
- Lista de sugerencias con los **66 libros de la Biblia**.
- Vista previa del pasaje antes de mostrarlo.
- Mostrar y ocultar rápidamente desde el controlador.

Ejemplos:

```text
Juan 3:16
Génesis 1:1
Isaías 53:5
1 Corintios 13:4-7
```

El sistema intenta automáticamente diferentes variantes de la referencia para mejorar la compatibilidad con las diferentes Biblias instaladas en OpenLP.

---

# 🎬 Lower Third

El sistema incluye un Lower Third personalizable para mostrar información durante la transmisión.

Puedes configurar:

- **Sección / Etiqueta**
- **Título**
- **Subtítulo**

Ejemplo:

```text
SECCIÓN:
IGLESIA CENTRAL

TÍTULO:
ADORACIÓN Y ALABANZA

SUBTÍTULO:
Un tiempo para exaltar a Dios
```

---

# 💾 Presets

Puedes guardar configuraciones frecuentes del Lower Third.

Por ejemplo:

- Adoración y Alabanza
- Momento Infantil
- Santa Cena
- Predicación
- Oración
- Bienvenida
- Anuncios

Cada preset guarda:

```text
✓ Sección
✓ Título
✓ Subtítulo
```

Al seleccionar un preset, la información se carga nuevamente en el formulario y puede modificarse antes de enviarla al Overlay.

Los presets se almacenan localmente en el navegador.

---

# 🏛️ Identidad de la organización

ChurchStream Control permite personalizar la identidad visual de cada iglesia u organización.

Desde la sección **Configuración** puedes definir:

### Nombre de la organización

Ejemplo:

```text
Iglesia Oasis
```

### Lema o subtítulo institucional

Ejemplo:

```text
Un corazón para Su presencia
```

### Logo

Puedes cargar el logo de tu iglesia u organización.

La configuración se guarda localmente en el navegador.

Esto permite que el proyecto sea reutilizable por diferentes iglesias sin modificar el código.

---

# 🖥️ Un único Overlay para OBS

ChurchStream Control utiliza un único archivo:

```text
overlay.html
```

Este Overlay recibe la información enviada desde el controlador y muestra:

- 📖 Pasajes bíblicos.
- 🎬 Lower Thirds.

---

# 🧱 Arquitectura

```text
ChurchStream-Control/
│
├── controller.html
├── overlay.html
├── server.py
├── README.md
│
└── ...
```

### `controller.html`

Interfaz utilizada por el operador.

Desde aquí se controla:

- Biblia.
- OpenLP.
- Lower Third.
- Presets.
- Configuración institucional.

### `overlay.html`

Es el archivo utilizado por OBS.

Recibe la información enviada por el controlador y muestra los gráficos en pantalla.

### `server.py`

Servidor local de ChurchStream Control.

Sus funciones principales son:

- Servir los archivos HTML localmente.
- Crear una conexión local con OpenLP.
- Actuar como proxy para la API de OpenLP.
- Mejorar la compatibilidad con referencias bíblicas.
- Evitar problemas de CORS entre el navegador y OpenLP.

---

# 📋 Requisitos

Antes de utilizar ChurchStream Control debes tener instalado:

- 🐍 **Python 3**
- 🖥️ **OBS Studio**
- 📖 **OpenLP**
- 🌐 Un navegador moderno para las configuraciones iniciales

> ⚠️ **Importante:** ChurchStream Control no incluye OBS Studio, OpenLP ni traducciones bíblicas. Estos componentes deben instalarse y configurarse por separado.

---

# 🖥️ OBS Studio

OBS Studio es necesario para utilizar ChurchStream Control durante la transmisión.

ChurchStream Control utiliza OBS para:

- 🎛️ Ejecutar el **Controlador** como un Panel/Dock de navegador personalizado.
- 🖥️ Mostrar `overlay.html` mediante una **Browser Source / Fuente de navegador**.

Puedes descargar OBS Studio desde su sitio oficial:

https://obsproject.com/

---

# 📖 OpenLP

OpenLP es necesario para utilizar la búsqueda y visualización de pasajes bíblicos.

ChurchStream Control se conecta localmente con la API de OpenLP, pero **no incluye OpenLP ni sus Biblias**.

Debes descargar e instalar OpenLP por separado desde su sitio oficial:

https://openlp.org/

Una vez instalado:

1. Abre OpenLP.
2. Instala o importa las versiones bíblicas que deseas utilizar.
3. Verifica que la API/Web Remote de OpenLP esté disponible.
4. Mantén OpenLP ejecutándose mientras utilizas ChurchStream Control.

---

# 🚀 Instalación

## 1. Instalar Python

ChurchStream Control requiere **Python 3**.

Puedes verificar la instalación ejecutando:

```bash
python --version
```

o:

```bash
py --version
```

---

## 2. Descargar el proyecto

Clona el repositorio:

```bash
git clone https://github.com/TU-USUARIO/ChurchStream-Control.git
```

Luego entra en la carpeta:

```bash
cd ChurchStream-Control
```

También puedes descargar el proyecto como archivo ZIP desde GitHub.

---

# ▶️ Ejecutar ChurchStream Control

Desde la carpeta del proyecto ejecuta:

```bash
python server.py
```

En Windows también puede funcionar:

```bash
py server.py
```

El servidor mostrará una salida similar a:

```text
==========================================================
              CHURCHSTREAM CONTROL
==========================================================

Servidor iniciado correctamente.

Control:
http://127.0.0.1:8765/

Overlay:
http://127.0.0.1:8765/overlay.html

OpenLP:
http://127.0.0.1:4316
```

---

# 🎛️ Controlador: uso recomendado dentro de OBS

> ⚠️ **Importante:** ChurchStream Control está diseñado para utilizarse como un **panel integrado (Dock/Panel) dentro de OBS**.

Aunque puedes abrir el controlador en un navegador mediante:

```text
http://127.0.0.1:8765/
```

se recomienda **no controlar la transmisión desde una ventana normal del navegador**.

La comunicación utilizada entre el controlador y el Overlay se realiza mediante el contexto del navegador integrado. Por esta razón, al utilizar el controlador desde una ventana externa del navegador, puede ocurrir que los comandos se reflejen únicamente en un Overlay abierto en ese mismo navegador y **no en el Browser Source utilizado por OBS**.

## Configurar ChurchStream Control como panel dentro de OBS

En OBS:

1. Abre el menú **Paneles / Docks**.
2. Selecciona **Custom Browser Docks / Paneles del navegador personalizados** (el nombre puede variar según el idioma de OBS).
3. Crea un nuevo panel.
4. Asigna un nombre, por ejemplo:

```text
ChurchStream Control
```

5. Utiliza esta URL:

```text
http://127.0.0.1:8765/
```

6. Guarda la configuración.

A partir de ese momento, controla:

- 📖 Biblia
- 🎬 Lower Third
- 💾 Presets
- ⚙️ Configuración

**directamente desde el panel integrado dentro de OBS**.

Esto asegura que los comandos enviados al Overlay funcionen correctamente durante la transmisión.

---

# 🖥️ Configuración en OBS

En OBS agrega una nueva fuente:

### Browser Source / Fuente de navegador

Utiliza la siguiente URL:

```text
http://127.0.0.1:8765/overlay.html
```

Configuración recomendada:

```text
Ancho:  1920
Alto:   1080
```

El fondo del Overlay es transparente.

---

# 📺 Configuración recomendada de OBS

```text
Escena
│
├── Cámara
├── Presentación / Video
├── Otros elementos
│
└── ChurchStream Overlay
```

El Browser Source de ChurchStream debe estar por encima de los elementos sobre los cuales quieres mostrar los gráficos.

---

# 📖 Configuración de OpenLP

ChurchStream Control requiere que:

1. OpenLP esté instalado.
2. OpenLP esté ejecutándose.
3. La API Web de OpenLP esté habilitada.
4. Tengas al menos una Biblia instalada en OpenLP.

Por defecto, ChurchStream Control intenta conectarse a:

```text
http://127.0.0.1:4316
```

---

# 🔎 Búsqueda bíblica inteligente

Las referencias son procesadas de forma tolerante para mejorar la compatibilidad entre diferentes versiones de Biblias instaladas en OpenLP.

Por ejemplo:

```text
Génesis 1:1
```

Puede probar variantes como:

```text
Génesis 1:1
Genesis 1:1
```

También se manejan nombres con y sin tildes:

```text
Éxodo / Exodo
Isaías / Isaias
```

Esto ayuda especialmente cuando una Biblia importada utiliza nombres de libros diferentes.

---

# ⚙️ Configuración avanzada

Por defecto, ChurchStream Control utiliza:

```text
Servidor ChurchStream:
127.0.0.1:8765

OpenLP:
127.0.0.1:4316
```

El servidor también permite configurar estos valores mediante variables de entorno:

```text
OPENLP_URL
PORT
CHURCHSTREAM_HOST
OPENLP_TIMEOUT
```

---

# 🔒 Funcionamiento local

Por defecto, ChurchStream Control funciona únicamente en:

```text
127.0.0.1
```

Esto significa que el sistema está pensado para ejecutarse localmente en el computador que controla la transmisión.

No requiere:

- Internet.
- Servidores externos.
- Cuentas.
- Suscripciones.

Una vez instalado, el sistema puede funcionar completamente dentro del computador de transmisión.

---

# 🎯 Flujo de trabajo recomendado

Durante una transmisión:

### 1️⃣ Abrir OpenLP

Inicia OpenLP y asegúrate de que las Biblias estén disponibles.

### 2️⃣ Ejecutar ChurchStream Control

```bash
python server.py
```

### 3️⃣ Configurar ChurchStream Control como panel dentro de OBS

En OBS, agrega ChurchStream Control desde:

**Paneles / Docks → Panel del navegador personalizado**

Utiliza:

```text
http://127.0.0.1:8765/
```

> ⚠️ Se recomienda controlar ChurchStream desde este panel integrado en OBS y no desde una ventana externa del navegador.

### 4️⃣ Configurar el Overlay en OBS

Verifica que la fuente Browser Source esté configurada con:

```text
http://127.0.0.1:8765/overlay.html
```

### 5️⃣ Configurar la identidad

En la pestaña **Configuración**:

- Escribe el nombre de la iglesia.
- Agrega el lema.
- Carga el logo.

### 6️⃣ Crear tus presets

Guarda los títulos que utilizas frecuentemente.

### 7️⃣ Controlar la transmisión

Utiliza:

- 📖 **Biblia**
- 🎬 **Lower Third**
- 🚫 **Ocultar Todo**

---

# 🛠️ Solución de problemas

## ❌ OpenLP no disponible

Verifica:

- Que OpenLP esté abierto.
- Que su API Web esté habilitada.
- Que OpenLP esté utilizando el puerto correcto.

Por defecto:

```text
http://127.0.0.1:4316
```

---

## ❌ No aparece el Overlay en OBS

Verifica que la URL sea:

```text
http://127.0.0.1:8765/overlay.html
```

También verifica que:

- `server.py` esté ejecutándose.
- La fuente Browser Source esté visible.
- La fuente esté ubicada correctamente en la escena.

---

## ❌ El logo no aparece

Recuerda que la configuración visual se guarda localmente en el navegador.

Después de cargar un logo:

1. Guarda la configuración.
2. Envía la configuración al Overlay.
3. Verifica que el Overlay esté abierto desde el servidor local.

---

# 🤝 Contribuciones

Las contribuciones son bienvenidas.

Puedes ayudar mediante:

- Reportes de errores.
- Nuevas funcionalidades.
- Mejoras de diseño.
- Compatibilidad con otros sistemas bíblicos.
- Nuevos estilos de Lower Third.
- Mejoras para OBS.
- Traducciones.

Para contribuir:

1. Haz un **Fork** del proyecto.
2. Crea una nueva rama.
3. Realiza tus cambios.
4. Envía un **Pull Request**.

---

# 💡 Próximas mejoras

- [ ] Múltiples diseños de Lower Third.
- [ ] Selector de temas visuales.
- [ ] Animaciones configurables.
- [ ] Más tipos de gráficos.
- [ ] Fondos para anuncios.
- [ ] Sistema de slides.
- [ ] Reloj y temporizador.
- [ ] Cuenta regresiva.
- [ ] Modo multimonitor.
- [ ] Control desde dispositivos de la red local.
- [ ] Perfiles de organizaciones.
- [ ] Exportar e importar presets.
- [ ] Backup de configuración.
- [ ] Integración más profunda con OBS.

---

# ❤️ Propósito del proyecto

ChurchStream Control nació con el objetivo de simplificar el manejo técnico de las transmisiones de iglesias y organizaciones.

La idea es ofrecer una herramienta:

```text
✓ Simple
✓ Gratuita
✓ Local
✓ Personalizable
✓ Compatible con OBS
✓ Compatible con OpenLP
```

para que los equipos de producción puedan concentrarse más en la transmisión y menos en la complejidad técnica.

---

# ⚖️ Software de terceros y licencias

ChurchStream Control se integra con aplicaciones independientes desarrolladas y distribuidas por sus respectivos proyectos.

## 📖 OpenLP

OpenLP es un proyecto independiente de software libre utilizado para la gestión y presentación de contenido de culto, incluyendo la búsqueda y proyección de pasajes bíblicos.

- Sitio oficial: https://openlp.org/
- Licencia: **GNU General Public License v3.0 o posterior (GPL-3.0-or-later)**

ChurchStream Control **no incluye, redistribuye ni modifica OpenLP**. La instalación y el uso de OpenLP están sujetos a sus propios términos y licencia.

ChurchStream Control no está afiliado oficialmente con el proyecto OpenLP.

## 🖥️ OBS Studio

OBS Studio es un proyecto independiente utilizado para producción, grabación y transmisión audiovisual.

- Sitio oficial: https://obsproject.com/
- Licencia: **GNU General Public License v2.0 o posterior (GPL-2.0-or-later)**

ChurchStream Control utiliza funciones de OBS como los Browser Docks y Browser Sources, pero no incluye ni redistribuye OBS Studio.

ChurchStream Control no está afiliado oficialmente con OBS Studio.

## 📚 Traducciones bíblicas

Las traducciones bíblicas utilizadas mediante OpenLP pueden estar sujetas a:

- Derechos de autor.
- Licencias específicas.
- Condiciones de uso.
- Restricciones para proyección, transmisión o redistribución.

**ChurchStream Control no distribuye traducciones bíblicas.**

Es responsabilidad del usuario verificar que cuenta con los permisos, licencias o autorizaciones necesarios para utilizar las traducciones bíblicas durante servicios, proyecciones o transmisiones.

---

# 📄 Licencia de ChurchStream Control

ChurchStream Control se distribuye como software de código abierto bajo la **MIT License**.

Esta licencia permite utilizar, copiar, modificar, distribuir y adaptar el código, siempre que se conserve el aviso de copyright y la licencia correspondiente.

La licencia MIT aplica únicamente al código y archivos propios de ChurchStream Control.

Las aplicaciones y contenidos de terceros utilizados junto con el proyecto, incluyendo **OpenLP**, **OBS Studio** y las **traducciones bíblicas**, conservan sus propias licencias, derechos de autor y condiciones de uso.

Consulta el archivo `LICENSE` incluido en este repositorio para conocer el texto completo de la licencia de ChurchStream Control.

---

# 🎥 ChurchStream Control

**Control local para OBS, OpenLP y gráficos en transmisión.**

Hecho para servir a iglesias y organizaciones que desean mejorar sus transmisiones con herramientas simples y accesibles. ❤️
