import json
import tkinter as tk
from tkinter import messagebox


class QuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game")
        self.master.configure(bg="#f2f2f2")  # Set background color

        self.quiz_data = self.load_quiz_data("quiz.json")
        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(self.master, text="", wraplength=400, bg="#f2f2f2", font=("Arial", 14, "bold"))
        self.question_label.pack(pady=20)

        self.options_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, bg="#ffffff", font=("Arial", 12))
        self.options_listbox.pack(pady=10)

        self.next_button = tk.Button(self.master, text="Next", command=self.next_question, bg="#4caf50", fg="#ffffff", font=("Arial", 12, "bold"))
        self.next_button.pack(pady=10)

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

    def next_question(self):
        if self.options_listbox.curselection() == ():
            messagebox.showerror("Error", "Please select an answer.")
            return

        user_answer = self.options_listbox.get(self.options_listbox.curselection())
        question = self.quiz_data["questions"][self.current_question]
        if user_answer.lower() == question["answer"].lower():
            self.score += 1

        self.current_question += 1

        if self.current_question < len(self.quiz_data["questions"]):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        messagebox.showinfo("Quiz Result", f"You've completed the quiz!\nYour score: {self.score}")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#f2f2f2")  # Set background color of the window
    quiz_game = QuizGame(root)
    quiz_game.load_question()
    root.mainloop()


