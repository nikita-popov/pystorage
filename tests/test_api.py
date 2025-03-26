import io
import os


def test_api_files(client, api_headers):
    response = client.get('/api/files')
    assert response.status_code == 401

    response = client.get('/api/files', headers=api_headers)
    assert response.status_code == 200
    assert 'files' in response.json


def test_api_upload(client, api_headers):
    test_file = (io.BytesIO(b'api content'), 'api_test.txt')

    response = client.post('/api/upload',
                           data={'file': test_file},
                           headers=api_headers,
                           )

    assert response.status_code == 201
    assert 'api_test.txt' in response.json['filename']


def test_api_delete(client, api_headers):
    uploads = f"{client.application.config['UPLOAD_FOLDER']}/testuser"
    os.makedirs(uploads, exist_ok=True)
    test_file = os.path.join(uploads, 'to_delete.txt')
    with open(test_file, 'w') as f:
        f.write('content')

    response = client.delete('/api/delete/to_delete.txt', headers=api_headers)
    assert response.status_code == 200
    assert not os.path.exists(test_file)
