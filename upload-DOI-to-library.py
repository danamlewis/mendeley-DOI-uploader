import requests
import importlib
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import MaxRetryError

#Input your Client ID and Client Secret
client_id = 'YOUR-CLIENT-ID'
client_secret = 'YOUR-CLIENT-SECRET'
redirect_uri = 'http://localhost'

#Input your Mendeley credentials
email = 'YOUR-EMAIL'
password = 'YOUR-MENDELEY-PASSWORD'

def get_access_token():
    filename = 'access_token.txt'
    if os.path.exists(filename):
        mod_time = os.path.getmtime(filename)
        elapsed_time = time.time() - mod_time
        if elapsed_time < 3590:
            print('Access token is still valid; proceeding.')
            with open(filename, 'r') as f:
                access_token = f.read().strip()
            return access_token
        else:
            print('Access token has expired; running authorization flow first.')
    else:
        print('Access token not found')
        return None

# Get the access token
access_token = get_access_token()

# Define function to get Mendeley authorization code using Selenium
def get_authorization_code(client_id, redirect_uri, email, password):
    authorize_url = f'https://api.mendeley.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=all'

    # Replace the path with the path to your ChromeDriver
    service = Service(executable_path='/path/to/chromedriver')
    driver = webdriver.Chrome(service=service)

    driver.get(authorize_url)

    # Wait for the email input field to become visible
    wait = WebDriverWait(driver, 10)
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="pf.username"]'))
    )
    email_input.send_keys(email)

    # Check if "Connect" button exists and click if it does
    try:
        connect_button = driver.find_element(By.XPATH, '//button[text()="Connect"]')
        connect_button.click()
    except NoSuchElementException:
        pass

    # Fill in email and password
    continue_button = driver.find_element(By.XPATH, '//button[text()="Continue"]')
    continue_button.click()

    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password_input.send_keys(password)
    connect_button = driver.find_element(By.XPATH, '//button[@value="signin"]')
    connect_button.click()

    # Wait for the page to redirect
    redirect_url = None
    while redirect_url is None or redirect_url.startswith('https://auth.mendeley.com/login'):
        redirect_url = driver.current_url
        time.sleep(1)

    # Wait for page to load after clicking Connect button
    try:
        WebDriverWait(driver, 10).until(EC.url_contains('?code='))
    except TimeoutException:
        print("Timed out waiting for page to load after clicking Connect button")
        driver.quit()

    # Get authorization code from URL
    try:
        auth_code = driver.current_url.split('code=')[1]
        print(f'Success! Authorization code: {auth_code}')
        return auth_code
    except IndexError:
        print("Authorization code not found in URL")
        driver.quit()
        return None
    except Exception as e:
        print(f'Error: {e}')
        print('Redirect failed. Could not retrieve authorization code.')
        driver.quit()
        return None

if access_token is None:
# Get the authorization code
    authorization_code = get_authorization_code(client_id, redirect_uri, email, password)

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'redirect_uri': 'http://localhost',
    }

    response = requests.post('https://api.mendeley.com/oauth/token', data=data)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        with open('access_token.txt', 'w') as file:
            file.write(access_token)
        print('Access token saved to access_token.txt')
    else:
        print('Error:', response.status_code, response.text)
else:
    print('Using existing access token')

def document_exists(doi, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(f'https://api.mendeley.com/documents?doi={doi}', headers=headers)
    if response.status_code == 200:
        return len(response.json()) > 0
    else:
        print('Error checking document existence:', response.status_code, response.text)
        return False

def create_document(doi, metadata, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/vnd.mendeley-document.1+json',
    }

    source_title = metadata.get('source')
    if isinstance(source_title, dict):
        source_title = source_title.get('title')

    data = {
        'title': metadata['title'],
        'type': metadata['type'],
        'identifiers': {
            'doi': doi,
        },
        'authors': metadata.get('authors', []),
        'year': metadata.get('year'),
	'source': source_title,
	'pages': metadata.get('pages'),
        'volume': metadata.get('volume'),
        'issue': metadata.get('issue'),
        'abstract': metadata.get('abstract'),
    }
    response = requests.post('https://api.mendeley.com/documents', headers=headers, json=data)
    if response.status_code == 201:
        print(f'Document with DOI {doi} added successfully')
    else:
        print(f'Error creating document with DOI {doi}:', response.status_code, response.text)

def read_access_token_from_file(filename='access_token.txt'):
    with open(filename, 'r') as file:
        return file.read().strip()

dois_file = 'dois.txt'

with open(dois_file, 'r') as file:
    dois = [doi.strip() for doi in file.readlines()]

for doi in dois:
    if not document_exists(doi, access_token):
        metadata = get_document_metadata(doi, access_token)
        if metadata:
            create_document(doi, metadata, access_token)
    else:
        print(f'Document with DOI {doi} already exists in the library')
