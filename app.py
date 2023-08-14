import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class ExpenseCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Gastos")

        self.expenses = []
        self.total = 0.0

        self.description_label = tk.Label(root, text="Descripción del Gasto:")
        self.description_label.pack()

        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.amount_label = tk.Label(root, text="Monto del Gasto:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.add_button = tk.Button(root, text="Agregar Gasto", command=self.add_expense)
        self.add_button.pack()

        self.show_graph_button = tk.Button(root, text="Mostrar Gráfico", command=self.show_graph)
        self.show_graph_button.pack()

        self.expenses_text = tk.Text(root, height=10, width=40)
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

                self.update_expenses()

                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido.")

    def update_expenses(self):
        self.expenses_text.delete(1.0, tk.END)
        for description, amount in self.expenses:
            self.expenses_text.insert(tk.END, f"{description}: ${amount:.2f}\n")

    def show_graph(self):
        categories = [expense[0] for expense in self.expenses]
        amounts = [expense[1] for expense in self.expenses]

        plt.bar(categories, amounts)
        plt.xlabel("Categorías")
        plt.ylabel("Monto")
        plt.title("Gastos por Categoría")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    root = tk.Tk()
    app = ExpenseCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
