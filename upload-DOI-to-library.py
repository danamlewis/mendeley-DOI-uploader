import requests

def get_document_metadata(doi, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(f'https://api.mendeley.com/catalog?doi={doi}&view=stats', headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    else:
        print('Error fetching document metadata:', response.status_code, response.text)
        return None

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

# Note that this is reading the token generated from get-mendeley-token.py
access_token = read_access_token_from_file()
dois_file = 'dois.txt'

with open(dois_file, 'r') as file:
    dois = [doi.strip() for doi in file.readlines()]

for doi in dois:
    metadata = get_document_metadata(doi, access_token)
    if metadata:
        create_document(doi, metadata, access_token)
