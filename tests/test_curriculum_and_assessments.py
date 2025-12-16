from fastapi.testclient import TestClient
from app.main import app
from app.routers import curriculum_and_assessments as router_module


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
    def __init__(self, get_return=None, execute_return=None):
        self._get_return = get_return
        self._execute_return = execute_return or []

    def get(self, model, pk):
        return self._get_return

    def execute(self, query):
        return FakeResult(self._execute_return)


client = TestClient(app)


# -------------------------
# LESSON TESTS
# -------------------------
def test_get_lesson_returns_response():
    class FakeItem:
        question_id = "q1"
        text = "What is X?"
        markscheme = "Answer X"
        difficulty = 1
        source_type = "exam"
        source_ref = "ref1"

    class FakeLesson:
        lesson_id = "lesson1"
        name = "Intro"
        unit = "Unit1"
        topic = "Topic1"

    app.dependency_overrides[router_module.get_db] = lambda: FakeDB(
        get_return=FakeLesson(), execute_return=[FakeItem()]
    )

    response = client.get("/lessons/lesson1")
    assert response.status_code == 200
    data = response.json()
    assert data["lesson_id"] == "lesson1"
    assert len(data["items"]) == 1
    assert data["items"][0]["item"]["question_id"] == "q1"


def test_get_lesson_returns_404_not_found():
    app.dependency_overrides[router_module.get_db] = lambda: FakeDB(get_return=None)
    response = client.get("/lessons/nonexistent")
    assert response.status_code == 404


# -------------------------
# PAPER TESTS
# -------------------------
def test_get_paper_returns_response():
    class FakeItem:
        question_id = "q1"
        text = "Question?"
        markscheme = "Answer"
        difficulty = 2
        source_type = "exam"
        source_ref = "ref1"

    class FakePaperItem:
        question_number = "1"

    class FakePaper:
        paper_id = "paper1"
        series = "SeriesA"
        tier = "Higher"
        subject = "Biology"

    app.dependency_overrides[router_module.get_db] = lambda: FakeDB(
        get_return=FakePaper(), execute_return=[(FakePaperItem(), FakeItem())]
    )

    response = client.get("/papers/paper1")
    assert response.status_code == 200
    data = response.json()

    assert data["paper_id"] == "paper1"
    assert data["subject"] == "Biology"
    assert data["series"] == "SeriesA"
    assert data["tier"] == "Higher"

    assert len(data["items"]) == 1
    assert data["items"][0]["question_number"] == "1"
    assert data["items"][0]["item"]["question_id"] == "q1"
    assert data["items"][0]["item"]["difficulty"] == 2
    assert data["items"][0]["item"]["markscheme"] == "Answer"
    assert data["items"][0]["item"]["source_type"] == "exam"
    assert data["items"][0]["item"]["text"] == "Question?"


def test_get_paper_returns_404_not_found():
    app.dependency_overrides[router_module.get_db] = lambda: FakeDB(get_return=None)
    response = client.get("/papers/nonexistent")
    assert response.status_code == 404


# -------------------------
# ITEM TESTS
# -------------------------
def test_get_item_returns_response():
    class FakeItem:
        question_id = "q1"
        text = "What is X?"
        markscheme = "Answer X"
        difficulty = 1
        source_type = "exam"
        source_ref = "ref1"
        # make appearances an actual attribute, not a property
        appearances = {"lessons": ["lesson1"], "papers": ["paper1"]}

    app.dependency_overrides[router_module.get_db] = lambda: FakeDB(
        get_return=FakeItem()
    )

    response = client.get("/items/q1")
    assert response.status_code == 200

    data = response.json()
    assert data["question_id"] == "q1"
    assert data["text"] == "What is X?"
    assert data["markscheme"] == "Answer X"
    assert data["difficulty"] == 1
    assert data["source_type"] == "exam"
    assert data["source_ref"] == "ref1"


def test_get_item_returns_404_not_found():
    app.dependency_overrides[router_module.get_db] = lambda: FakeDB(get_return=None)
    response = client.get("/items/nonexistent")
    assert response.status_code == 404
