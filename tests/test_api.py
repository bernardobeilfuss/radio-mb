from fastapi.testclient import TestClient

from server.app import app, HEARTBEATS, PLAYBACK_LOG

client = TestClient(app)


def setup_function():
    HEARTBEATS.clear()
    PLAYBACK_LOG.clear()


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_megashop_is_registered():
    response = client.get('/api/stores')
    assert response.status_code == 200
    stores = response.json()
    assert any(store['slug'] == 'megashop' for store in stores)


def test_next_media_for_megashop_uses_only_approved_media():
    response = client.get('/api/player/megashop/next')
    assert response.status_code == 200
    media = response.json()
    assert media['license_status'] == 'approved'
    assert media['id'] == 1


def test_heartbeat_for_megashop():
    response = client.post('/api/player/megashop/heartbeat')
    assert response.status_code == 200
    payload = response.json()
    assert payload['store'] == 'megashop'
    assert 'megashop' in HEARTBEATS


def test_playback_log_for_megashop():
    start = client.post('/api/player/megashop/playback/start', json={'media_id': 1})
    end = client.post('/api/player/megashop/playback/end', json={'media_id': 1})

    assert start.status_code == 200
    assert end.status_code == 200
    assert len(PLAYBACK_LOG) == 2
    assert PLAYBACK_LOG[0]['store_slug'] == 'megashop'
    assert PLAYBACK_LOG[0]['event'] == 'start'
    assert PLAYBACK_LOG[1]['event'] == 'end'


def test_invalid_store_returns_404():
    response = client.get('/api/player/nao-existe/next')
    assert response.status_code == 404
