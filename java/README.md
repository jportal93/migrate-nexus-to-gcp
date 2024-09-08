
# Maven Artifact Downloader and Deployer

Este script en Python se utiliza para descargar artefactos Maven de un servidor Nexus, actualizar archivos `pom.xml` con nueva información de gestión de distribución, y realizar despliegues Maven en Google Cloud mediante la autenticación con `gcloud`. El script también incluye un sistema recursivo para navegar por directorios, descargar archivos y realizar despliegues automáticos.

## Requisitos

1. **Python 3.x**
2. **Bibliotecas de Python**:
   - `requests`
   - `beautifulsoup4`
   - `subprocess`
   - `os`
   - `urllib`
   - `shutil`
   - `xml.etree.ElementTree`
   
   Puedes instalarlas ejecutando:

   ```bash
   pip install requests beautifulsoup4
   ```

3. **Maven**: Para realizar los despliegues Maven.
4. **Google Cloud SDK (`gcloud`)**: Para autenticar y obtener un token de acceso para Maven.

## Configuración

Asegúrate de configurar las siguientes variables en el script:

- `base_url`: La URL base de tu repositorio Nexus.
  ```python
  base_url = 'https://nexus.gg.com/service/rest/repository/browse/maven-public/com/repos/cl/'
  ```

- `base_dir`: El directorio base en tu sistema de archivos donde se almacenarán los artefactos descargados.
  ```python
  base_dir = './java'
  ```

## Funciones principales

### 1. `get_directories_and_files(url)`

Esta función toma una URL de un directorio Nexus y devuelve una lista de subdirectorios y archivos en el directorio.

- **Parámetros**: 
  - `url`: URL del directorio en Nexus.
- **Devuelve**: 
  - Listas de directorios y archivos.

### 2. `download_file(url, path)`

Descarga un archivo desde una URL dada y lo guarda en una ruta específica en tu sistema de archivos.

- **Parámetros**:
  - `url`: URL del archivo a descargar.
  - `path`: Directorio donde se guardará el archivo.

### 3. `update_distribution_management(pom_path, new_dist_management_xml)`

Actualiza la sección `distributionManagement` en un archivo `pom.xml` con un nuevo bloque de XML.

- **Parámetros**:
  - `pom_path`: Ruta al archivo `pom.xml`.
  - `new_dist_management_xml`: XML de la nueva sección de `distributionManagement`.

### 4. `maven_push(dir)`

Realiza un despliegue Maven (`mvn deploy`) autenticándose con Google Cloud.

- **Parámetros**:
  - `dir`: Directorio donde se encuentra el proyecto Maven que se va a desplegar.

### 5. `check_and_run_maven_push(file_path)`

Verifica si existe un archivo `pom.xml` en el directorio dado. Si existe, llama a `maven_push`. Después, intenta eliminar el directorio.

- **Parámetros**:
  - `file_path`: Ruta al directorio que contiene el `pom.xml`.

### 6. `process_artifact_versions(base_url, artifact, base_dir)`

Navega recursivamente por las versiones de un artefacto en Nexus, descarga los archivos correspondientes y realiza el despliegue Maven si hay un `pom.xml`.

- **Parámetros**:
  - `base_url`: URL base del repositorio.
  - `artifact`: Nombre del artefacto.
  - `base_dir`: Directorio base local donde se almacenarán las versiones.

## Ejecución

Para ejecutar el script, simplemente asegúrate de que todas las dependencias estén instaladas y ejecuta el script desde la línea de comandos:

```bash
python script.py
```

El script se conectará al repositorio de Nexus, descargará los artefactos correspondientes, actualizará los archivos `pom.xml` y realizará el despliegue Maven.

## Ejemplo

Supongamos que tienes un repositorio Maven en Nexus con la siguiente estructura:

```
com/repos/cl/
 ├── library-ig-core/
 ├── library-ig-db-mongo/
     ├── c053d052-SNAPSHOT/
         ├── maven-metadata.xml
         ├── ...other files...
```

El script:

1. Navegará a `com/repos/cl/`.
2. Descargará las versiones SNAPSHOT de los artefactos en `library-ig-core` y `library-ig-db-mongo`.
3. Actualizará el archivo `pom.xml` en cada uno de los artefactos descargados.
4. Realizará el despliegue Maven usando Google Cloud para autenticación.
5. Finalmente, eliminará el directorio local que contiene los artefactos descargados.

## Notas

- Asegúrate de tener permisos adecuados en el repositorio de Nexus y Google Cloud.
- El script realiza operaciones de escritura en el sistema de archivos local, así como llamadas al sistema para ejecutar Maven.
