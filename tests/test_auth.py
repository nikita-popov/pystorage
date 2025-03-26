def test_login_logout(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'pystorage' in response.data

    response = client.get('/logout', follow_redirects=True)
    assert b'login' in response.data


def test_invalid_login(client):
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'creds'
    })
    assert b'Wrong credentials' in response.data
