import pytest
from app import app as my_app


@pytest.fixture
def app():
    my_app.testing = True
    return my_app


def test_route_city_return_status_400_without_city_id_on_param_get(client):
    resp = client.get('/city')
    assert resp.status_code == 400


def test_route_city_return_status_404_with_city_id_nonexistent(client):
    resp = client.get('/city?id=1')
    assert resp.status_code == 404


def test_route_city_return_status_401_with_city_id(client):
    resp = client.post('/city?id=3677&days=15')
    assert resp.status_code == 404


def test_route_city_return_status_400_register_new_city_without_days(client):
    resp = client.post('/city?id=3479')
    assert resp.status_code == 400


def test_route_analyze_return_status_400_on_get_without_initial_date(client):
    resp = client.get('/analyze')
    assert resp.status_code == 400


def test_route_analyze_return_status_400_on_get_without_finish_date(client):
    resp = client.get('/analyze?initial_date=2020-11-10')
    assert resp.status_code == 400


def test_route_analyze_return_status_400_on_get_with_old_date(client):
    resp = client.get('/analyze?initial_date=2010-11-12&final_date=2011-11-19')
    assert resp.status_code == 404
