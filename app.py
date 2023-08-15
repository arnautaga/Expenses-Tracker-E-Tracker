import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import sqlite3
import os
import subprocess
import matplotlib.pyplot as plt

class ExpenseCalculatorWithLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Calculator with Login")

        self.initialize_database()

        self.login_frame = tk.Frame(root)
        self.login_frame.pack(padx=20, pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="e")

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="e")

        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=3, columnspan=2)

    def initialize_database(self):
        if not os.path.exists("expense_tracker.db"):
            conn = sqlite3.connect("expense_tracker.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    expense_type TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expense_types (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    type TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            conn.commit()
            conn.close()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter a username and password.")
            return

        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            self.user_id = user[0]
            self.open_expense_calculator()
        else:
            messagebox.showerror("Error", "Incorrect username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter a username and password.")
            return

        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        conn.close()

        messagebox.showinfo("Registration Successful", "User registered successfully.")

    def open_expense_calculator(self):
        self.root.destroy()

        self.expense_calculator = tk.Tk()
        self.expense_calculator.title("Expense Calculator")

        self.expenses = []
        self.total = 0.0

        self.description_label = tk.Label(self.expense_calculator, text="Expense Description:")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.expense_calculator)
        self.description_entry.pack()

        self.amount_label = tk.Label(self.expense_calculator, text="Expense Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.expense_calculator)
        self.amount_entry.pack()

        self.expense_type_combobox = ttk.Combobox(self.expense_calculator)
        self.expense_type_combobox.pack()

        self.add_expense_button = tk.Button(self.expense_calculator, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.add_expense_type_button = tk.Button(self.expense_calculator, text="Add Expense Type", command=self.add_expense_type)
        self.add_expense_type_button.pack()

        self.show_graph_button = tk.Button(self.expense_calculator, text="Show Graph", command=self.show_graph)
        self.show_graph_button.pack()

        self.expenses_text = tk.Text(self.expense_calculator, height=10, width=40)
        self.expenses_text.pack()

        self.update_expense_types()
        self.update_expenses()

    def add_expense_type(self):
        new_type = simpledialog.askstring("Add Expense Type", "Enter a new expense type:")
        if new_type:
            conn = sqlite3.connect("expense_tracker.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO expense_types (user_id, type) VALUES (?, ?)", (self.user_id, new_type))
            conn.commit()
            conn.close()

            self.update_expense_types()

    def update_expense_types(self):
        self.expense_type_combobox.set("")  # Clear the Combobox

        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT type FROM expense_types WHERE user_id=?", (self.user_id,))
        expense_types = [row[0] for row in cursor.fetchall()]

        conn.close()

        self.expense_type_combobox["values"] = expense_types

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        expense_type = self.expense_type_combobox.get()

        if description and amount and expense_type:
            try:
                amount = float(amount)
                self.expenses.append((description, amount))
                self.total += amount

                conn = sqlite3.connect("expense_tracker.db")
                cursor = conn.cursor()

                cursor.execute("INSERT INTO expenses (user_id, description, amount, expense_type) VALUES (?, ?, ?, ?)",
                               (self.user_id, description, amount, expense_type))

                conn.commit()
                conn.close()

                self.update_expenses()

                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")

    def update_expenses(self):
        self.expenses_text.delete(1.0, tk.END)

        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT description, amount, expense_type FROM expenses WHERE user_id=?", (self.user_id,))
        user_expenses = cursor.fetchall()

        conn.close()

        for description, amount, expense_type in user_expenses:
            self.expenses_text.insert(tk.END, f"{description} (${amount:.2f}) - {expense_type}\n")

    def show_graph(self):
        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT expense_type, SUM(amount) FROM expenses WHERE user_id=? GROUP BY expense_type", (self.user_id,))
        expense_data = cursor.fetchall()

        conn.close()

        categories = [data[0] for data in expense_data]
        amounts = [data[1] for data in expense_data]

        plt.bar(categories, amounts)
        plt.xlabel("Expense Types")
        plt.ylabel("Total Amount")
        plt.title("Expenses by Type")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def mainloop(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = ExpenseCalculatorWithLogin(root)
    app.mainloop()

if __name__ == "__main__":
    main()
