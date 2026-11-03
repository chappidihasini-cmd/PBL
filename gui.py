"""
gui.py
Optional Desktop Graphical User Interface (GUI) for MindMapr - Smart Revision Assistant.
Built using Python's standard library tkinter and ttk.
Demonstrates the modularity of the architecture: seamlessly reuses
core_operations.py and storage.py without modifying business logic.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.storage import StorageManager
from src.core_operations import RevisionManager


class MindMaprGUI:
    """Tkinter Desktop Application for MindMapr."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MindMapr – Smart Revision Assistant")
        self.root.geometry("980x680")
        self.root.minsize(800, 550)

        # Initialize Backend
        self.storage = StorageManager()
        self.manager = RevisionManager(self.storage.load_data())

        # Revision Session State
        self.session_topics = []
        self.current_session_index = 0
        self.current_card_index = 0

        self._configure_styles()
        self._build_ui()
        self.refresh_topics_table()

    def _configure_styles(self) -> None:
        """Applies clean styling to ttk widgets."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TNotebook", tabposition="n")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#0284c7")

    def _build_ui(self) -> None:
        """Constructs main layout with tabs."""
        # Top Header Banner
        header_frame = ttk.Frame(self.root, padding="12 10 12 6")
        header_frame.pack(fill=tk.X)

        title_lbl = ttk.Label(header_frame, text="MindMapr – Smart Revision Assistant", style="Header.TLabel")
        title_lbl.pack(side=tk.LEFT)

    

        # Tab Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: Topics Explorer
        self.tab_explorer = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_explorer, text="📚 Revision Topics")
        self._build_explorer_tab()

        # Tab 2: Smart Revision Session
        self.tab_session = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_session, text="🧠 Smart Revision & Active Recall")
        self._build_session_tab()

        # Tab 3: Dashboard & Analytics
        self.tab_analytics = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_analytics, text="📊 Progress Dashboard")
        self._build_analytics_tab()

    # -------------------------------------------------------------
    # Tab 1: Topics Explorer
    # -------------------------------------------------------------
    def _build_explorer_tab(self) -> None:
        # Search & Filter Bar
        filter_frame = ttk.LabelFrame(self.tab_explorer, text="Filter & Search", padding=8)
        filter_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.apply_filters())
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=22)
        search_entry.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(filter_frame, text="Subject:").pack(side=tk.LEFT, padx=(0, 4))
        self.subject_filter_var = tk.StringVar(value="All Subjects")
        self.subject_combo = ttk.Combobox(filter_frame, textvariable=self.subject_filter_var, state="readonly", width=18)
        self.subject_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.subject_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 4))
        self.status_filter_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_filter_var, state="readonly", width=12,
                                    values=["All", "Pending", "In Progress", "Mastered"])
        status_combo.pack(side=tk.LEFT, padx=(0, 15))
        status_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        btn_refresh = ttk.Button(filter_frame, text="Reset", command=self.reset_filters)
        btn_refresh.pack(side=tk.LEFT)

        # Topics Treeview Table
        table_frame = ttk.Frame(self.tab_explorer)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "subject", "title", "diff", "conf", "status", "due")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("title", text="Title")
        self.tree.heading("diff", text="Difficulty")
        self.tree.heading("conf", text="Confidence")
        self.tree.heading("status", text="Status")
        self.tree.heading("due", text="Next Revision")

        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("subject", width=160)
        self.tree.column("title", width=260)
        self.tree.column("diff", width=85, anchor=tk.CENTER)
        self.tree.column("conf", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=95, anchor=tk.CENTER)
        self.tree.column("due", width=100, anchor=tk.CENTER)

        tree_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_topic_select)

        # Split Bottom Details & Actions
        bottom_frame = ttk.Frame(self.tab_explorer, padding=(0, 8))
        bottom_frame.pack(fill=tk.BOTH, expand=False)

        # Details Display
        detail_frame = ttk.LabelFrame(bottom_frame, text="Topic Mind Map & Details", padding=8)
        detail_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.detail_text = tk.Text(detail_frame, height=7, wrap=tk.WORD, font=("Consolas", 9))
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        # Action Buttons
        action_frame = ttk.Frame(bottom_frame)
        action_frame.pack(side=tk.RIGHT, fill=tk.Y)

        btn_add = ttk.Button(action_frame, text="➕ Add Topic", command=self._open_add_topic_dialog, width=15)
        btn_add.pack(pady=3)

        btn_delete = ttk.Button(action_frame, text="🗑️ Delete Topic", command=self._delete_selected_topic, width=15)
        btn_delete.pack(pady=3)

        btn_export_txt = ttk.Button(action_frame, text="📄 Export TXT", command=self._export_txt, width=15)
        btn_export_txt.pack(pady=3)

        btn_export_html = ttk.Button(action_frame, text="🌐 HTML MindMap", command=self._export_html, width=15)
        btn_export_html.pack(pady=3)

    # -------------------------------------------------------------
    # Tab 2: Smart Revision Session
    # -------------------------------------------------------------
    def _build_session_tab(self) -> None:
        ctrl_frame = ttk.Frame(self.tab_session, padding=10)
        ctrl_frame.pack(fill=tk.X)

        self.session_info_lbl = ttk.Label(ctrl_frame, text="Click 'Start Session' to begin spaced revision for due topics.", font=("Segoe UI", 10, "bold"))
        self.session_info_lbl.pack(side=tk.LEFT)

        btn_start = ttk.Button(ctrl_frame, text="🚀 Start Smart Revision", command=self._start_revision_session)
        btn_start.pack(side=tk.RIGHT)

        # Card Container
        self.card_frame = ttk.LabelFrame(self.tab_session, text="Revision Item", padding=15)
        self.card_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.rev_topic_lbl = ttk.Label(self.card_frame, text="No active revision session.", font=("Segoe UI", 13, "bold"), foreground="#0284c7")
        self.rev_topic_lbl.pack(anchor=tk.W, pady=(0, 4))

        self.rev_meta_lbl = ttk.Label(self.card_frame, text="", font=("Segoe UI", 9))
        self.rev_meta_lbl.pack(anchor=tk.W, pady=(0, 10))

        # Mind Map concept review
        ttk.Label(self.card_frame, text="Mind Map Core Concepts:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.rev_concepts_text = tk.Text(self.card_frame, height=5, wrap=tk.WORD, font=("Segoe UI", 9), background="#f8fafc")
        self.rev_concepts_text.pack(fill=tk.X, pady=(2, 10))

        # Flashcard Active Recall
        fc_frame = ttk.LabelFrame(self.card_frame, text="Active Recall Flashcard", padding=10)
        fc_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.fc_q_lbl = ttk.Label(fc_frame, text="Question will appear here.", font=("Segoe UI", 10, "bold"), wraplength=700)
        self.fc_q_lbl.pack(anchor=tk.W, pady=(0, 8))

        self.fc_a_lbl = ttk.Label(fc_frame, text="", font=("Segoe UI", 10), foreground="#047857", wraplength=700)
        self.fc_a_lbl.pack(anchor=tk.W, pady=(0, 8))

        btn_reveal = ttk.Button(fc_frame, text="👁️ Reveal Answer", command=self._reveal_flashcard_answer)
        btn_reveal.pack(side=tk.LEFT, pady=4)

        btn_next_card = ttk.Button(fc_frame, text="Next Flashcard ⏩", command=self._next_flashcard)
        btn_next_card.pack(side=tk.LEFT, padx=10, pady=4)

        # Rating & Next Step
        rating_frame = ttk.Frame(self.card_frame, padding=(0, 10))
        rating_frame.pack(fill=tk.X)

        ttk.Label(rating_frame, text="Rate Recall Confidence:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        self.rating_var = tk.IntVar(value=3)
        for r, text in [(1, "1-Low"), (2, "2-Fair"), (3, "3-Good"), (4, "4-Very Good"), (5, "5-Mastered")]:
            ttk.Radiobutton(rating_frame, text=text, variable=self.rating_var, value=r).pack(side=tk.LEFT, padx=4)

        btn_save_item = ttk.Button(rating_frame, text="💾 Complete & Next Topic", command=self._complete_current_topic)
        btn_save_item.pack(side=tk.RIGHT, padx=5)

    # -------------------------------------------------------------
    # Tab 3: Dashboard & Analytics
    # -------------------------------------------------------------
    def _build_analytics_tab(self) -> None:
        self.analytics_frame = ttk.Frame(self.tab_analytics)
        self.analytics_frame.pack(fill=tk.BOTH, expand=True)

    def refresh_analytics(self) -> None:
        """Renders updated dashboard figures."""
        for w in self.analytics_frame.winfo_children():
            w.destroy()

        metrics = self.manager.get_summary_metrics()

        header = ttk.Label(self.analytics_frame, text="MindMapr Performance & Mastery Metrics", font=("Segoe UI", 12, "bold"))
        header.pack(anchor=tk.W, pady=(0, 15))

        # Metrics Grid
        grid_frame = ttk.Frame(self.analytics_frame)
        grid_frame.pack(fill=tk.X, pady=(0, 20))

        cards = [
            ("Total Topics", str(metrics["total_topics"]), "#0284c7"),
            ("Mastered", str(metrics["mastered_count"]), "#16a34a"),
            ("In Progress", str(metrics["in_progress_count"]), "#d97706"),
            ("Pending", str(metrics["pending_count"]), "#dc2626"),
            ("Mastery %", f"{metrics['mastery_pct']}%", "#9333ea"),
            ("Due Today", str(metrics["due_count"]), "#e11d48"),
        ]

        for i, (title, val, col) in enumerate(cards):
            card = ttk.LabelFrame(grid_frame, text=title, padding=12)
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            lbl = ttk.Label(card, text=val, font=("Segoe UI", 16, "bold"), foreground=col)
            lbl.pack(anchor=tk.CENTER)
            grid_frame.columnconfigure(i, weight=1)

        # Subject breakdown
        subj_frame = ttk.LabelFrame(self.analytics_frame, text="Subject Distribution", padding=10)
        subj_frame.pack(fill=tk.BOTH, expand=True)

        for subj, count in metrics["subject_breakdown"].items():
            pct = (count / metrics["total_topics"]) * 100 if metrics["total_topics"] > 0 else 0
            row = ttk.Frame(subj_frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=f"{subj}:", width=25, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
            ttk.Label(row, text=f"{count} topics ({pct:.1f}%)").pack(side=tk.LEFT)

    # -------------------------------------------------------------
    # Topic Operations & Events
    # -------------------------------------------------------------
    def refresh_topics_table(self, topics=None) -> None:
        """Populates the topics treeview."""
        if topics is None:
            topics = self.manager.get_all_topics()

        # Update subjects combo
        all_subjects = ["All Subjects"] + self.manager.get_all_subjects()
        self.subject_combo["values"] = all_subjects
        if self.subject_filter_var.get() not in all_subjects:
            self.subject_filter_var.set("All Subjects")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for t in topics:
            stars = "★" * t.get("confidence", 1) + "☆" * (5 - t.get("confidence", 1))
            self.tree.insert("", tk.END, iid=t.get("id"), values=(
                t.get("id"),
                t.get("subject"),
                t.get("title"),
                t.get("difficulty"),
                f"{t.get('confidence')}/5 {stars}",
                t.get("status"),
                t.get("next_revision")
            ))

        self.refresh_analytics()

    def apply_filters(self) -> None:
        """Filters topics according to user entries."""
        query = self.search_var.get().strip()
        selected_subject = self.subject_filter_var.get()
        selected_status = self.status_filter_var.get()

        topics = self.manager.get_all_topics()

        if query:
            topics = self.manager.search_topics(query)

        if selected_subject != "All Subjects":
            topics = [t for t in topics if t.get("subject", "").lower() == selected_subject.lower()]

        if selected_status != "All":
            topics = [t for t in topics if t.get("status", "").lower() == selected_status.lower()]

        self.refresh_topics_table(topics)

    def reset_filters(self) -> None:
        self.search_var.set("")
        self.subject_filter_var.set("All Subjects")
        self.status_filter_var.set("All")
        self.refresh_topics_table()

    def _on_topic_select(self, event) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        topic_id = selected[0]
        topic = self.manager.get_topic_by_id(topic_id)
        if not topic:
            return

        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, f"TOPIC: {topic.get('title')} ({topic.get('id')})\n")
        self.detail_text.insert(tk.END, f"Subject: {topic.get('subject')} | Difficulty: {topic.get('difficulty')} | Status: {topic.get('status')}\n")
        self.detail_text.insert(tk.END, f"Last Revised: {topic.get('last_revised')} | Next Due: {topic.get('next_revision')}\n\n")

        self.detail_text.insert(tk.END, "Mind Map Core Concepts:\n")
        nodes = topic.get("mindmap_nodes", [])
        if nodes:
            for n in nodes:
                self.detail_text.insert(tk.END, f"  • {n}\n")
        else:
            self.detail_text.insert(tk.END, "  (No concept nodes attached)\n")

        if topic.get("notes"):
            self.detail_text.insert(tk.END, f"\nNotes: {topic.get('notes')}\n")

    def _delete_selected_topic(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a topic to delete.")
            return

        topic_id = selected[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete topic {topic_id}?"):
            self.manager.delete_topic(topic_id)
            self.storage.save_data(self.manager.get_all_topics())
            self.refresh_topics_table()
            self.detail_text.delete("1.0", tk.END)
            messagebox.showinfo("Success", f"Topic {topic_id} deleted.")

    def _open_add_topic_dialog(self) -> None:
        """Opens a popup modal to add a new revision topic."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Revision Topic")
        dialog.geometry("480x520")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Subject:").pack(anchor=tk.W, padx=15, pady=(12, 2))
        subj_entry = ttk.Entry(dialog, width=50)
        subj_entry.pack(padx=15, fill=tk.X)

        ttk.Label(dialog, text="Topic Title:").pack(anchor=tk.W, padx=15, pady=(8, 2))
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.pack(padx=15, fill=tk.X)

        ttk.Label(dialog, text="Difficulty:").pack(anchor=tk.W, padx=15, pady=(8, 2))
        diff_combo = ttk.Combobox(dialog, state="readonly", values=["Easy", "Medium", "Hard"])
        diff_combo.set("Medium")
        diff_combo.pack(padx=15, fill=tk.X)

        ttk.Label(dialog, text="Mind Map Concepts (one per line):").pack(anchor=tk.W, padx=15, pady=(8, 2))
        concepts_text = tk.Text(dialog, height=5, font=("Segoe UI", 9))
        concepts_text.pack(padx=15, fill=tk.X)

        ttk.Label(dialog, text="Flashcard Question & Answer (optional):").pack(anchor=tk.W, padx=15, pady=(8, 2))
        fc_q_entry = ttk.Entry(dialog, width=50)
        fc_q_entry.pack(padx=15, fill=tk.X, pady=(0, 4))
        fc_a_entry = ttk.Entry(dialog, width=50)
        fc_a_entry.pack(padx=15, fill=tk.X)

        ttk.Label(dialog, text="Notes:").pack(anchor=tk.W, padx=15, pady=(8, 2))
        notes_entry = ttk.Entry(dialog, width=50)
        notes_entry.pack(padx=15, fill=tk.X)

        def save_topic():
            s = subj_entry.get().strip()
            t = title_entry.get().strip()
            if not s or not t:
                messagebox.showerror("Validation Error", "Subject and Title are required.", parent=dialog)
                return

            d = diff_combo.get()
            raw_concepts = concepts_text.get("1.0", tk.END).strip().splitlines()
            nodes = [line.strip() for line in raw_concepts if line.strip()]

            flashcards = []
            if fc_q_entry.get().strip() and fc_a_entry.get().strip():
                flashcards.append({"question": fc_q_entry.get().strip(), "answer": fc_a_entry.get().strip()})

            self.manager.add_topic(
                subject=s,
                title=t,
                difficulty=d,
                mindmap_nodes=nodes,
                flashcards=flashcards,
                notes=notes_entry.get().strip()
            )
            self.storage.save_data(self.manager.get_all_topics())
            self.refresh_topics_table()
            dialog.destroy()
            messagebox.showinfo("Success", f"Topic '{t}' successfully added!")

        ttk.Button(dialog, text="Save Topic", command=save_topic).pack(pady=15)

    # -------------------------------------------------------------
    # Revision Session Handlers
    # -------------------------------------------------------------
    def _start_revision_session(self) -> None:
        due = self.manager.get_due_topics()
        if not due:
            if messagebox.askyesno("Revision", "No topics are currently overdue. Would you like to revise all topics anyway?"):
                self.session_topics = self.manager.get_all_topics()
            else:
                return
        else:
            self.session_topics = due

        self.current_session_index = 0
        self._load_session_item()

    def _load_session_item(self) -> None:
        if not self.session_topics or self.current_session_index >= len(self.session_topics):
            self.session_info_lbl.config(text="Revision session complete! All items revised.")
            self.rev_topic_lbl.config(text="Session Complete!")
            self.rev_meta_lbl.config(text="")
            self.rev_concepts_text.delete("1.0", tk.END)
            self.fc_q_lbl.config(text="")
            self.fc_a_lbl.config(text="")
            self.refresh_topics_table()
            return

        topic = self.session_topics[self.current_session_index]
        self.session_info_lbl.config(text=f"Item {self.current_session_index + 1} of {len(self.session_topics)}")
        self.rev_topic_lbl.config(text=f"[{topic.get('id')}] {topic.get('title')}")
        self.rev_meta_lbl.config(text=f"Subject: {topic.get('subject')} | Difficulty: {topic.get('difficulty')} | Current Confidence: {topic.get('confidence')}/5")

        self.rev_concepts_text.delete("1.0", tk.END)
        for n in topic.get("mindmap_nodes", []):
            self.rev_concepts_text.insert(tk.END, f"• {n}\n")

        self.current_card_index = 0
        self._show_current_flashcard(topic)

    def _show_current_flashcard(self, topic) -> None:
        cards = topic.get("flashcards", [])
        if cards and self.current_card_index < len(cards):
            card = cards[self.current_card_index]
            self.fc_q_lbl.config(text=f"Q ({self.current_card_index + 1}/{len(cards)}): {card.get('question')}")
            self.fc_a_lbl.config(text="")
        else:
            self.fc_q_lbl.config(text="(No flashcards attached for this topic)")
            self.fc_a_lbl.config(text="")

    def _reveal_flashcard_answer(self) -> None:
        if not self.session_topics or self.current_session_index >= len(self.session_topics):
            return
        topic = self.session_topics[self.current_session_index]
        cards = topic.get("flashcards", [])
        if cards and self.current_card_index < len(cards):
            self.fc_a_lbl.config(text=f"Answer: {cards[self.current_card_index].get('answer')}")

    def _next_flashcard(self) -> None:
        if not self.session_topics or self.current_session_index >= len(self.session_topics):
            return
        topic = self.session_topics[self.current_session_index]
        cards = topic.get("flashcards", [])
        if cards and self.current_card_index + 1 < len(cards):
            self.current_card_index += 1
            self._show_current_flashcard(topic)
        else:
            messagebox.showinfo("Flashcards", "All flashcards reviewed for this topic.")

    def _complete_current_topic(self) -> None:
        if not self.session_topics or self.current_session_index >= len(self.session_topics):
            return
        topic = self.session_topics[self.current_session_index]
        rating = self.rating_var.get()

        self.manager.complete_revision_session(topic["id"], rating)
        self.storage.save_data(self.manager.get_all_topics())

        self.current_session_index += 1
        self._load_session_item()

    # -------------------------------------------------------------
    # Exports
    # -------------------------------------------------------------
    def _export_txt(self) -> None:
        metrics = self.manager.get_summary_metrics()
        topics = self.manager.get_all_topics()
        ok, path = self.storage.export_text_report(metrics, topics)
        if ok:
            messagebox.showinfo("Export Success", f"TXT Report exported to:\n{path}")
        else:
            messagebox.showerror("Export Failed", path)

    def _export_html(self) -> None:
        topics = self.manager.get_all_topics()
        ok, path = self.storage.export_html_mindmap(topics, "All Subjects")
        if ok:
            messagebox.showinfo("Export Success", f"Visual HTML Mind Map generated!\nDouble-click to open in browser:\n{path}")
        else:
            messagebox.showerror("Export Failed", path)


def main():
    root = tk.Tk()
    app = MindMaprGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

