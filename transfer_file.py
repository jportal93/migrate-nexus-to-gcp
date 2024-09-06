import os
import requests
from bs4 import BeautifulSoup
import subprocess  

html_file_path = './view-components.html'
download_folder = './view-component'

url = 'https://nexus.prueba.com/service/rest/repository/browse/npm-hosted/librery@/view-components/'
try:
    subprocess.run(['wget', '-O', html_file_path, url], check=True)
    print(f'Good {html_file_path}.')
except subprocess.CalledProcessError as e:
    print(f'Error in download: {e}')


os.makedirs(download_folder, exist_ok=True)
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, "html.parser")
a_tags = soup.find_all('a')
for a_tag in a_tags:
    href = a_tag.get('href')
    if href and href.startswith("http"):
        file_name = os.path.join(download_folder, href.split('/')[-1])
        try:
            response = requests.get(href)
            response.raise_for_status() 
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"File '{file_name}' download good '{download_folder}'.")
            subprocess.run(['npm', 'publish', file_name], check=True)
            print(f"Librery '{file_name}' push good.")
            os.remove(file_name)
            print(f"File '{file_name}' deleted.")
        except requests.exceptions.RequestException as e:
            print(f"Not Download {file_name}: {e}")
        except subprocess.CalledProcessError as e:
            print(f"Error in 'npm publish' for {file_name}: {e}")
        except Exception as e:
            print(f"Error in {file_name}: {e}")
