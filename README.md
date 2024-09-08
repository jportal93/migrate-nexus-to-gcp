
# Descripción de los Scripts

Este archivo README contiene una descripción sencilla de dos scripts creados para automatizar tareas relacionadas con la descarga y despliegue de artefactos Maven y bibliotecas NPM.

## Script 1: Maven Artifact Downloader and Deployer

### Propósito
Este script está diseñado para descargar artefactos Maven desde un servidor Nexus, modificar los archivos `pom.xml` con información de distribución y desplegar los artefactos en un registro Maven usando Google Cloud para la autenticación.

### Componentes Clave:
- **Descarga de artefactos Maven**: Utiliza `requests` y `BeautifulSoup` para navegar y descargar artefactos desde Nexus.
- **Modificación de `pom.xml`**: Edita los archivos `pom.xml` para incluir un nuevo bloque de `distributionManagement`.
- **Despliegue Maven**: Ejecuta `mvn deploy` usando autenticación con Google Cloud (`gcloud auth`).

### Flujo:
1. Descarga los artefactos desde Nexus.
2. Modifica el archivo `pom.xml` con la información de distribución actualizada.
3. Ejecuta el comando `mvn deploy` para desplegar el artefacto.
4. Elimina los archivos descargados después del despliegue.

---

## Script 2: NPM Library Downloader and Publisher

### Propósito
Este script está diseñado para descargar bibliotecas desde un servidor Nexus y luego publicarlas en un registro NPM. Automatiza el proceso de descarga, publicación y eliminación de archivos descargados.

### Componentes Clave:
- **Descarga de HTML**: Utiliza `wget` para descargar una página HTML que contiene enlaces a versiones de la biblioteca.
- **Extracción de enlaces**: Usa `BeautifulSoup` para extraer los enlaces `<a>` que contienen las URLs de los archivos.
- **Publicación en NPM**: Descarga los archivos y los publica en un registro de NPM usando el comando `npm publish`.

### Flujo:
1. Descarga la página HTML con los enlaces de las versiones de la biblioteca.
2. Extrae los enlaces y descarga las versiones.
3. Publica las bibliotecas descargadas en NPM.
4. Elimina los archivos después de la publicación.

---

## Requisitos para Ambos Scripts

1. **Python 3.x**: Ambos scripts están escritos en Python.
2. **Dependencias de Python**: 
   - `requests`
   - `beautifulsoup4`
   - `subprocess`
   - `os`

   Puedes instalarlas ejecutando:

   ```bash
   pip install requests beautifulsoup4
   ```

3. **Maven y NPM**: 
   - **Maven** es necesario para el primer script, ya que realiza despliegues Maven.
   - **NPM** es necesario para el segundo script para publicar bibliotecas en un registro NPM.
4. **Google Cloud SDK (`gcloud`)**: Es necesario para el primer script, ya que utiliza Google Cloud para autenticarse antes de desplegar los artefactos Maven.

## Ejecución

- Para ejecutar cualquiera de los scripts, asegúrate de que todas las dependencias estén instaladas y que tengas acceso al repositorio Nexus y los registros Maven/NPM correspondientes.
- Ejecuta los scripts desde la línea de comandos:

```bash
cd java
python migrate_java_lib.py  # Para el despliegue Maven

cd node
python transfer_file_node.py  # Para la publicación en NPM
```

Asegúrate de ajustar las rutas y URLs en los scripts según tu entorno y requisitos.

