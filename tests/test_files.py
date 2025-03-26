import io


def test_upload_and_download(auth_client):
    test_file = (io.BytesIO(b'test content'), 'test.txt')
    response = auth_client.post('/upload', data={
        'file': test_file,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'test.txt' in response.data

    response = auth_client.get('/download/test.txt')
    assert response.status_code == 200
    assert response.data == b'test content'


def test_file_list(auth_client):
    response = auth_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Files list' in response.data
