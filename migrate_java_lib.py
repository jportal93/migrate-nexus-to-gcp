import requests
from bs4 import BeautifulSoup
import subprocess
import os
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
import shutil

########################
###########  URL  ######
########################

base_url = 'https://nexus.gg.com/service/rest/repository/browse/maven-public/com/repos/cl/'
base_dir = './java'  

#########################
#########################

def get_directories_and_files(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return [tag['href'] for tag in soup.find_all('a', href=True)], [tag.text for tag in soup.find_all('a', href=True) if not tag['href'].endswith('/')]
def download_file(url, path):
    if not os.path.basename(path):
        print(f" '{path}' is directory, not file.")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
                print(f"EUREKA {path}")
        else:
            print(f"Error status code: {response.status_code}")
    except subprocess.CalledProcessError as e:
        print(f"Error in download: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error in curl: {e}")

def update_distribution_management(pom_path, new_dist_management_xml):
    namespace = '{http://maven.apache.org/POM/4.0.0}'
    ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
    tree = ET.parse(pom_path)
    root = tree.getroot()
    project = root.find(f'{namespace}project') if root.tag != f'{namespace}project' else root
    dist_management = project.find(f'{namespace}distributionManagement')
    if dist_management is not None:
        project.remove(dist_management)
    new_dist_management_element = ET.fromstring(new_dist_management_xml)
    project.append(new_dist_management_element)
    tree.write(pom_path, encoding='utf-8', xml_declaration=True)
    print(f"Updated distributionManagement in {pom_path}")
    
def download_file(url, path):
    new_dist_management_xml = '''
<distributionManagement>
    <repository>
        <id>artifact-registry</id>
        <url>https://us-east1-maven.pkg.dev/preproduction-core38560aad/maven</url>
    </repository>
</distributionManagement>
'''
    os.makedirs(path, exist_ok=True)
    if not os.path.isdir(path):
        print(f" '{path}' is not a valid directory.")
        return
    
    filename = os.path.basename(urlsplit(url).path)
    
    if not filename:
        print(f"problems in get url: {url}")
        return
    
    full_path = os.path.join(path, filename)
    try:
        print(f"Download from: {url}")
        response = requests.get(url, allow_redirects=True)

        if response.status_code == 200:
            with open(full_path, 'wb') as file:
                file.write(response.content)
            if filename.endswith('.pom'):
                pom_path = full_path
                new_pom_path = os.path.join(path, 'pom.xml') if filename != 'pom.xml' else pom_path
                shutil.copy(pom_path, new_pom_path)
                print(f"Renamed: {pom_path} to {new_pom_path}")
                update_distribution_management(new_pom_path, new_dist_management_xml)
        else:
            print(f"Error in download: {response.status_code}")
    except Exception as e:
        print(f"Error in download file: {e}")

def maven_push(dir):
    try:
        os.chdir(dir)
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).strip().decode('utf-8')
        os.environ['GOOGLE_MAVEN_AUTH'] = token
        result = subprocess.run(["mvn", "deploy", "-X"], check=True)        
        print("Maven deploy completed successfully.")
        os.chdir("../../..")
        print(f"Now back 3 directories: {os.getcwd()}")
    except subprocess.CalledProcessError as e:
        print(f"Error in Maven deploy: {e}")
        os.chdir("../../..")
    except Exception as e:
        print(f"An error occurred: {e}")
        os.chdir("../../..")

def check_and_run_maven_push(file_path):
    pom_file = os.path.join(file_path, "pom.xml")
    if os.path.isfile(pom_file):
        print(f"'pom.xml' found pom file {file_path}. maven_push.")
        maven_push(file_path)
    else:
        print(f"'pom.xml' not found in {file_path}. not run maven_push.")
    try:

        shutil.rmtree(file_path)
        print(f"Directory {file_path} eliminate succesfully.")
    except Exception as e:
        print(f"Error in delete {file_path}: {e}")
        
def process_artifact_versions(base_url, artifact, base_dir):
    versions_url = f"{base_url}{artifact}/"
    versions, _ = get_directories_and_files(versions_url)
    for version in versions:
        if version == "../":
            pass
        else:
            version_name = version.split('/')[-2]
            version_dir = os.path.join(base_dir, artifact, version_name)
            os.makedirs(version_dir, exist_ok=True)
            files, _ = get_directories_and_files(f"{versions_url}{version}")
            for file in files:
                if file == "../":
                    pass
                else:
                    if file.endswith('/'):
                        files2, _ = get_directories_and_files(f"{versions_url}{version}{file}")
                        for file2 in files2:
                            if file2 == "../":
                                pass
                            else:
                                file_url = f"{file2}"
                                file_path = version_dir
                                print(file_path)
                                download_file(file_url, file_path)
                    else:
                        file_url = f"{file}"
                        file_path = version_dir
                        download_file(file_url, file_path)                        
                        print(file_url)
                        print(f"Descargado {file} en {version_dir}")
            check_and_run_maven_push(file_path)

artifacts, _ = get_directories_and_files(base_url)
artifacts = [artifact for artifact in artifacts if artifact.endswith('/')]
for artifact in artifacts:
    print(artifact)
    if artifact == "../":
        pass
    else:
        artifact_name = artifact.rstrip('/').split('/')[-1]
        process_artifact_versions(base_url, artifact_name, base_dir)
