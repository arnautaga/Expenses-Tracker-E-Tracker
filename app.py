import tkinter as tk
from tkinter import messagebox
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
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            conn.commit()

            conn.close()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario y contraseña.")
            return

        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            self.user_id = user[0]  # Guardar el ID del usuario actual
            self.open_expense_calculator()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario y contraseña.")
            return

        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        conn.close()

        messagebox.showinfo("Registro Exitoso", "Usuario registrado correctamente.")

    def open_expense_calculator(self):
        self.root.destroy()  # Cerrar la ventana de inicio de sesión

        # Crear la ventana de la calculadora de gastos
        self.expense_calculator = tk.Tk()
        self.expense_calculator.title("Calculadora de Gastos")

        self.expenses = []
        self.total = 0.0

        self.description_label = tk.Label(self.expense_calculator, text="Descripción del Gasto:")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.expense_calculator)
        self.description_entry.pack()

        self.amount_label = tk.Label(self.expense_calculator, text="Monto del Gasto:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.expense_calculator)
        self.amount_entry.pack()

        self.add_button = tk.Button(self.expense_calculator, text="Agregar Gasto", command=self.add_expense)
        self.add_button.pack()

        self.show_graph_button = tk.Button(self.expense_calculator, text="Mostrar Gráfico", command=self.show_graph)
        self.show_graph_button.pack()

        self.expenses_text = tk.Text(self.expense_calculator, height=10, width=40)
        self.expenses_text.pack()

        self.update_expenses()

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        if description and amount:
            try:
                amount = float(amount)
                self.expenses.append((description, amount))
                self.total += amount

                # Agregar el gasto a la base de datos
                conn = sqlite3.connect("expense_tracker.db")
                cursor = conn.cursor()

                cursor.execute("INSERT INTO expenses (user_id, description, amount) VALUES (?, ?, ?)",
                           (self.user_id, description, amount))

                conn.commit()
                conn.close()

                self.update_expenses()

                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido.")

    def update_expenses(self):
        # Limpiar el campo de texto de gastos
        self.expenses_text.delete(1.0, tk.END)

        # Obtener los gastos del usuario de la base de datos
        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT description, amount FROM expenses WHERE user_id=?", (self.user_id,))
        user_expenses = cursor.fetchall()

        conn.close()

        # Mostrar los gastos en el campo de texto
        for description, amount in user_expenses:
            self.expenses_text.insert(tk.END, f"{description}: ${amount:.2f}\n")

    def show_graph(self):
        # Obtener los gastos y ganancias del usuario de la base de datos
        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT description, amount FROM expenses WHERE user_id=?", (self.user_id,))
        user_expenses = cursor.fetchall()

        conn.close()

        categories = [expense[0] for expense in user_expenses]
        amounts = [expense[1] for expense in user_expenses]

        plt.bar(categories, amounts)
        plt.xlabel("Categorías")
        plt.ylabel("Monto")
        plt.title("Gastos por Categoría")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    root = tk.Tk()
    app = ExpenseCalculatorWithLogin(root)
    root.mainloop()

if __name__ == "__main__":
    # Instalar dependencias necesarias
    subprocess.run(["pip3", "install", "pysqlite3", "matplotlib"])

    main()
