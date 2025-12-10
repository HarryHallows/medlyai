# Medly Backend Engineer Take-Home

## Context

You’ll design and implement a small, production-ready part of our backend. The task focuses on data modeling, migration from various JSON sources, API design, and DevOps planning. We’re also assessing how you use AI in your workflow — feel free to use any copilots/agents.

**Time Allocation:** 8–12 hours

---

## Inputs (provided as JSON files)

You’ll receive four datasets:

1. **`user_data.json`**
   Nested Firebase export with per-user question attempts, e.g. keys like:
   `users/<firebase_uid>/subjectsWeb/<subject_id>/mocks/<paper_id>/questions/<questionID>` → user interaction objects (timestamps, questionID, canvas textboxes, isMarked, etc.).

2. **`aqaGCSEBio_course.json`**
   Units → topics → lessons hierarchy with stable `lessonID`s (e.g. `aqaGCSEBio0.0.11`).

3. **`aqaGCSEBio_practices.json`**
   Practice banks with per-lesson items (GCSE/AQA/subject, lesson\_id, items\[] with parts and `questionID`).

4. **`aqaGCSEBio_exams.json`**
   Paper set (board/qualification/subject/series/tier) → papers\[] → questions\[] → items\[] containing `questionID` + markscheme, difficulty, etc.

> The same `questionID` appears across Firebase user attempts and paper/practice items. The data has been cleaned but you should still handle edge cases like missing fields.

---

## Your Goal

Design a **normalized Postgres schema**, **migrate** the four JSON sources into it, and expose a minimal **Python web API** service, all **containerized** with Docker.

We want to see your judgment: how you structure the data; how you reconcile identifiers across sources; how you keep the pipeline idempotent and handle edge cases gracefully.

---

## Requirements

### 1) Data Modeling & Migration

* Define a schema that captures, at minimum:

  * **Users** (from Firebase), including stable identity and optional metadata.
  * **Curriculum** (units → topics → lessons), keyed by `lessonID`.
  * **Assessments**: model **Papers** (exam) and **Practice banks** (lesson-aligned). Represent **Items/Parts** with `questionID` as a stable external key.
  * **User–Assessment interactions** from Firebase nested targets (e.g., per question attempt context like canvas textboxes, timestamps), with references back to Items via `questionID`.
* Implement a **repeatable, idempotent** migration:

  * Parse the nested Firebase keys to extract `<firebase_uid>`, `<subject_id>`, `<paper_id>`, `<questionID>`.
  * Reconcile **`questionID`** across all data sources.
  * Map `lessonIDs` (from exam/practice questions) to real lessons in the course data (best-effort; handle missing/unknown).
  * Preserve provenance (source file, first\_seen/last\_seen timestamps).
  * Create sensible **indexes** considering scale (e.g., on `questionID`, `lessonID`, `(user_id, questionID)` for millions of questions, thousands of users).
* **Bulk inserts (required):** implement efficient bulk inserts for large datasets (particularly practice questions) and note the performance improvements over naive approaches.

**Output of the migration**

* A concise **migration report** (stdout or file): counts inserted/updated, deduped, skipped (with reasons), elapsed time.

---

### 2) API

Expose a small, useful surface (you choose exact routes, but include these capabilities):

* **Health**

  * `GET /health` → 200 with app/db status.

* **Users**

  * `GET /users/{id}` → base profile.
  * `GET /users/{id}/activity` → recent interactions (filter by subject/paper/lesson).
  * A simple write path (e.g., `PATCH /users/{id}` for name/metadata) with validation.

* **Curriculum & Assessment**

  * `GET /lessons/{lesson_id}` → lesson meta + linked practice items.
  * `GET /papers/{paper_id}` → paper meta + items (ordered by question/part).
  * `GET /items/{questionID}` → canonical item view (question text, markmax, difficulty, links to any appearances in practice/exam).

**Expectations**

* Pydantic models; clear 4xx errors; pagination on lists (default page size: 20, max: 100).
* OpenAPI docs neat and accurate - should be self-documenting.
* Query efficiency: use indexes where appropriate, but focus on correctness first.
* Response times: aim for <200ms for simple queries, <1s for complex aggregations (document any optimizations for scale).

---

### 3) Containerization

* `Dockerfile` for the API.
* `docker-compose.yml` for `api` + `postgres` (optional adminer/pgadmin is fine).
* One command to: create schema, load JSONs, run the API.

---

### 4) CI/CD (Optional Bonus)

Consider adding GitHub Actions for:

* **Lint** (your preferred linter) and **type check** (optional but recommended).
* **Tests** (your testing framework of choice) with a Postgres service.
* **Build** the Docker image. Use caching for speed.

---

### 5) Technical Documentation

Be prepared to discuss the following in the task review session: 

* **Schema design**: entity boundaries, primary/foreign keys, why you chose certain data types
* **Identifier reconciliation**: how you handle questionID matching across sources, missing references
* **Migration approach**: idempotency strategy, bulk insert implementation, error handling
* **Scalability considerations**: how your design handles 100x scale (millions of questions, thousands of subjects, concurrent users), database optimization strategies, caching approach (if any), query performance at scale
* **Key assumptions**: what edge cases you prioritized, performance vs. correctness tradeoffs
* **API design choices**: pagination strategy, error response format, validation approach

---

## Technical Constraints

* Python 3.11+, **Python web framework** (e.g., FastAPI, Django REST Framework, Flask), **ORM of choice** (e.g., SQLAlchemy, Django ORM) with **migration tool** (e.g., Alembic, Django migrations).
* **Postgres** (use JSONB where it helps, but keep the relational core solid).

---

## Testing

Demonstrate test coverage that shows engineering judgment. **Prioritize testing:**

1. **Critical path**: Migration correctness, API contract validation
2. **Edge cases**: Missing questionIDs, malformed timestamps, empty arrays
3. **Integration**: Database transactions, health checks, docker-compose startup

**Scope guidance**: Focus on meaningful tests over 100% coverage. Quality over quantity.

---

## What We’re Evaluating

**Architecture & Code Organization (40%)**
Separation of concerns, clear layers, maintainability.

**Data Migration & Integrity (25%)**
Correctness, idempotency, referential integrity, indexing.

**API Quality & Performance (20%)**
Ergonomic contracts, validation, efficient queries, bulk-insert evidence.

**Testing & Code Quality (15%)**
Meaningful test coverage, clean code structure, type safety.

---

## Submission

1. **GitHub repo** with clear setup.
2. **README.md** covering:
   * How to run with Docker Compose.
   * How to execute the migration & view the report.
   * Env vars + sensible defaults.
3. Brief technical documentation with key decisions.
4. The JSON files are located in `user_data/` and `curriculum_data/` directories (treat them as the sole source of truth).