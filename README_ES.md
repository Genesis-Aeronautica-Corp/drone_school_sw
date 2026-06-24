# Software para la Escuela de Drones a Distancia

## Contenido

1. [Primeros pasos](#primeros-pasos)
    - [Estudiante](#estudiante)
    - [Instructor](#instructor)
    - [Desarrollador](#desarrollador)
2. [Modo de uso](#modo-de-uso)
    - [Estudiante](#estudiante-1)
    - [Instructor](#instructor-1)
3. [Código fuente](#código-fuente)

## Primeros pasos

### Estudiante

#### Requisitos del sistema:

- 8 GB de RAM
- Procesador Intel Core i3 / Ryzen 3
- Conexión a Internet estable (la mejor opción es mediante cable Ethernet)
- Sistemas operativos compatibles:
  - Windows 11
  - Ubuntu 24.04 / 26.04
  - MacOS 14 / 15 / 26

#### Descarga e instalación

1. Vaya a [Releases](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/releases), haga clic en el botón «Assets» de la última versión y descargue el paquete para su sistema operativo.
2. Descomprima el archivo (normalmente basta con hacer doble clic en él en el administrador de archivos o seleccionar «Extraer» en el menú contextual) y navegue hasta la carpeta resultante.
3. Dentro encontrará dos archivos: `ClientSessStarter` y el instalador de `External Frontend`.
   - El primero se encarga de incorporar su equipo a nuestra red Tailscale.
     - Se puede ejecutar simplemente haciendo doble clic.
       - Tenga en cuenta que **MacOS** probablemente bloqueará el inicio, ya que aún no disponemos de una cuenta de desarrollador de Apple para una distribución de software fluida (en cualquier caso, MacOS no es nuestra plataforma de nivel 1).
       - Si el archivo se descargó en la carpeta `Downloads` habitual, el comando `xattr -cr ~/Downloads/RDS_Kit_*/ClientSessStarter*` resolverá el problema.
       - Contacte con su instructor si tiene alguna pregunta o problema.
   - El segundo es la aplicación principal con la que trabajará.
4. Instale `External Frontend` siguiendo cuidadosamente las [instrucciones](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/ext_front_user_guide.md).
   - El proceso de instalación no es del todo trivial, así que hágalo con calma y siga exactamente lo que indican las instrucciones. Ante cualquier duda o problema, **contacte con su instructor**.

### Instructor

Si está leyendo esto, asumimos que nuestro equipo técnico ya ha preparado una máquina Ubuntu para usted.

### Desarrollador

El repositorio es bastante simple y directo. Las operaciones principales se pueden realizar mediante `just` (instálelo a través de su gestor de paquetes si aún no lo tiene):

- `just install` — instala las dependencias necesarias para este proyecto.
- `just build` — compila el ejecutable `ClientSessStarter` para su distribución.
- `just run` — ejecuta el binario compilado.
- `python3 InstructorSessStarter.py` — ejecuta el script del instructor.

## Modo de uso

### Estudiante

1. Espere a que su instructor prepare una sesión e informe a través de su canal de comunicación habitual (p. ej., Telegram o WhatsApp).
2. Abra el archivo `ClientSessStarter` haciendo doble clic.
3. Introduzca el correo electrónico y la contraseña de su cuenta (su instructor debería habérselos enviado).
4. En algunos sistemas puede ser necesario introducir su contraseña para acceder a nuestra VPN de Tailscale. Proporciónela si se solicita.
5. Si todo va bien, debería ver un mensaje indicando que se ha conectado a Tailscale. Deje esta ventana abierta; debe permanecer en ejecución durante toda la sesión de vuelo.
    - Si la cierra accidentalmente, simplemente reiníciela, sin problema.
    - Ante cualquier problema, contacte siempre con su instructor; no intente resolverlo por su cuenta.
6. Inicie `External Frontend` y espere a que se conecte a la instancia del instructor.
7. Una vez conectado, se mostrará una ventana con el mapa, la consola de registro y otros elementos. Listo, ya puede trabajar.
    - External Frontend está diseñado de forma que se puede cerrar y volver a abrir sin riesgo en caso de problemas. Hágalo con confianza, pero informe siempre de los incidentes a su instructor para que podamos resolverlos en el futuro.

### Instructor

Se asume que la parte hardware (drones, radio, etc.) ya está configurada.

Necesitará dos aplicaciones que el equipo técnico debería haber instalado en el escritorio de la máquina de trabajo:
  - `InstructorSessStarter`
  - `Milocus`

1. Abra `Milocus` y configure un vehículo para el estudiante.
2. Cuando el estudiante esté listo, inicie la sesión abriendo `InstructorSessStarter`.
3. Si se le solicitan el correo electrónico y la contraseña de la cuenta corporativa del equipo terrestre, introdúzcalos.
4. Seleccione la misión que va a llevar a cabo.
5. Contacte con el estudiante e indíquele que inicie la sesión en su lado ejecutando `ClientSessStarter`.
6. Espere a que todo se conecte (puede tardar un tiempo dependiendo de la calidad de la conexión).

## Código fuente

Este repositorio contiene únicamente scripts de Python para establecer la comunicación entre el estudiante y el instructor. Si necesita el código fuente de `External Frontend`, contacte con su instructor.
