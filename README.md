# Takehome Test for MedlyAI Instructions.


## Prerequisite

- [UV (Docs Linked)](https://docs.astral.sh/uv/)


## Useful commands

```bash
make (will show all available commands)
```


## Installation

```bash
make install
```

## Setup

### Build Dockerfile & Run
```bash
make run
```

## Running Application

### Curl Commands

#### Health:

##### `GET /health`

```bash
curl -X GET http://localhost:8000/health

returns { "status": "ok", "db": "ok" }
```

---

#### Users:

**Sample User ID:** `05IsdAyoSnekvovtyr2fC5cNOnF3`

##### `GET /users/{id}`
```bash
curl -X GET http://localhost:8000/users/<USER_ID>


response: {
  "id": 1,
  "firebase_uid": "abc123",
  "name": "Example Name",
  "metadata": {...}
}
```

##### `GET /users/{id}/activity`
```bash
curl -s "http://localhost:8000/users/<USER_ID>/activity?page=1&size=20" | jq

response: {
  "user_id": 1,
  "interactions": [
    {
      "question_id": "q123",
      "lesson_id": "lesson_01",
      "canvas_text": "...",
      "is_marked": true,
      "timestamp": "2025-01-01T09:00:00"
    },
    ...
  ]
}
```

##### `PATCH /users/{id}`
```bash
curl -s -X PATCH http://localhost:8000/users/<USER_ID> \
     -H "Content-Type: application/json" \
     -d '{"name": "New Name", "metadata": {"level": "advanced"}}' | jq


response: {
  "id": 1,
  "firebase_uid": "abc123",
  "name": "New Name",
  "metadata": {"level": "advanced"}
}
```

---

#### Curriculum / Assessments:

##### `GET /lessons/{lesson_id}`
```bash
curl -s http://localhost:8000/lessons/<LESSON_ID> | jq


response: {
  "lesson_id": "lesson_01",
  "topic_id": "topic_01",
  "unit_id": "unit_01",
  "title": "Cell Biology",
  "practice_items": [
    {"question_id": "q123", "text": "What is a cell?"},
    ...
  ]
}
```

##### `GET /papers/{paper_id}`
```bash
curl -s http://localhost:8000/papers/<PAPER_ID> | jq


response: {
  "paper_id": "paper_01",
  "series": "2025",
  "tier": "higher",
  "questions": [
    {
      "question_id": "q123",
      "text": "Explain mitosis",
      "markscheme": "Cell division process...",
      "difficulty": 3
    },
    ...
  ]
}
```

##### `GET /items/{question_id}`
```bash
curl -s http://localhost:8000/items/<QUESTION_ID> | jq


response: {
  "question_id": "q123",
  "text": "Explain mitosis",
  "markscheme": "Cell division process...",
  "difficulty": 3,
  "appearances": {
    "lessons": ["lesson_01", "lesson_02"],
    "papers": ["paper_01", "paper_05"]
  }
}
```
