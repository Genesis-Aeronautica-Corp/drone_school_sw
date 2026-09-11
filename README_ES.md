# Paquete de software para Remote Drone School

- [In English](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/README.md)
- [На русском](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/README_RU.md)

## Índice

1. [Primeros pasos](#primeros-pasos)
    - [Estudiante](#estudiante)
    - [Instructor](#instructor)
    - [Desarrollador](#desarrollador)
2. [Cómo usarlo](#cómo-usarlo)
    - [Estudiante](#estudiante-1)
    - [Instructor](#instructor-1)
3. [Código fuente](#código-fuente)

## Primeros pasos

### Estudiante

#### Requisitos del sistema

- 8 GB de RAM
- 1 GB de espacio libre en disco
- CPU Intel Core i3 / Ryzen 3 o superior
- Conexión a Internet estable (la mejor opción es mediante cable Ethernet)
- Versiones de SO compatibles (las que están entre paréntesis no cuentan con soporte oficial, pero se espera que funcionen):
  - Windows 11 (10)
  - Ubuntu 26.04
  - MacOS 26 (15, 14)

#### Descarga e instalación

1. Ve a la sección [Releases](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/releases), haz clic en el botón "Assets" del último release y descarga el instalador de la aplicación `External Frontend` para tu sistema operativo.
2. Instala `External Frontend` siguiendo cuidadosamente las [instrucciones](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/ext_front_user_guide.md).

### Instructor

Si estás leyendo esto, asumimos que nuestro equipo técnico ya preparó una máquina con Ubuntu para ti.

## Cómo usarlo

### Estudiante

1. Espera a que tu instructor prepare una sesión para ti y te lo notifique por tu canal de comunicación (por ejemplo, Telegram o WhatsApp).
2. Abre la aplicación `External Frontend`.
3. Ingresa tu correo electrónico y contraseña en la pantalla `Login to Genesis Aeronautica Network` (deberían haberte sido enviados por tu instructor).
4. Si todo está correcto, verás la pantalla `Connect to Backend`.
    - Si no hay URLs de `Backend` disponibles, contacta a tu instructor. Lo más probable es que aún no haya iniciado su programa.
5. Haz clic en `Connect`.
6. Verás la ventana principal de la aplicación. El instructor te indicará qué hacer a continuación.

### Instructor

Se asume que la parte de hardware (drones, radio, etc.) ya fue configurada.

Necesitarás dos aplicaciones que nuestro equipo técnico debería haber configurado en el escritorio de la máquina de trabajo:

- `Milocus`
- `Invite2Milocus`

1. Abre `Milocus` y configura un vehículo para el estudiante.
2. Cuando el estudiante esté listo, inicia la sesión abriendo `Invite2Milocus`.
3. Es posible que se te pida el correo y la contraseña de la cuenta corporativa del equipo de tierra; en ese caso, ingrésalos.
4. Elige la misión que vas a realizar.
5. Contacta al estudiante e indícale que abra la aplicación `External Frontend` y siga las instrucciones anteriores.
6. Espera hasta que todo se conecte (puede tardar un poco dependiendo de la calidad de la conexión).

## Código fuente

Este repositorio no contiene código fuente y solo sirve como alojamiento de guías y recursos.
