def test_chat_validation_error(client):
    response = client.post("/api/chat", json={}) # Missing required question
    assert response.status_code == 422
