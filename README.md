# Takehome Test for MedlyAI Instructions.

> ## Incomplete Challenge Notes
- User migration works: 36 users inserted.
- Curriculum migration works: 8 units, 25 topics, 279 lessons inserted.
- Practice lessons migration works: 279 inserted.
- Exam lessons partially migrated: 1 lesson inserted, 0 questions.
- API endpoints not fully tested; some may fail due to type mismatch (User.id vs firebase_uid).
- Next steps if picked up later:
  1. Fix User.id vs firebase_uid type issue.
  2. Add proper tests for endpoints.
  3. Complete exam question migration.



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
curl -X GET http://localhost:8000/health | jq

returns { "status": "ok", "db": "ok" }
```

---

#### Users:

**Sample User ID:** `05IsdAyoSnekvovtyr2fC5cNOnF3`

##### `GET /users/{id}`
```bash
curl -X GET http://localhost:8000/users/<USER_ID> | jq


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
  "user_id": "05IsdAyoSnekvovtyr2fC5cNOnF3",
  "attempts": [
    {
      "attempt_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "question_id": "Q123",
      "attempt_type": "practice",
      "score": 8,
      "max_score": 10,
      "started_at": "2025-12-15T14:23:12Z",
      "submitted_at": "2025-12-15T14:25:30Z",
      "metadata": {...}
    },
    ...
  ]
}
```

##### `PATCH /users/{id}`
```bash
curl -s -X PATCH http://localhost:8000/users/<USER_ID> \
  -H "Content-Type: application/json" \
  -d '{
        "firebase_uid": "<USER_ID>",
        "metadata_jsonb": {"level": "advanced"}
      }' | jq

response: {
  "firebase_uid": "<USER_ID>",
  "metadata_jsonb": {
    "level": "advanced"
  },
  "created_at": "2025-12-16T01:01:14.421315Z",
  "updated_at": "2025-12-16T01:01:21.062704Z"
}
```

---

#### Curriculum / Assessments:

**Sample LessonID** `aqaGCSEBio0.0.0`

##### `GET /lessons/{lesson_id}`
```bash
curl -s http://localhost:8000/lessons/<LESSON_ID> | jq

response: {
  "lesson_id": "aqaGCSEBio0.0.0",
  "name": "Prokaryotic and Eukaryotic Cells",
  "unit": "Cell biology",
  "topic": "The Structure of Cells",
  "items": [
    {
      "order_index": 0,
      "item": {
        "question_id": "aqaGCSEBio0.0.0_41G0QRPtmU",
        "text": "All plant and animal cells are examples of eukaryotic cells. They share several fundamental features.\n\nDescribe how the genetic material is stored in a eukaryotic cell.",
        "markscheme": "It is contained within a (membrane-bound) nucleus.\nIt is organised as chromosomes.",
        "difficulty": 4,
        "source_type": "practice",
        "source_ref": "aqaGCSEBio0.0.0"
      }
    },...
  ]
}
```

##### `GET /papers/{paper_id}`
**Sample PaperID** `medlymockaqaGCSEBio_Sept_Mock1Higher`

```bash
curl -s http://localhost:8000/papers/<PAPER_ID> | jq

{
  "paper_id": "medlymockaqaGCSEBio_Sept_Mock1Higher",
  "subject": "Biology",
  "series": "Sept_Mock",
  "tier": "Higher",
  "items": [
    {
      "question_number": "1",
      "item": {
        "question_id": "aqaGCSEBio_1_1_1_EBc0BgD11T",
        "text": "A pharmaceutical company is developing a new antiviral drug, ‘Virostop’, to treat a new strain of influenza.\n\n**Table 1** below shows data about the number of potential drug compounds tested during the development process.",
        "markscheme": "drug was not effective (at treating the virus)\nallow it did not work",
        "difficulty": 3,
        "source_type": "exam",
        "source_ref": "medlymockaqaGCSEBio_Sept_Mock1Higher"
      }
    },
    ...
  ]
}
```

##### `GET /items/{question_id}`

**Sample QuestionID** `aqaGCSEBio0.1.1_p644iKIKCD`


```bash
curl -s http://localhost:8000/items/<QUESTION_ID> | jq


response: {
  "question_id": "aqaGCSEBio0.1.1_p644iKIKCD",
  "text": "A student uses a microscope to view a prepared slide of onion epidermal cells.\n\nA key feature of a microscope is its resolution. \n\nDescribe what is meant by the term ‘resolution’.",
  "markscheme": "The smallest distance between two points that can still be seen as separate.\nALLOW: the sharpness/clarity of the image.\nALLOW: the ability to distinguish between two points.",
  "difficulty": 2,
  "source_type": "practice",
  "source_ref": "aqaGCSEBio0.0.11"
}
```
