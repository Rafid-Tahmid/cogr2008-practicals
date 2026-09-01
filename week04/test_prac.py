from prac import app


def test_count_students():
    n_max = 40 + 20 + 20 + 40
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert 0 <= int(response.data) <= n_max


def test_count_teachers():
    response = app.test_client().get('/teacher')
    assert response.status_code == 200
    assert response.data == b'There are 2 instructors'
