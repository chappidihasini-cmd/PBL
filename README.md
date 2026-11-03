# MindMapr – Smart Revision Assistant

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Layered-orange.svg)]()

> **Project Based Learning (PBL)**  
> **Career Development Center | Narasimha Reddy Engineering College**

---

## 📌 Project Overview

**MindMapr – Smart Revision Assistant** is a structured, Python-based application engineered to help students organize, track, and master academic subjects. Built entirely with pure Python standard libraries, the system implements modular programming, persistent file storage, and active recall with spaced repetition algorithms.

### Why This Project?
- **Encourages application of Python fundamentals**: Integrates lists, dictionaries, loops, functions, file handling, and modular OOP architecture.
- **Provides a real-world solution**: Helps students defeat the "forgetting curve" through structured revision scheduling and active recall.
- **Scalable to advanced versions**: Decoupled layered architecture designed to cleanly transition into GUI (Tkinter/PyQt) or Web (FastAPI/Flask) interfaces.
- **Strengthens coding confidence**: Employs clean coding standards, robust input validation, and automated unit testing.

---

## 🏛️ System Architecture & Block Diagram

The project structure directly mirrors the specified system block diagram:

```
                  ┌────────────────────────┐
                  │          User          │
                  └───────────┬────────────┘
                              │ Interacts
                              ▼
                  ┌────────────────────────┐
                  │    Menu Controller     │ ◄────► [Output Display]
                  │ (src/menu_controller)  │        (src/output_display)
                  └───────────┬────────────┘
                              │ Delegates logic
                              ▼
                  ┌────────────────────────┐
                  │    Core Operations     │
                  │ (src/core_operations)  │
                  └───────────┬────────────┘
                              │ Persists / Loads
                              ▼
                  ┌────────────────────────┐
                  │ File / Database Storage│
                  │    (JSON / TXT DB)     │
                  │    (src/storage)       │
                  └────────────────────────┘
```

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **Entity Management (CRUD)** | Add, view, update, and delete revision topics with ease. |
| **Mind Map & Concept Branching** | Break down complex topics into hierarchical bullet points and concept trees. |
| **Active Recall Flashcards** | Store question-and-answer pairs for self-testing during revision sessions. |
| **Spaced Repetition Scheduler** | Automatically calculates the next due revision date (+1, +2, +4, +7, +14, +21 days) based on your self-rated recall confidence (1–5). |
| **Categorization & Filtering** | Filter topics by Subject, Difficulty level (Easy, Medium, Hard), Status (Pending, In Progress, Mastered), or Spaced Repetition Due Date. |
| **Full-Text Multi-Field Search** | Instantly search across Topic IDs, Titles, Subjects, Notes, and Mind Map concepts. |
| **Persistent Storage (JSON & TXT)** | Automatic two-way serialization into `data/revision_data.json` and human-readable text report exports into `exports/`. |
| **Visual Dashboard & Analytics** | ASCII progress meters, topic status breakdown, confidence distribution histogram, and subject allocation. |

---

## 📁 Repository Structure

```
PBL/
├── data/
│   └── revision_data.json           # Persistent JSON database (auto-seeded)
├── exports/
│   ├── MindMap_*.html               # Interactive visual SVG/HTML Mind Map
│   └── MindMapr_Revision_Report.txt # Generated text summary reports
├── src/
│   ├── __init__.py                  # Package definition
│   ├── models.py                    # Entity structures, validation & seed generator
│   ├── storage.py                   # JSON storage manager & TXT/HTML exporter
│   ├── core_operations.py           # CRUD, search, filter, spaced repetition, metrics
│   ├── output_display.py            # Formatted ASCII tables, diagrams & dashboard
│   └── menu_controller.py           # Interactive menu navigation & input handler
├── tests/
│   ├── test_storage.py              # Unit tests for persistent storage & exports
│   └── test_core_operations.py      # Unit tests for business logic & scheduler
├── main.py                          # Unified launcher (Console & GUI modes)
├── gui.py                           # Desktop Graphical User Interface (Tkinter)
├── PROJECT_REPORT.md                # Formal PBL Submission Report & Viva Q&A
└── README.md                        # Project documentation & user guide
```

---

## 💻 Python Concepts Applied

1. **Lists & Dictionaries**:
   - Topics are stored as structured dictionary records containing nested lists of mind-map nodes and flashcard objects.
   - Dynamic sorting, filtering, and comprehension operations.
2. **File Handling & Serialization**:
   - `json.dump()` and `json.load()` ensure complete persistence across application restarts.
   - Stream-based writing (`with open(...)`) generates detailed formatted ASCII text reports.
3. **Control Flow & Loops**:
   - Interactive `while` loops for menu systems with input sanitization.
   - `for` loops with unpacking for table rendering and metric calculations.
4. **Modular Architecture**:
   - Clear separation of concerns between Controller, Business Logic, Presentation, and Data Persistence.
5. **Defensive Programming & Error Handling**:
   - `try-except` blocks protect against corrupted files, bad user inputs, and missing records.

---

## 🛠️ How to Run

### Prerequisites
- Python 3.8 or higher installed on your system.
- No external packages required (uses pure Python standard library: `json`, `datetime`, `os`, `sys`, `unittest`, `tkinter`).

### 1. Launch the Application

#### Interactive Console Menu Mode:
```bash
python main.py
```

#### Modern Desktop GUI Mode:
```bash
python main.py --gui
# or directly:
python gui.py
```

### 2. Run the Unit Test Suite
Verify that all 14 unit test cases pass:
```bash
python -m unittest discover tests
```

---

## 📖 User Manual & Workflow

### Main Menu Options
```
========================= [ MAIN MENU ] =========================
  1. View, Search & Inspect Revision Topics
  2. Add New Topic (Mind Map Nodes & Flashcards)
  3. Update Existing Topic
  4. Delete a Topic
  5. Start Smart Revision Session (Active Recall & Spaced Repetition)
  6. View Analytics & Mastery Dashboard
  7. Export Revision Summary Report (TXT)
  8. Exit Application
=================================================================
```

### 🧠 How the Smart Revision Session Works
1. When you select **Option 5**, MindMapr finds all topics that are due for revision today according to the spaced repetition schedule.
2. For each topic:
   - MindMapr presents the **Mind Map breakdown** for quick conceptual review.
   - MindMapr prompts you with **Active Recall Flashcards** one by one. Pressing `Enter` reveals the answer so you can test your memory.
   - At the end of the item, you submit your self-evaluated confidence (1 to 5).
3. MindMapr automatically recalibrates your next review date:
   - **Rating 1 (Low)**: Due again tomorrow (+1 day).
   - **Rating 2 (Fair)**: Due in 2 days (+2 days).
   - **Rating 3 (Good)**: Due in 4 days (+4 days).
   - **Rating 4 (Very Good)**: Due in 1 week (+7 days).
   - **Rating 5 (Mastered)**: Due in 2–3 weeks (+14 to +21 days).

---

## 📄 Sample Report Output

When you run **Option 7**, an ASCII report is written to the `exports/` directory:
```
========================================================================
                MINDMAPR - SMART REVISION ASSISTANT REPORT               
========================================================================
Generated On  : Tuesday, 03 November 2026 at 02:43 PM
Storage File  : data/revision_data.json
------------------------------------------------------------------------

[ EXECUTIVE SUMMARY ]
  • Total Topics Tracked  : 5
  • Mastered Topics       : 1
  • In Progress Topics    : 2
  • Pending Revision      : 2
  • Overall Mastery Rate  : 20.0%
  • Average Confidence    : 3.2 / 5.0
  • Topics Due For Revision: 5

[ SUBJECT BREAKDOWN ]
  • Python Programming        : 2 topic(s)
  • Data Structures           : 1 topic(s)
  • Operating Systems         : 1 topic(s)
  • Database Systems          : 1 topic(s)
...
```

---

## 🔮 Future Expansion (Expected Outcome Roadmap)
As outlined in the Career Development Center specification, this console application can be expanded into:
- [ ] Graphical User Interface (GUI) using `Tkinter` or `PyQt`.
- [ ] Web application with `Flask`/`FastAPI` and `SQLite`/`PostgreSQL`.
- [ ] Interactive visual mind-map graph renderer using HTML5 Canvas or `Graphviz`.

