import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from difflib import SequenceMatcher
import re

root = tk.Tk()
root.title("Hallucination Benchmark - Testing Free AI Chatbots")
root.geometry("1000x720")
root.minsize(850, 620)
results = []

tk.Label(root, text="Hallucination Benchmark", font=("Arial", 20, "bold")).pack(pady=(12, 2))
tk.Label(root, text="Testing Free AI Chatbots").pack()

form = tk.Frame(root)
form.pack(pady=12)
labels = ["Question", "Chatbot Name", "Chatbot Answer", "Reference Answer"]
entries = []

for i, label in enumerate(labels):
    tk.Label(form, text=label).grid(row=i, column=0, padx=8, pady=5, sticky="w")
    entry = tk.Entry(form, width=72)
    entry.grid(row=i, column=1, padx=8, pady=5)
    entries.append(entry)

status = ttk.Combobox(
    form, values=["Correct", "Incorrect", "Needs Review"],
    state="readonly", width=68
)
status.set("Needs Review")
tk.Label(form, text="Fact-check Result").grid(row=4, column=0, padx=8, pady=5, sticky="w")
status.grid(row=4, column=1, padx=8, pady=5, sticky="w")

comparison_label = tk.Label(
    root,
    text="Answer comparison: Enter both answers, then click Compare Answers.",
    wraplength=900
)
comparison_label.pack(pady=5)

def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())

def compare_answers():
    chatbot_answer = entries[2].get().strip()
    reference_answer = entries[3].get().strip()
    if not chatbot_answer or not reference_answer:
        messagebox.showwarning("Missing Answers", "Enter both Chatbot Answer and Reference Answer first.")
        return

    a, b = normalize(chatbot_answer), normalize(reference_answer)
    similarity = SequenceMatcher(None, a, b).ratio() * 100
    if a == b:
        status.set("Correct")
        note = "The answers match exactly after basic text cleanup."
    else:
        status.set("Needs Review")
        note = "The wording differs. Please check the meaning manually."

    comparison_label.config(
        text=f"Text similarity: {similarity:.1f}% | {note} "
             "Similarity is only a clue, not proof of factual correctness."
    )

columns = ("Question", "Chatbot", "Result")
table = ttk.Treeview(root, columns=columns, show="headings", height=9)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=310)
table.pack(padx=12, pady=10, fill="both", expand=True)

def add_result():
    values = [entry.get().strip() for entry in entries]
    if not all(values):
        messagebox.showwarning("Missing Information", "Please fill in all four fields.")
        return

    result = status.get()
    table.insert("", "end", values=(values[0], values[1], result))
    results.append([values[0], values[1], values[2], values[3], result])

    total = len(results)
    correct = sum(1 for row in results if row[4] == "Correct")
    incorrect = sum(1 for row in results if row[4] == "Incorrect")
    checked = correct + incorrect
    accuracy = (correct / checked * 100) if checked else 0
    score.config(
        text=f"Total: {total} | Correct: {correct} | Incorrect: {incorrect} | "
             f"Needs Review: {total - checked} | Accuracy (checked only): {accuracy:.1f}%"
    )

    for entry in entries:
        entry.delete(0, tk.END)
    status.set("Needs Review")
    comparison_label.config(text="Answer comparison: Enter both answers, then click Compare Answers.")

def save_csv():
    if not results:
        messagebox.showwarning("No Results", "Add at least one result before saving.")
        return
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="benchmark_results.csv"
    )
    if filename:
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Question", "Chatbot", "Chatbot Answer",
                "Reference Answer", "Fact-check Result"
            ])
            writer.writerows(results)
        messagebox.showinfo("Saved", "Results saved successfully!")

buttons = tk.Frame(root)
buttons.pack(pady=5)
tk.Button(buttons, text="Compare Answers", command=compare_answers, width=18).pack(side="left", padx=6)
tk.Button(buttons, text="Add Checked Result", command=add_result, width=20).pack(side="left", padx=6)
tk.Button(buttons, text="Save Results to CSV", command=save_csv, width=20).pack(side="left", padx=6)

score = tk.Label(
    root,
    text="Total: 0 | Correct: 0 | Incorrect: 0 | Needs Review: 0 | Accuracy (checked only): 0%"
)
score.pack(pady=(8, 12))
root.mainloop()
