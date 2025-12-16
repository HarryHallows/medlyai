from app.models import User


def test_get_user_by_id(client, db_session):
    user = User(firebase_uid="abc123")
    db_session.add(user)
    db_session.commit()

    response = client.get(f"/users/{user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["firebase_uid"] == "abc123"


def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404
