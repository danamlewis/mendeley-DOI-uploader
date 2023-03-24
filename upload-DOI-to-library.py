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

# Make sure to replace AUTHORIZATION_CODE with the code you got from Mendeley, and make sure your DOI text file matches the name you gave it.
access_token = 'AUTHORIZATION_CODE'
dois_file = 'dois.txt'

with open(dois_file, 'r') as file:
    dois = [doi.strip() for doi in file.readlines()]

for doi in dois:
    metadata = get_document_metadata(doi, access_token)
    if metadata:
        create_document(doi, metadata, access_token)
