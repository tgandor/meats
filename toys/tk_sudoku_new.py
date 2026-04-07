import sys
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
    Zwraca (rozwiązana_macierz_lub_None, is_unique).
    is_unique=True oznacza dokładnie jedno rozwiązanie.
    """
    clauses = BASE_CLAUSES[:]

    for r in range(9):
        for c in range(9):
            val = grid_matrix[r][c]
            if val != 0:
                clauses.append([val_to_var(r, c, val - 1)])

    solution = pycosat.solve(clauses)

    if solution == "UNSAT":
        return None, True

    result_grid = [[0] * 9 for _ in range(9)]
    for var in solution:
        if var > 0:
            r, c, v = var_to_val(var)
            result_grid[r][c] = v + 1

    blocking_clause = [-v for v in solution]
    clauses.append(blocking_clause)
    second = pycosat.solve(clauses)
    is_unique = (second == "UNSAT")

    return result_grid, is_unique


# ── cell canvas geometry ─────────────────────────────────────────────────────

CELL_SIZE = 48
BIG_FONT = ("Helvetica", 22, "bold")
MARK_FONT = ("Helvetica", 9)

# Mark types
MARK_DIGIT = "digit"
MARK_DOT = "dot"
MARK_VLINE = "vline"
MARK_HLINE = "hline"

_MARK_SYMBOLS = {
    MARK_DOT: "•",    # U+2022 bullet
    MARK_VLINE: "|",
    MARK_HLINE: "−",  # U+2212 minus sign
}


def mark_symbol(digit, mark_type):
    if mark_type == MARK_DIGIT:
        return str(digit)
    return _MARK_SYMBOLS.get(mark_type, "")


def mark_xy(digit):
    """Returns (x, y) pixel position inside a CELL_SIZE×CELL_SIZE canvas for digit 1-9."""
    col = (digit - 1) % 3
    row = (digit - 1) // 3
    x = (col + 0.5) * CELL_SIZE / 3
    y = (row + 0.5) * CELL_SIZE / 3
    return x, y


# --- INTERFEJS GRAFICZNY (GUI) ---


class ModernSudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Sudoku Solver")
        self.root.configure(bg="#1e1e1e")

        self.COLORS = {
            "bg": "#1e1e1e",
            "cell_bg": "#2d2d2d",
            "highlight": "#3e3e3e",
            "accent": "#007acc",
            "solve_btn": "#4caf50",
            "clear_btn": "#f44336",
            "check_btn": "#ff9800",
            "solved_fg": "#4caf50",
            "user_fg": "#ffffff",
            "preset_fg": "#87ceeb",
            "violation_fg": "#ff4444",
            "wrong_fg": "#ff8800",
            "mark_fg": "#999999",
            "grid_line": "#555555",
        }

        self.cells = {}          # (r, c) -> tk.Canvas
        self.grid_data = [[0] * 9 for _ in range(9)]
        self.selected_cell = None
        self.preset_cells = set()
        self.solved_cells = set()
        self.wrong_cells = set()
        # marks[r][c] = dict  digit -> mark_type  (only for empty cells)
        self.marks = [[{} for _ in range(9)] for _ in range(9)]
        self.mark_mode = None    # None | MARK_DIGIT | MARK_DOT | MARK_VLINE | MARK_HLINE
        self.check_rules_var = tk.BooleanVar(value=False)

        self._setup_ui()

        if len(sys.argv) > 1:
            self.load_puzzle_from_file(sys.argv[1])

    # ── rendering ────────────────────────────────────────────────────────────

    def _get_fg_color(self, r, c, violations=None):
        if (r, c) in self.preset_cells:
            return self.COLORS["preset_fg"]
        if (r, c) in self.solved_cells:
            return self.COLORS["solved_fg"]
        if (r, c) in self.wrong_cells:
            return self.COLORS["wrong_fg"]
        if self.check_rules_var.get():
            if violations is None:
                violations = self._find_violations()
            if (r, c) in violations:
                return self.COLORS["violation_fg"]
        return self.COLORS["user_fg"]

    def _redraw_cell(self, r, c, violations=None):
        canvas = self.cells[(r, c)]
        canvas.delete("all")
        val = self.grid_data[r][c]
        if val != 0:
            canvas.create_text(
                CELL_SIZE // 2, CELL_SIZE // 2,
                text=str(val),
                font=BIG_FONT,
                fill=self._get_fg_color(r, c, violations),
            )
        else:
            for digit, mtype in self.marks[r][c].items():
                x, y = mark_xy(digit)
                canvas.create_text(
                    x, y,
                    text=mark_symbol(digit, mtype),
                    font=MARK_FONT,
                    fill=self.COLORS["mark_fg"],
                )

    def _redraw_all(self, violations=None):
        if violations is None and self.check_rules_var.get():
            violations = self._find_violations()
        for r in range(9):
            for c in range(9):
                self._redraw_cell(r, c, violations)

    # ── UI setup ─────────────────────────────────────────────────────────────

    def _setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.COLORS["bg"])
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Board
        board_frame = tk.Frame(main_frame, bg=self.COLORS["grid_line"], padx=2, pady=2)
        board_frame.pack(side="left", padx=20)

        for r in range(9):
            for c in range(9):
                pad_top = 3 if r % 3 == 0 and r != 0 else 0
                pad_left = 3 if c % 3 == 0 and c != 0 else 0

                cell_frame = tk.Frame(board_frame, bg=self.COLORS["grid_line"], bd=0)
                cell_frame.grid(
                    row=r, column=c,
                    padx=(1 + pad_left, 1),
                    pady=(1 + pad_top, 1),
                )

                canvas = tk.Canvas(
                    cell_frame,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    bg=self.COLORS["cell_bg"],
                    highlightthickness=0,
                )
                canvas.pack()
                canvas.bind("<Button-1>", lambda e, row=r, col=c: self.select_cell(row, col))
                canvas.bind("<Button-3>", lambda e, row=r, col=c: self._start_mark_mode(row, col, MARK_DIGIT))
                self.cells[(r, c)] = canvas

        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        control_frame.pack(side="right", fill="y", padx=20)

        tk.Label(
            control_frame,
            text="SUDOKU\nSOLVER",
            font=("Helvetica", 30, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["accent"],
            justify="left",
        ).pack(pady=(0, 30), anchor="w")

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

        for i, num in enumerate(range(1, 10)):
            tk.Button(
                numpad_frame,
                text=str(num),
                **btn_params,
                command=lambda n=num: self.set_number(n),
            ).grid(row=i // 3, column=i % 3, padx=5, pady=5)

        tk.Button(
            numpad_frame, text="⌫", **btn_params, command=lambda: self.set_number(0)
        ).grid(row=3, column=1, padx=5, pady=5)

        action_frame = tk.Frame(control_frame, bg=self.COLORS["bg"])
        action_frame.pack(pady=20, fill="x")

        tk.Button(
            action_frame,
            text="ROZWIĄŻ",
            font=("Helvetica", 14, "bold"),
            bg=self.COLORS["solve_btn"],
            fg="white", relief="flat", height=2,
            command=self.solve_action,
        ).pack(fill="x", pady=5)

        tk.Button(
            action_frame,
            text="RESETUJ",
            font=("Helvetica", 12),
            bg=self.COLORS["clear_btn"],
            fg="white", relief="flat",
            command=self.reset_board,
        ).pack(fill="x", pady=5)

        tk.Button(
            action_frame,
            text="SPRAWDŹ",
            font=("Helvetica", 12),
            bg=self.COLORS["check_btn"],
            fg="white", relief="flat",
            command=self.check_action,
        ).pack(fill="x", pady=5)

        tk.Checkbutton(
            control_frame,
            text="Sprawdzaj reguły",
            variable=self.check_rules_var,
            command=self._on_check_rules_toggle,
            bg=self.COLORS["bg"], fg="white",
            selectcolor=self.COLORS["highlight"],
            activebackground=self.COLORS["bg"],
            activeforeground="white",
            font=("Helvetica", 11),
        ).pack(anchor="w", pady=(10, 0))

        tk.Button(
            control_frame,
            text="?",
            font=("Helvetica", 12, "bold"),
            bg=self.COLORS["highlight"],
            fg="white",
            relief="flat",
            width=3,
            command=self._show_help,
        ).pack(anchor="w", pady=(14, 0))

        self.root.bind("<Key>", self.handle_keypress)

    # ── cell selection ───────────────────────────────────────────────────────

    def select_cell(self, r, c):
        if self.selected_cell:
            pr, pc = self.selected_cell
            self.cells[(pr, pc)].config(bg=self.COLORS["cell_bg"])
        self.selected_cell = (r, c)
        self.cells[(r, c)].config(bg=self.COLORS["accent"])
        self.mark_mode = None
        self.root.focus_set()  # return keyboard focus to root so <Key> binding fires

    # ── number input ─────────────────────────────────────────────────────────

    def set_number(self, num):
        if not self.selected_cell:
            return
        r, c = self.selected_cell
        if (r, c) in self.preset_cells:
            return

        val = int(num)
        self.grid_data[r][c] = val
        self.marks[r][c].clear()
        self.wrong_cells.discard((r, c))
        self.solved_cells.discard((r, c))

        if val != 0:
            self._cleanup_marks_for_digit(r, c, val)

        violations = self._find_violations() if self.check_rules_var.get() else None
        self._redraw_cell(r, c, violations)
        if violations is not None:
            # Refresh all cells so violation highlights stay consistent
            for rr in range(9):
                for cc in range(9):
                    if (rr, cc) != (r, c) and self.grid_data[rr][cc] != 0:
                        self._redraw_cell(rr, cc, violations)

    def _cleanup_marks_for_digit(self, r, c, digit):
        """Remove marks for `digit` from every peer (same row, col, 3×3 box)."""
        box_r, box_c = 3 * (r // 3), 3 * (c // 3)
        peers = set(
            [(r, cc) for cc in range(9)]
            + [(rr, c) for rr in range(9)]
            + [(rr, cc)
               for rr in range(box_r, box_r + 3)
               for cc in range(box_c, box_c + 3)]
        )
        for rr, cc in peers:
            if digit in self.marks[rr][cc]:
                del self.marks[rr][cc][digit]
                if self.grid_data[rr][cc] == 0:
                    self._redraw_cell(rr, cc)

    def _show_help(self):
        messagebox.showinfo(
            "Znaczniki",
            "PPM na komórce lub ? + cyfra  →  mała cyfra\n"
            ". + cyfra                      →  · (kropka)\n"
            r"\ lub | lub / + cyfra         →  | (pionowa kreska)" + "\n"
            "- lub _ lub = + cyfra          →  − (pozioma kreska)\n"
            "\nPonowne wpisanie tego samego znacznika — usuwa go.\n"
            "Wpisanie cyfry usuwa konfliktujące znaczniki "
            "z wiersza, kolumny i bloku.",
        )

    # ── mark input ───────────────────────────────────────────────────────────

    def _start_mark_mode(self, r, c, mode):
        self.select_cell(r, c)
        self.mark_mode = mode

    def _set_mark(self, digit, mark_type):
        if not self.selected_cell:
            return
        r, c = self.selected_cell
        if (r, c) in self.preset_cells or self.grid_data[r][c] != 0:
            return
        marks = self.marks[r][c]
        if marks.get(digit) == mark_type:
            del marks[digit]       # toggle off
        else:
            marks[digit] = mark_type
        self._redraw_cell(r, c)

    # ── keyboard ─────────────────────────────────────────────────────────────

    def handle_keypress(self, event):
        if not self.selected_cell:
            return

        char = event.char

        # Consume pending mark mode prefix
        if self.mark_mode is not None:
            if char.isdigit() and char != "0":
                self._set_mark(int(char), self.mark_mode)
            self.mark_mode = None
            return

        if char.isdigit() and char != "0":
            self.set_number(int(char))
            return
        if event.keysym in ("BackSpace", "Delete") or char == "0":
            self.set_number(0)
            return

        # Mark-mode prefix keys
        if char == "?":
            self.mark_mode = MARK_DIGIT
            return
        if char == ".":
            self.mark_mode = MARK_DOT
            return
        if char in r"\|/":
            self.mark_mode = MARK_VLINE
            return
        if char in "-_=":
            self.mark_mode = MARK_HLINE
            return

        # Arrow navigation (runs even after digit input, intentionally)
        r, c = self.selected_cell
        if event.keysym == "Up":
            r = (r - 1) % 9
        elif event.keysym == "Down":
            r = (r + 1) % 9
        elif event.keysym == "Left":
            c = (c - 1) % 9
        elif event.keysym == "Right":
            c = (c + 1) % 9
        else:
            return
        self.select_cell(r, c)

    # ── board management ─────────────────────────────────────────────────────

    def reset_board(self):
        if self.solved_cells:
            # Level 1: remove only algorithm-filled cells
            for r, c in self.solved_cells:
                self.grid_data[r][c] = 0
                self._redraw_cell(r, c)
            self.solved_cells.clear()
        elif any(
            self.grid_data[r][c] != 0 or bool(self.marks[r][c])
            for r in range(9)
            for c in range(9)
            if (r, c) not in self.preset_cells
        ):
            # Level 2: remove user digits and user marks, keep presets
            for r in range(9):
                for c in range(9):
                    if (r, c) not in self.preset_cells:
                        was_filled = self.grid_data[r][c] != 0 or bool(self.marks[r][c])
                        self.grid_data[r][c] = 0
                        self.marks[r][c].clear()
                        if was_filled:
                            self._redraw_cell(r, c)
            self.wrong_cells.clear()
        else:
            # Level 3: wipe everything
            self.grid_data = [[0] * 9 for _ in range(9)]
            self.marks = [[{} for _ in range(9)] for _ in range(9)]
            self.preset_cells.clear()
            self.solved_cells.clear()
            self.wrong_cells.clear()
            for r in range(9):
                for c in range(9):
                    self.cells[(r, c)].config(bg=self.COLORS["cell_bg"])
                    self._redraw_cell(r, c)

        self.selected_cell = None
        self.mark_mode = None

    # ── solving ──────────────────────────────────────────────────────────────

    def solve_action(self):
        input_grid = [row[:] for row in self.grid_data]
        solution, is_unique = solve_sudoku_logic(input_grid)

        if solution is None:
            messagebox.showerror("Błąd", "To Sudoku nie ma rozwiązania lub jest sprzeczne!")
            return

        if not is_unique:
            messagebox.showwarning(
                "Wiele rozwiązań",
                "To Sudoku jest niedookreślone — istnieje wiele rozwiązań.\n"
                "Poniżej pokazano jedno z możliwych.",
            )
        self.wrong_cells.clear()
        self.solved_cells.clear()
        self.animate_solution(input_grid, solution)

    def animate_solution(self, original, solved, idx=0):
        if idx >= 81:
            return
        r, c = idx // 9, idx % 9
        if original[r][c] == 0:
            val = solved[r][c]
            self.grid_data[r][c] = val
            self.marks[r][c].clear()
            self.solved_cells.add((r, c))
            self._redraw_cell(r, c)
            self.root.update()
            time.sleep(0.02)
        self.root.after(1, lambda: self.animate_solution(original, solved, idx + 1))

    # ── rules / violation check ───────────────────────────────────────────────

    def _find_violations(self):
        violations = set()
        for r in range(9):
            seen = {}
            for c in range(9):
                val = self.grid_data[r][c]
                if val:
                    if val in seen:
                        violations.add((r, c))
                        violations.add((r, seen[val]))
                    else:
                        seen[val] = c
        for c in range(9):
            seen = {}
            for r in range(9):
                val = self.grid_data[r][c]
                if val:
                    if val in seen:
                        violations.add((r, c))
                        violations.add((seen[val], c))
                    else:
                        seen[val] = r
        for sx in range(3):
            for sy in range(3):
                seen = {}
                for r in range(3 * sx, 3 * sx + 3):
                    for c in range(3 * sy, 3 * sy + 3):
                        val = self.grid_data[r][c]
                        if val:
                            if val in seen:
                                violations.add((r, c))
                                violations.add(seen[val])
                            else:
                                seen[val] = (r, c)
        return violations

    def _update_rule_colors(self, violations=None):
        if violations is None:
            violations = self._find_violations()
        for r in range(9):
            for c in range(9):
                if self.grid_data[r][c] != 0:
                    self._redraw_cell(r, c, violations)

    def _on_check_rules_toggle(self):
        violations = self._find_violations() if self.check_rules_var.get() else None
        for r in range(9):
            for c in range(9):
                if self.grid_data[r][c] != 0:
                    self._redraw_cell(r, c, violations)

    # ── correctness check ────────────────────────────────────────────────────

    def check_action(self):
        puzzle_grid = [[0] * 9 for _ in range(9)]
        if self.preset_cells:
            for r, c in self.preset_cells:
                puzzle_grid[r][c] = self.grid_data[r][c]
        else:
            puzzle_grid = [row[:] for row in self.grid_data]

        solution, is_unique = solve_sudoku_logic(puzzle_grid)
        if solution is None:
            messagebox.showerror("Błąd", "Brak rozwiązania dla podanej łamigłówki!")
            return

        if not is_unique:
            messagebox.showinfo(
                "Wiele rozwiązań",
                "To Sudoku jest niedookreślone — istnieje wiele rozwiązań.\n"
                "Żadna wprowadzona cyfra nie może być uznana za błędną.",
            )
            return

        self.wrong_cells.clear()
        wrong_count = 0
        correct_count = 0
        for r in range(9):
            for c in range(9):
                if (r, c) not in self.preset_cells and self.grid_data[r][c] != 0:
                    if self.grid_data[r][c] != solution[r][c]:
                        self.wrong_cells.add((r, c))
                        wrong_count += 1
                    else:
                        correct_count += 1

        violations = self._find_violations() if self.check_rules_var.get() else None
        for r in range(9):
            for c in range(9):
                if self.grid_data[r][c] != 0:
                    self._redraw_cell(r, c, violations)

        if wrong_count == 0 and correct_count == 0:
            messagebox.showinfo("Sprawdź", "Nie wprowadzono żadnych cyfr do sprawdzenia.")
        elif wrong_count == 0:
            messagebox.showinfo("Sprawdź", f"Wszystkie {correct_count} wprowadzonych cyfr są poprawne!")
        else:
            messagebox.showwarning(
                "Sprawdź",
                f"Znaleziono {wrong_count} błędnych cyfr (zaznaczone na pomarańczowo).",
            )

    # ── file loading ─────────────────────────────────────────────────────────

    def load_puzzle_from_file(self, filename):
        try:
            with open(filename) as f:
                content = f.read()
        except OSError as e:
            messagebox.showerror("Błąd", f"Nie można otworzyć pliku: {e}")
            return

        digits = []
        for ch in content:
            if ch.isdigit():
                digits.append(int(ch))
            elif ch == ".":
                digits.append(0)

        if len(digits) != 81:
            messagebox.showerror(
                "Błąd",
                f"Plik musi zawierać dokładnie 81 cyfr/kropek (znaleziono {len(digits)}).",
            )
            return

        # Full reset before loading
        self.grid_data = [[0] * 9 for _ in range(9)]
        self.marks = [[{} for _ in range(9)] for _ in range(9)]
        self.preset_cells.clear()
        self.solved_cells.clear()
        self.wrong_cells.clear()
        self.selected_cell = None
        self.mark_mode = None
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].config(bg=self.COLORS["cell_bg"])
                self._redraw_cell(r, c)

        for i, digit in enumerate(digits):
            r, c = i // 9, i % 9
            self.grid_data[r][c] = digit
            if digit != 0:
                self.preset_cells.add((r, c))
                self._redraw_cell(r, c)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSudokuApp(root)
    root.mainloop()
