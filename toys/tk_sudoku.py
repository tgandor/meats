import tkinter as tk
from tkinter import messagebox
import pycosat
from itertools import combinations, chain
import time


def var_to_val(var):
    var -= 1
    return var // 81, var // 9 % 9, var % 9


def val_to_var(row, col, val):
    return 81 * row + 9 * col + val + 1


def one_and_only_one(values):
    yield values
    for a, b in combinations(values, 2):
        yield [-a, -b]


def build_sudoku_clauses():
    # Generowanie bazowych klauzul tylko raz dla wydajności
    def one_digit_per_field():
        for row in range(9):
            for col in range(9):
                yield from one_and_only_one(
                    [val_to_var(row, col, val) for val in range(9)]
                )

    def one_digit_per_row():
        for col in range(9):
            for val in range(9):
                yield from one_and_only_one(
                    [val_to_var(row, col, val) for row in range(9)]
                )

    def one_digit_per_col():
        for row in range(9):
            for val in range(9):
                yield from one_and_only_one(
                    [val_to_var(row, col, val) for col in range(9)]
                )

    def square(sx, sy):
        for row in range(3 * sx, 3 * sx + 3):
            for col in range(3 * sy, 3 * sy + 3):
                yield row, col

    def one_digit_per_square():
        for sx in range(3):
            for sy in range(3):
                for val in range(9):
                    yield from one_and_only_one(
                        [val_to_var(row, col, val) for row, col in square(sx, sy)]
                    )

    return list(
        chain(
            one_digit_per_field(),
            one_digit_per_row(),
            one_digit_per_col(),
            one_digit_per_square(),
        )
    )


BASE_CLAUSES = build_sudoku_clauses()


def solve_sudoku_logic(grid_matrix):
    """
    Przyjmuje listę list 9x9 (int), gdzie 0 to puste pole.
    Zwraca rozwiązaną macierz lub None.
    """
    clauses = BASE_CLAUSES[:]

    # Dodaj ustalone cyfry jako klauzule
    for r in range(9):
        for c in range(9):
            val = grid_matrix[r][c]
            if val != 0:
                clauses.append([val_to_var(r, c, val - 1)])

    # Rozwiąż używając pycosat
    solution = pycosat.solve(clauses)

    if solution == "UNSAT":
        return None

    # Odtwórz wynik
    result_grid = [[0] * 9 for _ in range(9)]
    for var in solution:
        if var > 0:
            r, c, v = var_to_val(var)
            result_grid[r][c] = v + 1

    return result_grid


# --- INTERFEJS GRAFICZNY (GUI) ---


class ModernSudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Sudoku Solver")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e1e")  # Ciemne tło

        # Kolorystyka
        self.COLORS = {
            "bg": "#1e1e1e",
            "cell_bg": "#2d2d2d",
            "cell_fg": "#ffffff",
            "highlight": "#3e3e3e",
            "accent": "#007acc",  # Niebieski akcent
            "solve_btn": "#4caf50",  # Zielony
            "clear_btn": "#f44336",  # Czerwony
            "solved_fg": "#4caf50",  # Kolor cyfr rozwiązania
            "user_fg": "#ffffff",  # Kolor cyfr wpisanych przez użytkownika
            "grid_line": "#555555",
        }

        self.cells = {}  # Słownik przechowujący widgety komórek: (row, col) -> Label
        self.grid_data = [[0 for _ in range(9)] for _ in range(9)]  # Dane logiczne
        self.selected_cell = None  # Aktualnie wybrana komórka (row, col)

        self._setup_ui()

    def _setup_ui(self):
        # Główny kontener
        main_frame = tk.Frame(self.root, bg=self.COLORS["bg"])
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # -- Lewa strona: Plansza Sudoku --
        board_frame = tk.Frame(main_frame, bg=self.COLORS["grid_line"], padx=2, pady=2)
        board_frame.pack(side="left", padx=20)

        # Budowanie siatki 9x9
        for r in range(9):
            for c in range(9):
                # Obliczanie odstępów dla bloków 3x3
                pad_top = 1 if r % 3 == 0 and r != 0 else 0
                pad_left = 1 if c % 3 == 0 and c != 0 else 0

                # Kontener dla komórki (dla efektu obramowania)
                cell_frame = tk.Frame(board_frame, bg=self.COLORS["grid_line"], bd=0)
                cell_frame.grid(
                    row=r, column=c, padx=(1 + pad_left, 1), pady=(1 + pad_top, 1)
                )

                # Sama komórka (Label działający jak przycisk)
                lbl = tk.Label(
                    cell_frame,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    width=2,
                    height=1,
                    bg=self.COLORS["cell_bg"],
                    fg=self.COLORS["cell_fg"],
                    relief="flat",
                )
                lbl.pack()

                # Bindowanie kliknięcia
                lbl.bind(
                    "<Button-1>", lambda e, row=r, col=c: self.select_cell(row, col)
                )
                self.cells[(r, c)] = lbl

        # -- Prawa strona: Panel Sterowania --
        control_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        control_frame.pack(side="right", fill="y", padx=20)

        # Tytuł
        tk.Label(
            control_frame,
            text="SUDOKU\nSOLVER",
            font=("Helvetica", 30, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["accent"],
            justify="left",
        ).pack(pady=(0, 30), anchor="w")

        # Klawiatura numeryczna
        numpad_frame = tk.Frame(control_frame, bg=self.COLORS["bg"])
        numpad_frame.pack(pady=10)

        btn_params = {
            "font": ("Helvetica", 14),
            "width": 4,
            "height": 1,
            "bg": self.COLORS["highlight"],
            "fg": "white",
            "relief": "flat",
            "activebackground": self.COLORS["accent"],
            "activeforeground": "white",
        }

        # Cyfry 1-9
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i, num in enumerate(nums):
            btn = tk.Button(
                numpad_frame,
                text=str(num),
                **btn_params,
                command=lambda n=num: self.set_number(n)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        # Przycisk czyszczenia komórki (X)
        btn_del = tk.Button(
            numpad_frame, text="⌫", **btn_params, command=lambda: self.set_number(0)
        )
        btn_del.grid(row=3, column=1, padx=5, pady=5)

        # Przyciski akcji
        action_frame = tk.Frame(control_frame, bg=self.COLORS["bg"])
        action_frame.pack(pady=30, fill="x")

        solve_btn = tk.Button(
            action_frame,
            text="ROZWIĄŻ",
            font=("Helvetica", 14, "bold"),
            bg=self.COLORS["solve_btn"],
            fg="white",
            relief="flat",
            height=2,
            command=self.solve_action,
        )
        solve_btn.pack(fill="x", pady=5)

        reset_btn = tk.Button(
            action_frame,
            text="RESETUJ",
            font=("Helvetica", 12),
            bg=self.COLORS["clear_btn"],
            fg="white",
            relief="flat",
            command=self.reset_board,
        )
        reset_btn.pack(fill="x", pady=5)

        # Obsługa klawiatury fizycznej
        self.root.bind("<Key>", self.handle_keypress)

    def select_cell(self, r, c):
        # Resetuj tło poprzedniej komórki (jeśli nie jest to ta sama)
        if self.selected_cell:
            pr, pc = self.selected_cell
            self.cells[(pr, pc)].config(bg=self.COLORS["cell_bg"])

        self.selected_cell = (r, c)
        # Podświetl nową
        self.cells[(r, c)].config(bg=self.COLORS["accent"])

    def set_number(self, num):
        if not self.selected_cell:
            return

        r, c = self.selected_cell
        val = int(num)
        self.grid_data[r][c] = val

        text = str(val) if val > 0 else ""
        # Ustawiamy kolor: Biały dla wprowadzonych przez użytkownika
        self.cells[(r, c)].config(text=text, fg=self.COLORS["user_fg"])

    def handle_keypress(self, event):
        if not self.selected_cell:
            return

        char = event.char
        if char.isdigit() and char != "0":
            self.set_number(int(char))
        elif event.keysym in ["BackSpace", "Delete", "0"]:
            self.set_number(0)

        # Nawigacja strzałkami
        r, c = self.selected_cell
        if event.keysym == "Up":
            r = (r - 1) % 9
        elif event.keysym == "Down":
            r = (r + 1) % 9
        elif event.keysym == "Left":
            c = (c - 1) % 9
        elif event.keysym == "Right":
            c = (c + 1) % 9
        self.select_cell(r, c)

    def reset_board(self):
        self.grid_data = [[0] * 9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].config(
                    text="", fg=self.COLORS["user_fg"], bg=self.COLORS["cell_bg"]
                )
        self.selected_cell = None

    def solve_action(self):
        # Zbieranie danych
        input_grid = [row[:] for row in self.grid_data]

        # Rozwiązywanie
        solution = solve_sudoku_logic(input_grid)

        if solution:
            self.animate_solution(input_grid, solution)
        else:
            messagebox.showerror(
                "Błąd", "To Sudoku nie ma rozwiązania lub jest sprzeczne!"
            )

    def animate_solution(self, original, solved, idx=0):
        """Rekurencyjna funkcja do animowania wypełniania"""
        if idx >= 81:
            return

        r, c = idx // 9, idx % 9

        # Jeśli w oryginale było 0 (puste), to wstawiamy cyfrę z rozwiązania
        if original[r][c] == 0:
            val = solved[r][c]
            self.cells[(r, c)].config(text=str(val), fg=self.COLORS["solved_fg"])
            # Odśwież GUI i czekaj chwilę dla efektu "fali"
            self.root.update()
            # Opóźnienie dynamiczne - im dalej, tym szybciej, albo stałe
            time.sleep(0.02)

        # Wywołaj dla następnej komórki
        self.root.after(1, lambda: self.animate_solution(original, solved, idx + 1))


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSudokuApp(root)
    root.mainloop()
