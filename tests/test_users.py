from fastapi.testclient import TestClient
from app.main import app
from app.routers import users as users_router_module


import pytest


# -------------------------
# FAKE DB HELPERS
# -------------------------
class FakeResult:
    def __init__(self, data):
        self._data = data

    def all(self):
        return self._data

    def scalars(self):
        return self


class FakeDB:
    def __init__(self, query_return=None, execute_return=None, commit_side_effect=None, get_return=None):
        self._query_return = query_return
        self._execute_return = execute_return or []
        self._commit_side_effect = commit_side_effect
        self._get_return = get_return

    def query(self, model):
        return FakeQuery(self._query_return)

    def execute(self, query):
        return FakeResult(self._execute_return)

    def get(self, model, pk):
        # Return get_return if provided, otherwise fall back to query_return
        return self._get_return if self._get_return is not None else self._query_return

    def commit(self):
        if self._commit_side_effect:
            self._commit_side_effect()

    def refresh(self, obj):
        pass


class FakeQuery:
    def __init__(self, return_value):
        self._return_value = return_value

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def offset(self, value):
        return self

    def limit(self, value):
        return self

    def first(self):
        return self._return_value

    def all(self):
        if isinstance(self._return_value, list):
            return self._return_value
        return [self._return_value] if self._return_value else []


client = TestClient(app)


# -------------------------
# USER TESTS
# -------------------------
def test_get_user_success():
    class FakeUser:
        firebase_uid = "user1"
        username = "Test User"
        metadata_jsonb = {"level": 1}
        created_at = "2024-01-01T00:00:00"
        updated_at = "2024-01-01T00:00:00"

    app.dependency_overrides[users_router_module.get_db] = lambda: FakeDB(
        query_return=FakeUser()
    )

    response = client.get("/users/user1")
    assert response.status_code == 200
    data = response.json()
    assert data["firebase_uid"] == "user1"

    # Clean up
    app.dependency_overrides.clear()


def test_get_user_not_found():
    app.dependency_overrides[users_router_module.get_db] = lambda: FakeDB(
        query_return=None
    )

    response = client.get("/users/nonexistent")
    assert response.status_code == 404

    # Clean up
    app.dependency_overrides.clear()


# -------------------------
# USER ACTIVITY TESTS
# -------------------------
def test_user_activity_success():
    class FakeAttempt:
        attempt_id = "550e8400-e29b-41d4-a716-446655440000"  # Valid UUID
        user_id = "user1"
        question_id = "q1"
        attempt_type = "exam"  # Must be 'exam' or 'practice'
        submitted_at = "2024-01-01T00:00:00"
        started_at = "2024-01-01T00:00:00"
        score = 85
        max_score = 100
        metadata_jsonb = {}

    app.dependency_overrides[users_router_module.get_db] = lambda: FakeDB(
        query_return=[FakeAttempt()]
    )

    response = client.get("/users/user1/activity")
    assert response.status_code == 200
    data = response.json()
    assert "attempts" in data
    assert len(data["attempts"]) > 0

    # Clean up
    app.dependency_overrides.clear()


def test_user_activity_empty():
    app.dependency_overrides[users_router_module.get_db] = lambda: FakeDB(
        query_return=[]
    )

    response = client.get("/users/user1/activity")
    assert response.status_code == 200
    data = response.json()
    assert "attempts" in data
    assert len(data["attempts"]) == 0

    # Clean up
    app.dependency_overrides.clear()


# -------------------------
# UPDATE USER TESTS
# -------------------------
def test_update_user_success():
    pass

def test_update_user_not_found():
    pass