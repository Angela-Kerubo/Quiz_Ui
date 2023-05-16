import json
import tkinter as tk
from tkinter import messagebox

class QuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game")
        self.master.configure(bg="black")  # Set background color

        self.quiz_data = self.load_quiz_data("quiz.json")
        self.current_question = 0
        self.score = 0
        self.user_answers = []

        self.question_label = tk.Label(self.master, text="", wraplength=400, bg="grey", font=("Arial", 16, "bold"))
        self.question_label.pack(pady=20, fill=tk.BOTH, expand=True)

        self.options_listbox = tk.Listbox(
            self.master,
            selectmode=tk.SINGLE,
            bg="grey",
            font=("Arial", 14),
            justify=tk.CENTER,
            exportselection=False,
        )
        self.options_listbox.pack(pady=20, fill=tk.BOTH, expand=True)

        self.previous_button = tk.Button(
            self.master, text="Previous", command=self.previous_question, bg="#2196f3", fg="#ffffff", font=("Arial", 12, "bold")
        )
        self.previous_button.place(relx=0.4, rely=0.7, anchor='w',)

        self.next_button = tk.Button(
            self.master, text="Next", command=self.next_question, bg="#4caf50", fg="#ffffff", font=("Arial", 12, "bold")
        )
        self.next_button.place(relx=0.6, rely=0.7, anchor='e',)

        self.load_question()

    def load_quiz_data(self, file_path):
        with open(file_path) as file:
            quiz_data = json.load(file)
        return quiz_data

    def load_question(self):
        question = self.quiz_data["questions"][self.current_question]
        self.question_label.config(text=question["question"])

        self.options_listbox.delete(0, tk.END)
        for option in question["options"]:
            self.options_listbox.insert(tk.END, option)

        # Select the user's previous answer if available
        if len(self.user_answers) > self.current_question and self.user_answers[self.current_question] in question["options"]:
            self.options_listbox.select_set(question["options"].index(self.user_answers[self.current_question]))
        else:
            self.options_listbox.selection_clear(0, tk.END)

    def previous_question(self):
        if self.current_question == 0:
            return

        self.current_question -= 1
        self.load_question()

    def next_question(self):
        if self.options_listbox.curselection() == ():
            messagebox.showerror("Error", "Please select an answer.")
            return

        user_answer = self.options_listbox.get(self.options_listbox.curselection())
        question = self.quiz_data["questions"][self.current_question]
        if user_answer.lower() == question["answer"].lower():
            self.score += 1
        self.user_answers.append(user_answer)

        self.current_question += 1

        if self.current_question < len(self.quiz_data["questions"]):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        result_message = f"You've completed the quiz!\nYour score: {self.score}/{len(self.quiz_data['questions'])}\n\n"
        for i, question in enumerate(self.quiz_data["questions"]):
            result_message += f"Question {i + 1}: {question['question']}\n"
            result_message += f"Your answer: {self.user_answers[i]}\n"
            result_message += f"Correct answer: {question['answer']}\n\n"

        messagebox.showinfo("Quiz result", result_message)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#f2f2f2")  # Set background color of the window
    quiz_game = QuizGame(root)
    quiz_game.load_question()
    root.mainloop()


