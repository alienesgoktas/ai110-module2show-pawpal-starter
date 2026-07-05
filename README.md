# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
$ python main.py
Today's Schedule for Jordan's pets
========================================
08:00 - Feeding (10 min) [priority: high]
08:10 - Morning walk (30 min) [priority: high]
08:40 - Litter box cleaning (10 min) [priority: medium]

Skipped:
  Playtime: skipped - not enough remaining time (10 min left, needs 15 min)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

The suite covers: priority-based schedule building under a time budget (`tests/test_scheduler.py`), and — in `tests/test_pawpal.py` — task completion, chronological sorting (with untimed tasks last), filtering by status/pet, recurring daily/weekly tasks advancing correctly via `timedelta`, and conflict detection (same pet, across pets, and correctly ignoring already-completed tasks). It also covers empty-state edge cases: a pet with no tasks and an owner with no pets.

Sample test output:

```
$ pytest
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Enes\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 19 items

tests\test_pawpal.py ..............                                      [ 73%]
tests\test_scheduler.py .....                                            [100%]

============================= 19 passed in 0.03s ==============================
```

**Confidence Level:** ★★★★☆ (4/5) — all core scheduling, sorting, filtering, recurrence, and conflict-detection behaviors are covered by passing tests, including several edge cases (empty pets/owners, same-pet conflicts, completed-task exclusion). Not a 5: conflict detection only checks exact time matches, not overlapping durations (see `reflection.md` section 2b), so that gap isn't and can't be tested yet.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their `"HH:MM"` time string; untimed tasks sort last |
| Filtering | `Scheduler.filter_by_status()`, `Owner.tasks_for_pet()` | Filter by completion status, or by which pet a task belongs to |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns when two or more pending tasks (any pet) share the same clock time; returns an empty list instead of raising |
| Recurring tasks | `Task.next_occurrence()`, `Pet.mark_task_complete()` | Completing a `"daily"`/`"weekly"` task auto-creates its next occurrence with `due_date` advanced via `timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
