import tkinter as tk
from tkinter import messagebox
from scipy.optimize import linprog

class SimplexCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Simplex Dual")
        self.root.withdraw()  # Ocultar la ventana principal al inicio a
        self.ask_variables_and_constraints()

    def ask_variables_and_constraints(self):
        self.var_window = tk.Toplevel(self.root)
        self.var_window.title("Configuración de Variables y Restricciones")

        tk.Label(self.var_window, text="Número de Variables:").grid(row=0, column=0, padx=10, pady=5)
        self.num_vars_entry = tk.Entry(self.var_window, width=10)
        self.num_vars_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.var_window, text="Número de Restricciones:").grid(row=1, column=0, padx=10, pady=5)
        self.num_constraints_entry = tk.Entry(self.var_window, width=10)
        self.num_constraints_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.var_window, text="Aceptar", command=self.create_widgets).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def create_widgets(self):
        try:
            self.num_vars = int(self.num_vars_entry.get())
            self.num_constraints = int(self.num_constraints_entry.get())
            self.var_window.destroy()
            self.root.deiconify()  # Mostrar la ventana principal después de configurar

            # Opción de Maximización/Minimización
            tk.Label(self.root, text="¿Qué desea realizar?").grid(row=0, column=0, padx=10, pady=5)
            self.objetive = tk.StringVar()
            self.objetive.set("Maximizar")
            tk.OptionMenu(self.root, self.objetive, "Maximizar", "Minimizar").grid(row=0, column=1, padx=10, pady=5)

            # Función objetivo
            tk.Label(self.root, text="Función Objetivo:").grid(row=1, column=0, padx=10, pady=5)
            self.objetive_entries = []
            for i in range(self.num_vars):
                entry = tk.Entry(self.root, width=10)
                entry.grid(row=1, column=2 * i + 1, padx=10, pady=5)
                self.objetive_entries.append(entry)
                tk.Label(self.root, text=f"X{i+1}").grid(row=1, column=2 * i + 2, padx=10, pady=5)
                if i < self.num_vars - 1:
                    tk.Label(self.root, text="+").grid(row=1, column=2 * i + 3, padx=10, pady=5)

            # Restricciones
            tk.Label(self.root, text="Restricciones:").grid(row=2, column=0, padx=10, pady=5)
            self.constraint_entries = []
            for j in range(self.num_constraints):
                row_entries = []
                for i in range(self.num_vars):
                    entry = tk.Entry(self.root, width=10)
                    entry.grid(row=3 + j, column=2 * i + 1, padx=10, pady=5)
                    row_entries.append(entry)
                    tk.Label(self.root, text=f"X{i+1}").grid(row=3 + j, column=2 * i + 2, padx=10, pady=5)
                    if i < self.num_vars - 1:
                        tk.Label(self.root, text="+").grid(row=3 + j, column=2 * i + 3, padx=10, pady=5)

                sign_var = tk.StringVar()
                sign_var.set("<=")
                tk.OptionMenu(self.root, sign_var, "<=", ">=", "=").grid(row=3 + j, column=2 * self.num_vars + 1, padx=10, pady=5)
                row_entries.append(sign_var)

                b_entry = tk.Entry(self.root, width=10)
                b_entry.grid(row=3 + j, column=2 * self.num_vars + 2, padx=10, pady=5)
                row_entries.append(b_entry)

                self.constraint_entries.append(row_entries)

            self.solve_button = tk.Button(self.root, text="Continuar", command=self.solve_simplex)
            self.solve_button.grid(row=3 + self.num_constraints, column=0, columnspan=2 * self.num_vars + 3, padx=10, pady=10)

            self.result_text = tk.Text(self.root, width=60, height=10, wrap="word")
            self.result_text.grid(row=4 + self.num_constraints, column=0, columnspan=2 * self.num_vars + 3, padx=10, pady=10)

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduzca números válidos para las variables y restricciones.")

    def solve_simplex(self):
        try:
            # Coeficientes de la función objetivo
            c = [float(entry.get()) for entry in self.objetive_entries]

            # Restricciones
            A_ub = []
            b_ub = []
            A_eq = []
            b_eq = []

            for row in self.constraint_entries:
                a_row = [float(entry.get()) for entry in row[:self.num_vars]]
                sign = row[self.num_vars].get()
                b = float(row[self.num_vars + 1].get())
                if sign == "<=":
                    A_ub.append(a_row)
                    b_ub.append(b)
                elif sign == ">=":
                    A_ub.append([-val for val in a_row])
                    b_ub.append(-b)
                elif sign == "=":
                    A_eq.append(a_row)
                    b_eq.append(b)

            if self.objetive.get() == "Maximizar":
                c = [-coeff for coeff in c]

            # Convertir listas vacías a None para linprog
            if not A_eq:
                A_eq = None
            if not b_eq:
                b_eq = None

            res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='simplex')

            self.result_text.delete(1.0, tk.END)
            if res.success:
                result = "Solución óptima encontrada:\n"
                result += f"Valores de las variables: {res.x}\n"
                result += f"Valor óptimo de la función objetivo: {-res.fun if self.objetive.get() == 'Maximizar' else res.fun}\n"
            else:
                result = "No se encontró una solución óptima."

            self.result_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplexCalculator(root)
    root.mainloop()
