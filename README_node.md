
# NPM Library Downloader and Publisher

Este script en Python descarga bibliotecas desde un repositorio Nexus y las publica en NPM. Utiliza `wget` para obtener una página HTML con enlaces a las versiones disponibles de las bibliotecas, luego descarga las bibliotecas y las publica en un registro de NPM. Después de publicarlas, elimina los archivos descargados.

## Requisitos

1. **Python 3.x**
2. **Bibliotecas de Python**:
   - `requests`
   - `beautifulsoup4`
   - `subprocess`
   - `os`
   
   Puedes instalarlas ejecutando:

   ```bash
   pip install requests beautifulsoup4
   ```

3. **NPM**: Para publicar las bibliotecas en el registro de NPM.
4. **`wget`**: Necesario para descargar la página HTML con las versiones de la biblioteca.

## Configuración

Asegúrate de configurar las siguientes variables en el script:

- `url`: La URL base de tu repositorio Nexus donde se listan las versiones de la biblioteca. Por ejemplo:
  ```python
  url = 'https://nexus.prueba.com/service/rest/repository/browse/npm-hosted/librery@/view-components/'
  ```

- `html_file_path`: La ruta donde se guardará el archivo HTML descargado que contiene los enlaces a las versiones.
  ```python
  html_file_path = './view-components.html'
  ```

- `download_folder`: El directorio local donde se descargarán las versiones de la biblioteca.
  ```python
  download_folder = './view-component'
  ```

## Funciones principales

### 1. Descarga de la página HTML

El script utiliza `wget` para descargar la página HTML que contiene los enlaces a las versiones de la biblioteca.

```python
subprocess.run(['wget', '-O', html_file_path, url], check=True)
```

### 2. Extracción y descarga de archivos

El archivo HTML se analiza con `BeautifulSoup` para extraer todos los enlaces `<a>` que apunten a las versiones de la biblioteca. Luego, el script descarga cada versión.

```python
a_tags = soup.find_all('a')
for a_tag in a_tags:
    href = a_tag.get('href')
    if href and href.startswith("http"):
        # Descargar el archivo
```

### 3. Publicación en NPM

Una vez descargado el archivo, el script utiliza `npm publish` para publicarlo en NPM.

```python
subprocess.run(['npm', 'publish', file_name], check=True)
```

### 4. Eliminación de archivos descargados

Después de la publicación exitosa, el archivo se elimina del sistema.

```python
os.remove(file_name)
```

## Ejecución

Para ejecutar el script, simplemente asegúrate de que todas las dependencias estén instaladas y ejecuta el script desde la línea de comandos:

```bash
python script.py
```

El script:

1. Descargará la página HTML de versiones desde el repositorio Nexus.
2. Analizará el contenido de la página para extraer los enlaces de descarga.
3. Descargará cada versión de la biblioteca.
4. Publicará cada versión en NPM utilizando `npm publish`.
5. Eliminará el archivo descargado después de la publicación.

## Ejemplo

Supongamos que tienes la siguiente estructura en el repositorio Nexus:

```
npm-hosted/
 ├── librery@/
     ├── view-components/
         ├── 1.0.0/
         ├── 1.1.0/
```

El script:

1. Descargará las versiones `1.0.0` y `1.1.0` de `view-components`.
2. Las publicará en NPM.
3. Eliminará los archivos locales después de la publicación.

## Notas

- Asegúrate de que tienes acceso adecuado al repositorio de Nexus y al registro de NPM.
- El script eliminará los archivos descargados después de publicarlos, así que asegúrate de que esta es la funcionalidad deseada.

