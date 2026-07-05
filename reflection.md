# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The app needs to support three core user actions:
1. **Add a pet-care task** — the owner records something that needs to happen (e.g., a walk, a feeding, a med), along with how long it takes and how important it is.
2. **Generate a daily schedule** — given a list of tasks and a limited amount of time available today, the system decides which tasks fit, in what order, and at what time each one starts.
3. **See today's plan and why** — the owner sees the resulting schedule along with a short explanation of why each task was included, and which tasks (if any) didn't fit and why.

To support this, the design has four classes, all living in `pawpal_system.py`:

- **Task** — holds the data for one care task: `title` (what it is), `duration_minutes` (how long it takes), and `priority` (`"low"`/`"medium"`/`"high"`, how important it is). It has no behavior of its own — it's a plain data holder (`@dataclass`).
- **Pet** — holds identity info for the animal being cared for: `name` and `species`.
- **Owner** — holds identity info for the person doing the planning: `name`.
- **Scheduler** — the only class with real behavior. Its `build_schedule(tasks, available_minutes, start_minute)` method takes the raw list of tasks plus the time budget and turns it into a `ScheduleResult`: an ordered list of `ScheduledTask` (each with a computed start/end time and a reason it was chosen) and a list of skipped tasks (each with a reason it didn't fit). It decides *what* happens and *when*, while `Task`/`Pet`/`Owner` just describe *who*/*what*.

**b. Design changes**

The scheduling logic was originally split across two files — a `models.py` for the plain data classes (`Task`, `Pet`, `Owner`) and a `scheduler.py` for the behavior (`Scheduler`, `ScheduledTask`, `ScheduleResult`). It was consolidated into a single `pawpal_system.py` logic-layer file to match the project's expected structure. This was a pure reorganization — no class attributes, methods, or scheduling behavior changed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: **priority** (`"low"`/`"medium"`/`"high"`) and **available time** (a daily minute budget). `Scheduler.build_schedule()` sorts by priority first, then by duration as a tie-break, then greedily fits tasks into the remaining budget — so high-priority tasks are never bumped by lower-priority ones, but among equal-priority tasks, shorter ones are preferred since they let more tasks fit into a limited day. Priority mattered most because the scenario is about a busy owner who needs the *important* things (meds, feeding) guaranteed before nice-to-haves (playtime) when time runs short.

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only checks for exact `time` string matches (e.g., two tasks both at `"08:00"`) rather than checking whether tasks' full duration windows overlap (e.g., an 08:00–08:30 task and an 08:15 task). This is a deliberately lightweight strategy: it's a simple dictionary lookup grouped by the `time` string, with no interval-overlap math, so it's fast and easy to reason about. The tradeoff is that it will miss "soft" conflicts where two tasks start at different times but their durations overlap — that's reasonable for this scenario because the owner is mainly trying to catch obvious double-bookings ("I put two things at 8am"), not build a minute-precise calendar; a stricter overlap check could always be added later without changing the rest of the design.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
