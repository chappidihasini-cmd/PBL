# PROJECT-BASED LEARNING (PBL) REPORT

## **MINDMAPR – SMART REVISION ASSISTANT**

**Department of Computer Science & Engineering / Information Technology**  
**Narasimha Reddy Engineering College (UGC Autonomous)**  
*Career Development Center (CDC) – Academic Year 2026*

---

## 📑 TABLE OF CONTENTS
1. [Abstract](#1-abstract)
2. [Introduction & Motivation](#2-introduction--motivation)
3. [Problem Statement](#3-problem-statement)
4. [System Architecture & Block Diagram](#4-system-architecture--block-diagram)
5. [Hardware & Software Requirements](#5-hardware--software-requirements)
6. [Detailed Module Design](#6-detailed-module-design)
7. [Algorithms & Spaced Repetition Logic](#7-algorithms--spaced-repetition-logic)
8. [Data Structures & Python Concepts Employed](#8-data-structures--python-concepts-employed)
9. [Verification & Test Cases](#9-verification--test-cases)
10. [Sample Execution Logs & Outputs](#10-sample-execution-logs--outputs)
11. [Viva Voce & Technical Defense Preparation](#11-viva-voce--technical-defense-preparation)
12. [Conclusion & Future Roadmap](#12-conclusion--future-roadmap)

---

## 1. ABSTRACT

**MindMapr – Smart Revision Assistant** is an innovative Python-based software application engineered to optimize academic study workflows and overcome the cognitive forgetting curve. Developed using pure Python standard libraries without external dependencies, MindMapr provides a menu-driven terminal interface alongside a Graphical User Interface (GUI). 

The system enables students to decompose syllabus topics into hierarchical concept branches (Mind Maps), attach active recall flashcards, and track revision schedules automatically through a scientifically grounded Spaced Repetition algorithm. Revision records are serialized persistently using JSON file storage, and comprehensive diagnostic reports can be exported in both plaintext (TXT) and interactive visual HTML/SVG formats.

---

## 2. INTRODUCTION & MOTIVATION

Academic learning frequently suffers from inefficient passive review practices, where students reread textbooks without systematic recall or scheduled re-engagement. According to Hermann Ebbinghaus’s mathematical model of memory, over 70% of newly acquired information is forgotten within 48 hours unless reinforced.

MindMapr bridges academic theory and engineering practice by providing:
- **Active Recall**: Replacing passive reading with query-response flashcard prompts.
- **Spaced Repetition**: Dynamically computing the optimal next study date based on self-evaluated mastery.
- **Hierarchical Visualization**: Mapping subjects to topics and conceptual bullet nodes.

---

## 3. PROBLEM STATEMENT

Develop a modular, persistent, and user-friendly Python console and desktop system that enables learners to:
1. Create, update, view, and delete revision subjects, topics, and conceptual notes.
2. Filter and search topics across multiple criteria (Subject, Difficulty, Status, Review Date).
3. Conduct active self-revision sessions with automated schedule recalculation.
4. Persist data continuously across executions using file handling (`JSON` / `TXT`).
5. Render analytics dashboards and generate exportable study summaries.

---

## 4. SYSTEM ARCHITECTURE & BLOCK DIAGRAM

The architecture follows a strict 4-tier modular separation of concerns matching the institutional PBL specification:

```
                  ┌──────────────────────────────┐
                  │             USER             │
                  └──────────────┬───────────────┘
                                 │
                   (CLI Inputs / GUI Events)
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       MENU CONTROLLER        │ ◄────► [ OUTPUT DISPLAY ]
                  │    (src/menu_controller.py)  │        (src/output_display.py)
                  │       (or gui.py)            │        • ASCII Tables
                  └──────────────┬───────────────┘        • Progress Bars
                                 │                        • Mind Map Trees
                        Delegates User Action             • Dashboard UI
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       CORE OPERATIONS        │
                  │   (src/core_operations.py)   │
                  │      (src/models.py)         │
                  │   • CRUD Operations          │
                  │   • Spaced Repetition Engine │
                  │   • Multi-Field Filter/Search│
                  │   • Statistical Analytics    │
                  └──────────────┬───────────────┘
                                 │
                        Persists / Restores Data
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │   FILE / DATABASE STORAGE    │
                  │       (src/storage.py)       │
                  │   • data/revision_data.json  │
                  │   • exports/Report_*.txt     │
                  │   • exports/MindMap_*.html   │
                  └──────────────────────────────┘
```

---

## 5. HARDWARE & SOFTWARE REQUIREMENTS

### Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher.
- **RAM**: Minimum 2 GB (4 GB recommended).
- **Storage**: Minimum 50 MB free disk space.
- **Display**: Any standard terminal emulator or monitor (minimum resolution $1024 \times 768$).

### Software Requirements
- **Operating System**: Cross-platform (Windows 10/11, Ubuntu/Debian Linux, macOS).
- **Programming Language**: Python 3.8 to 3.15+.
- **Standard Libraries**: `json`, `datetime`, `os`, `sys`, `typing`, `unittest`, `tkinter`.
- **External Dependencies**: Zero ($0$) external pip packages needed.

---

## 6. DETAILED MODULE DESIGN

### A. Model Layer (`src/models.py`)
Encapsulates entity structures. Every revision topic is represented as a Python dictionary:
- `id` (`str`): Unique key (e.g., `"REV-101"`).
- `subject` (`str`): Subject classification (e.g., `"Data Structures"`).
- `title` (`str`): Topic title (e.g., `"Binary Search Trees"`).
- `difficulty` (`str`): `"Easy"`, `"Medium"`, or `"Hard"`.
- `confidence` (`int`): Self-rated retention scale from $1$ (Beginner) to $5$ (Mastered).
- `status` (`str`): Current progression (`"Pending"`, `"In Progress"`, `"Mastered"`).
- `mindmap_nodes` (`List[str]`): Ordered list of core conceptual branch points.
- `flashcards` (`List[Dict[str, str]]`): Active recall Question & Answer pairs.
- `created_at`, `last_revised`, `next_revision` (`str`): ISO-formatted date strings.
- `revision_count` (`int`): Total completed revisions.

### B. Storage Layer (`src/storage.py`)
- **JSON Serialization**: Atomic reading and writing via `json.load()` and `json.dump()`.
- **Auto-Seeding**: Automatically seeds sample academic subjects upon first startup if no database is found.
- **Report Exporters**:
  - `export_text_report()`: Generates detailed summary cards in plain text format.
  - `export_html_mindmap()`: Generates an offline, responsive visual knowledge graph using CSS grid and SVG.

### C. Core Operations Layer (`src/core_operations.py`)
- **CRUD Engine**: Validates inputs, handles automatic ID incrementation (`REV-101`, `REV-102`), and executes safe updates and deletions.
- **Filtering & Search**: Case-insensitive substring matching across title, subject, notes, and mind-map nodes.
- **Metrics Calculator**: Aggregates mastery percentage, average confidence, and subject distribution.

### D. Output & Controller Layers (`src/output_display.py` & `src/menu_controller.py`)
- Renders tabular listings with fixed column widths.
- Displays visual mind map tree structures using ASCII branch connectors (`├──`, `└──`).
- Displays terminal progress meters: `[████████░░░░] 60.0%`.
- Manages submenus, input validation, and user feedback.

### E. Optional Desktop GUI Layer (`gui.py`)
- Implemented with `tkinter` and `ttk.Notebook`.
- Provides 3 interactive tabs: Topics Explorer, Active Recall Revision, and Progress Dashboard.
- Launches via `python main.py --gui` or directly via `python gui.py`.

---

## 7. ALGORITHMS & SPACED REPETITION LOGIC

MindMapr implements a discrete SuperMemo-inspired spaced repetition formula. The next revision date $\Delta t$ (in days) is calculated as a function of the user's self-assessed recall confidence $C \in \{1, 2, 3, 4, 5\}$ and revision count $N$:

$$\Delta t(C, N) = \begin{cases} 
1 \text{ day} & \text{if } C = 1 \text{ (Struggled / Low retention)} \\
2 \text{ days} & \text{if } C = 2 \text{ (Fair / Needed assistance)} \\
4 \text{ days} & \text{if } C = 3 \text{ (Good / Understood core concepts)} \\
7 \text{ days} & \text{if } C = 4 \text{ (Very Good / Fluent)} \\
14 \text{ days} & \text{if } C = 5 \text{ and } N < 3 \\
21 \text{ days} & \text{if } C = 5 \text{ and } N \ge 3 \text{ (Mastered)}
\end{cases}$$

$$\text{Next Revision Date} = \text{Current Date} + \Delta t$$

Automatic status transitions:
- If $C = 5$ and $N \ge 2 \implies \text{Status} \leftarrow \text{"Mastered"}$
- If $C \ge 3 \implies \text{Status} \leftarrow \text{"In Progress"}$
- Otherwise $\implies \text{Status} \leftarrow \text{"In Progress"}$

---

## 8. DATA STRUCTURES & PYTHON CONCEPTS EMPLOYED

| Python Concept | Where and How Applied in MindMapr |
| :--- | :--- |
| **Dictionaries (`dict`)** | Entity modeling for topics, flashcards, metadata, and metric counters. |
| **Lists (`list`)** | Topic collections, mind map concepts, flashcards, search query results. |
| **List Comprehensions** | High-performance filtering by subject, difficulty, and due dates. |
| **File I/O (`open()`)** | Context-managed read/write operations for JSON database and TXT/HTML files. |
| **String Formatting** | Column alignment (`<20`), ASCII branch trees, date formatting. |
| **Modular OOP** | Separation into distinct classes: `StorageManager`, `RevisionManager`, `MenuController`. |
| **Exception Handling** | `try...except...finally` blocks guarding against missing or corrupted files. |
| **Date Arithmetic** | `datetime` and `timedelta` calculations for spaced repetition intervals. |

---

## 9. VERIFICATION & TEST CASES

The codebase includes 14 automated unit tests in `tests/test_storage.py` and `tests/test_core_operations.py`.

| Test ID | Module Tested | Test Objective | Expected Result | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | `models` | Validate default entity creation schema | Dictionary with normalized values | **PASS** |
| **TC-02** | `models` | Verify interval calculation for Confidence 4 | Date offset equals $+7$ days | **PASS** |
| **TC-03** | `storage` | Auto-seed sample topics on first run | File created with $>0$ sample topics | **PASS** |
| **TC-04** | `storage` | Atomic save and reload verification | Reloaded data matches saved data | **PASS** |
| **TC-05** | `storage` | Plaintext TXT report exporter | Well-formatted summary file written | **PASS** |
| **TC-06** | `storage` | HTML/SVG visual Mind Map generator | Valid HTML with topic cards created | **PASS** |
| **TC-07** | `core_ops`| Create and insert new topic entity | Increments count, assigns unique ID | **PASS** |
| **TC-08** | `core_ops`| Retrieve topic by ID | Returns matching entity or `None` | **PASS** |
| **TC-09** | `core_ops`| Modify existing topic fields | Target fields updated, others intact | **PASS** |
| **TC-10** | `core_ops`| Delete topic by ID | Topic removed from working list | **PASS** |
| **TC-11** | `core_ops`| Filter topics by subject | Subset contains only matching subject | **PASS** |
| **TC-12** | `core_ops`| Multi-field keyword search | Matches found in title, notes, concepts | **PASS** |
| **TC-13** | `core_ops`| Spaced repetition execution | Updates confidence, count, and date | **PASS** |
| **TC-14** | `core_ops`| Summary metrics aggregation | Correct counts, mastery %, and averages | **PASS** |

---

## 10. SAMPLE EXECUTION LOGS & OUTPUTS

### Main Menu Interface
```
============================================================================
          MINDMAPR - SMART REVISION ASSISTANT
        Bridging Academic Learning with Structured Revision
============================================================================

========================= [ MAIN MENU ] =========================
  1. View, Search & Inspect Revision Topics
  2. Add New Topic (Mind Map Nodes & Flashcards)
  3. Update Existing Topic
  4. Delete a Topic
  5. Start Smart Revision Session (Active Recall & Spaced Repetition)
  6. View Analytics & Mastery Dashboard
  7. Export Reports & Visual Mind Maps (TXT / HTML)
  8. Exit Application
=================================================================
```

### Visual Mind Map Terminal Hierarchy
```
  [ MIND MAP HIERARCHY ]
  [Python Programming]
     └── Lists, Tuples, and Dictionaries
          ├── Lists: Mutable, ordered sequences, indexing & slicing
          ├── Tuples: Immutable sequences, hashable, tuple packing/unpacking
          ├── Dictionaries: Key-value pairs, hash tables, O(1) lookup
          └── Comprehensions: List & dictionary comprehension syntax
```

### Analytics Dashboard
```
--- [ MINDMAPR PROGRESS & ANALYTICS DASHBOARD ] -----------------------------
  Overall Progress    : [█████░░░░░░░░░░░░░░░░░░░] 20.0%
  Total Topics        : 5      | Mastered: 1    | In Progress: 2    | Pending: 2
  Average Confidence  : 3.2 / 5.0

  ┌────────────────────────────────────────────────────────────────────┐
  │ ⚡ SMART ALERT: 5 topic(s) due for revision today or overdue!        │
  │    Select option [5] from the Main Menu to start a Smart Revision! │
  └────────────────────────────────────────────────────────────────────┘

  [ SUBJECT BREAKDOWN ]
  • Python Programming       :  2 topic(s) ( 40.0%)
  • Data Structures          :  1 topic(s) ( 20.0%)
  • Operating Systems        :  1 topic(s) ( 20.0%)
  • Database Systems         :  1 topic(s) ( 20.0%)
```

---

## 11. VIVA VOCE & TECHNICAL DEFENSE PREPARATION

### Q1: Why did you choose JSON for persistent storage over plain text or SQLite?
> **Answer**: JSON provides native structural alignment with Python dictionaries and lists, allowing nested hierarchy (e.g., mind map concept lists and flashcard dictionaries) to be stored and retrieved with zero impedance mismatch. It is human-readable, lightweight, and requires no external database engine.

### Q2: How does your modular architecture adhere to software engineering principles?
> **Answer**: The application implements separation of concerns. `models.py` defines schemas, `storage.py` isolates persistence, `core_operations.py` contains business logic, and `menu_controller.py` / `gui.py` manage the presentation layer. Because business logic is decoupled from user interaction, the exact same core operations power both the terminal CLI and the desktop Tkinter GUI without altering a single line of backend code.

### Q3: How is spaced repetition implemented?
> **Answer**: Based on Ebbinghaus's forgetting curve, each topic holds a `confidence` rating (1 to 5) and a `next_revision` timestamp. When a student completes a revision session, the system computes the next revision interval dynamically ($\Delta t = 1, 2, 4, 7, 14,$ or $21$ days) using `datetime.timedelta`.

### Q4: How does the system handle corrupt or missing data files?
> **Answer**: In `StorageManager.load_data()`, file access is wrapped in a `try...except (json.JSONDecodeError, IOError)` block. If a file is corrupted, the system creates a timestamped recovery backup (`.backup_YYYYMMDD_HHMMSS`) and automatically seeds valid default sample topics, preventing catastrophic application crashes.

### Q5: How did you implement unit testing?
> **Answer**: We leveraged Python's built-in `unittest` framework to implement 14 automated test cases covering model creation, data persistence, CRUD operations, filters, search algorithms, and metric calculations. All tests pass with zero failures.

---

## 12. CONCLUSION & FUTURE ROADMAP

### Conclusion
**MindMapr – Smart Revision Assistant** successfully achieves all objectives established by the Career Development Center at Narasimha Reddy Engineering College. It demonstrates proficient use of foundational Python concepts, software architecture design, defensive error handling, and test-driven verification.

### Future Roadmap
1. **Cloud Synchronization**: Syncing JSON revision graphs to cloud databases (Firebase / AWS DynamoDB).
2. **AI Flashcard Generation**: Integrating LLM APIs to automatically generate mind map nodes and flashcards from lecture notes or textbook PDFs.
3. **Cross-Platform Mobile App**: Porting the architecture to a mobile framework (Kivy or Flutter).

---
*Report prepared for Project Based Learning (PBL) Evaluation.*

