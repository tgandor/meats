#!/usr/bin/env python

# TODO: https://tkdocs.com/tutorial/grid.html#resize ? maybe
# https://stackoverflow.com/questions/53073534/tkinter-button-expand-using-grid

import argparse
import datetime
import json
import locale
import os
import re
import sqlite3
import sys
import tempfile
import time
from typing import Literal


def _install_and_die(package):
    ans = input(f"Missing {package}, install with pip (Y/n)? ")
    if ans.lower().startswith("n"):
        if os.path.isfile("/etc/apt/sources.list"):
            cmd = f"sudo apt install python3-{package}"
        elif os.path.isfile("/etc/pacman.conf"):
            cmd = f"sudo pacman -S python-{package}"
        else:
            print("No alternative installation methods found.")
            exit(1)
        ans = input(f"Run '{cmd}' (Y/n)? ")
        if ans.lower().startswith("n"):
            exit(1)
        ret = os.system(cmd)
    else:
        ret = os.system("pip install {}".format(package))
    if ret:
        print(f"Installation problems. Retry:\npip install {package}")
        exit(1)
    print("Installation successful. Please re-run.")
    exit()


try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont, TTFError
except ImportError:
    _install_and_die("reportlab")
    raise SystemExit("ReportLab not found, exiting.")

parser = argparse.ArgumentParser()
parser.add_argument("--font-size", type=int, default=32)
parser.add_argument(
    "--round",
    action="store_true",
    help="Set default shape to round (mostly for commandline)",
)
parser.add_argument(
    "--repeat",
    type=int,
    default=1,
    help="Times to repeat each label verbatim (without series)",
)
parser.add_argument(
    "--print",
    action="store_true",
    help="Try to print directly, instead of opening",
    dest="print_",
)
parser.add_argument(
    "--gui", action="store_true", help="Open a tkinter GUI to create labels"
)
parser.add_argument(
    "--db-shell",
    action="store_true",
    help="Open a connection do DB and query from console",
)
parser.add_argument(
    "--multiline",
    action="store_true",
    help="For DB shell: require semicolon (multiline queries)",
)
parser.add_argument(
    "--import", "-i", type=str, help="Import a labels.db file to default database"
)
parser.add_argument("args", type=str, nargs="*", help="Old arguments.")

settings: dict = dict(
    font_size=32,
    date_font=14,
    round_label=False,
    top_margin=0.0 * cm,
    bottom_margin=1.0 * cm,
    line_width=0.25,
)
default_text = "Example label"
default_width = 21 * cm
default_height = 28.5 * cm
default_length = None
default_output_file = os.path.join(tempfile.gettempdir(), "simple_label_output.pdf")

# region rendering
fonts_to_try = ["Ubuntu-L", "Verdana", "Arial", "DejaVuSans", "Vera", "Helvetica"]
last_font = []  # needs to be reloaded after new page


def _setup_canvas(outfile=default_output_file):
    font_to_use = None
    for font_name in fonts_to_try:
        try:
            font = TTFont(font_name, font_name + ".ttf")
            pdfmetrics.registerFont(font)
            font_to_use = font_name
            break
        except TTFError:
            continue

    c = canvas.Canvas(outfile)
    if font_to_use:
        c.setFont(font_to_use, settings["font_size"])
        last_font.append(font_to_use)
    else:
        sys.stderr.write(
            "No TTF font found from list: {}\n".format(", ".join(fonts_to_try))
        )
    c.setTitle(outfile)
    return c


def new_page(c):
    print("Starting new page")
    c.showPage()
    if last_font:
        c.setFont(last_font[0], settings["font_size"])


class LabelState:
    horizontal = False
    height_left = A4[1] - settings["top_margin"]


def label(c, text, width=default_width, height=default_height, state=LabelState()):
    print("Drawing label:", repr(text))

    # convenience hack
    width, height = [min(x, max(A4)) for x in (width, height)]

    # validate
    if min(width, height) > min(A4) or max(width, height) > max(A4):
        sys.stderr.write(
            "Error: label too big: {}x{} - not generating.\n".format(width, height)
        )
        return False

    # starting page width
    page_width, page_height = landscape(A4) if state.horizontal else A4

    # some extra margin for round label
    if settings["round_label"]:
        state.height_left -= 1 * cm

    # new page if can't fit
    if height > state.height_left:
        new_page(c)
        state.height_left = (
            page_height
            - settings["top_margin"]
            - (1 * cm if settings["round_label"] else 0.0)
        )

    # maybe switch to landscape
    if width > page_width:
        if state.height_left < page_height:
            new_page(c)
        c.setPageSize(landscape(A4))
        page_width, page_height = landscape(A4)
        state.horizontal = True
        state.height_left = page_height - settings["top_margin"]
        sys.stderr.write("Warning: switched to horizontal.\n")

    # maybe switch back to portrait
    if height > page_height:
        # page already shown
        c.setPageSize(A4)
        page_width, page_height = A4
        state.horizontal = False
        state.height_left = page_height - settings["top_margin"]
        sys.stderr.write("Warning: switched to vertical.\n")

    # coordinates inversion
    inv = lambda x: page_height - x

    c.saveState()
    c.setDash(4, 8)
    c.setLineWidth(settings["line_width"])

    # top line
    if (
        settings["line_width"] > 0
        and state.height_left < page_height
        and not settings["round_label"]
    ):
        # used to be until page width:
        c.line(0, state.height_left, width, state.height_left)

    h_offset = state.height_left - page_height
    # seems like transform IS part of state
    c.translate(1 * cm if settings["round_label"] else 0.0, h_offset)

    # borders - with margins to not 'fit to printing area' too much
    if settings["line_width"] > 0 and not settings["round_label"]:
        # horizontal line between labels
        c.line(0.2 * cm, inv(height), width - 0.2 * cm, inv(height))

        # vertical line right to label
        if width < page_width - 0.2 * cm:
            # print(f'width ({width}) < page_width ({page_width})')
            # width (595.275590551181) < page_width (595.2755905511812)
            # floats... can never be trusted.
            c.line(width, inv(0), width, inv(height))

    # text breaking...
    font_size = settings["font_size"]
    lines = text.split("\n")
    extra_h = len(lines) / 2 * font_size * (-1)
    for line, i in zip(lines, range(len(lines))):
        # serial label: last line should be with date font
        if i == len(lines) - 1 and re.match(r"\d+/\d+$", line):
            c.setFontSize(settings["date_font"])
        c.drawCentredString(width / 2, inv((height + font_size) / 2 + extra_h), line)
        extra_h += font_size

    # date subscript
    c.setFontSize(settings["date_font"])
    x = width / 2
    y = max(inv(height) + 0.5 * cm, settings["bottom_margin"])
    if settings["round_label"]:
        # hoping to fit the date
        y = inv(height * 0.75)
    date_text = datetime.datetime.now().strftime("%Y-%m-%d (%a) %H:%M")
    c.drawCentredString(x, y, date_text)

    # round border - not looking at line width...
    if settings["round_label"]:
        c.ellipse(0, inv(0), width, inv(height))

    # final cleanup
    c.restoreState()
    state.height_left -= height
    return True


def _finish_rendering(canvas):
    canvas.showPage()
    canvas.save()

    if sys.platform.startswith("linux"):
        if args.print_:
            os.system('lp "%s"' % default_output_file)
        else:
            os.system('xdg-open "%s"' % default_output_file)
    else:
        os.startfile(default_output_file, "print" if args.print_ else "open")


# endregion

# region label persistence


def open_database():
    labels_file = os.path.expanduser("~/labels.db")
    initialize = not os.path.exists(labels_file)
    conn = sqlite3.connect(labels_file)
    cursor = conn.cursor()
    # initialization
    if initialize:
        cursor.executescript(
            """
create table labels
(
    id integer not null primary key autoincrement,
    text text not null,
    width decimal not null,
    height decimal not null,
    length decimal null
);

create table outprints
(
    id integer not null primary key autoincrement,
    label_id integer not null references labels(id),
    outprint_date datetime not null,
    settings text null
);
"""
        )
    conn.text_factory = str  # which == unicode on Py3, and works!
    # migrations:
    run_migrations(cursor)
    return conn, cursor


def _fetch_one(cursor, query, params=()):
    """Helper for single result queries.
    Arguments:
        cursor: `sqlite3.Cursor`
        query: `str`
        params: `tuple`
    """
    cursor.execute(query, params)
    return cursor.fetchone()


def _fetch_all(cursor, query, params=()):
    """Helper for single result queries.
    Arguments:
        cursor: `sqlite3.Cursor`
        query: `str`
        params: `tuple`
    """
    cursor.execute(query, params)
    return cursor.fetchall()


def run_migrations(cursor):
    def log_migration(number):
        cursor.execute(
            "insert into schema_version values (?, ?);",
            (number, datetime.datetime.now()),
        )

    # 1. settings field for outprints
    if "settings" not in [
        r[1] for r in _fetch_all(cursor, "PRAGMA table_info(outprints)")
    ]:
        print("Migration 1: create settings column in outprint.")
        cursor.execute("alter table outprints add column settings text null;")
    # 2. initialize version table
    if _fetch_one(cursor, "PRAGMA table_info(schema_version)") is None:
        print("Migration 2: create schema_version.")
        cursor.execute(
            """
            create table schema_version (
                version integer not null primary key,
                updated datetime not null
            );
        """
        )
        cursor.execute(
            "insert into schema_version values (?, ?);", (2, datetime.datetime.now())
        )

    file_version = _fetch_one(cursor, "select max(version) from schema_version;")[0]

    # 3. prev / next after, with views
    if file_version < 3:
        print("Migration 3: create next_label / prev_label.")
        cursor.executescript(
            """
            create view last_outprint as
            select label_id, max(id) as max_id
            from outprints group by label_id;

            create view next_label as
            select
                label_id,
                (
                    select min(label_id) from last_outprint where max_id > lo.max_id
                ) as next_label_id
            from last_outprint lo;

            create view prev_label as
            select
                label_id,
                (
                    select max(label_id) from last_outprint where max_id < lo.max_id
                ) as prev_label_id
            from last_outprint lo;
        """
        )
        log_migration(3)
    # 4. time-based prev / next views
    if file_version < 4:
        print("Migration 4: create newer_label / older_label.")
        # note the hack with selecting id from outprints, without it
        # being grouped by it. It happens to be the id of the row
        # which has max(outprint_date)
        # SQL orthodoxes hate this (not really portable),
        # and offer even scarier things with "partition by" etc.
        # https://dba.stackexchange.com/questions/158602/get-id-of-row-in-aggregate/158603
        # https://stackoverflow.com/questions/7745609/sql-select-only-rows-with-max-value-on-a-column
        cursor.executescript(
            """
            create view newest_outprint as
            select label_id, max(outprint_date) as last_date, id
            from outprints group by label_id
            order by last_date;

            create view newer_label as
            select label_id,
                (
                    select label_id
                    from newest_outprint
                    where last_date > no.last_date
                    order by last_date
                    limit 1
                ) as next_label_id
            from newest_outprint no;

            create view older_label as
            select label_id,
                (
                    select label_id
                    from newest_outprint
                    where last_date < no.last_date
                    order by last_date desc
                    limit 1
                ) as prev_label_id
            from newest_outprint no;
        """
        )
        log_migration(4)


def close_database(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def save_label(text, width, height, length, label_settings={}):
    conn, cursor = open_database()
    cursor.execute("SELECT id FROM labels WHERE text = ?", (text,))
    # create or update label
    label_id = cursor.fetchone()
    if length is not None:
        length /= cm
    if label_id is None:
        cursor.execute(
            "INSERT INTO labels (text, width, height, length) VALUES (?,?,?,?)",
            (
                text,
                width / cm,
                height / cm,
                length,
            ),
        )
        label_id = cursor.lastrowid
        print("{} Created label {}".format(time.strftime("%H:%M"), label_id))
    else:
        label_id = label_id[0]
        cursor.execute(
            "UPDATE labels SET width=?, height=?, length=? WHERE id=?",
            (width / cm, height / cm, length, label_id),
        )
        print("{} Updated label {}".format(time.strftime("%H:%M"), label_id))
    # log the generation
    cursor.execute(
        "INSERT INTO outprints(label_id, outprint_date, settings) VALUES (?,?,?)",
        (label_id, datetime.datetime.now(), json.dumps(label_settings)),
    )
    close_database(conn, cursor)


def _load_label(cursor, label_id):
    """Helper for loading labels.
    Arguments:
        cursor: `sqlite3.Cursor`
        label_id: `tuple` 1-element tuple containing label_id
    """
    last_date = _fetch_one(
        cursor, "select last_date from newest_outprint where label_id=?", label_id
    )[0]
    print("Loading label: {} (last printed {})".format(label_id[0], last_date))
    return _fetch_one(
        cursor, "select id, text, width, height from labels WHERE id=?", label_id
    )


def get_previous_label(current):
    conn = cursor = None
    try:
        conn, cursor = open_database()
        if current == 0:
            prev_id = _fetch_one(
                cursor,
                "select label_id from newest_outprint order by last_date desc limit 1",
            )
        else:
            prev_id = _fetch_one(
                cursor,
                "select prev_label_id from older_label where label_id=?",
                (current,),
            )
        if not prev_id or not prev_id[0]:
            return None

        return _load_label(cursor, prev_id)
    finally:
        if conn and cursor:
            close_database(conn, cursor)


def get_next_label(current):
    conn = cursor = None
    try:
        conn, cursor = open_database()
        if current == 0:
            next_id = _fetch_one(
                cursor,
                "select label_id from newest_outprint order by last_date limit 1",
            )
        else:
            next_id = _fetch_one(
                cursor,
                "select next_label_id from newer_label where label_id=?",
                (current,),
            )
        if not next_id or not next_id[0]:
            return None

        return _load_label(cursor, next_id)
    finally:
        if conn and cursor:
            close_database(conn, cursor)


def get_previous_label_filtered(current, pattern, back=False):
    print("Searching for:", pattern, "(backwards)" if back else "")
    conn = cursor = None
    try:
        conn, cursor = open_database()
        if current == 0:
            prev_id = _fetch_one(
                cursor,
                """select o.label_id
                from outprints o
                join labels l on o.label_id = l.id
                where l.text like ?
                order by o.outprint_date {} limit 1""".format(
                    "" if back else "desc"
                ),
                ("%{}%".format(pattern),),
            )
        else:
            forward_values = ("<", "desc")
            backward_values = (">", "")
            # no hacks, 3 subqueries, 1 condtion between 2 subqueries, and order by subquery...
            # plain SQL algebra.
            prev_id = _fetch_one(
                cursor,
                """select lbl.id
                from labels lbl
                where lbl.id <> ?
                    and lbl.text like ?
                    and
                        (select max(outprint_date) from outprints where label_id=lbl.id)
                        {}
                        (select max(outprint_date) from outprints where label_id=?)
                order by (select max(outprint_date) from outprints where label_id=lbl.id) {}
                limit 1""".format(
                    *(backward_values if back else forward_values)
                ),
                (current, "%{}%".format(pattern), current),
            )

        if not prev_id or not prev_id[0]:
            return None

        return _load_label(cursor, prev_id)
    finally:
        if conn and cursor:
            close_database(conn, cursor)


# endregion


def multi_label(text, width, height, count, canvas=None, label_state=None):
    save_label(text, width, height, None, label_settings(count=count))
    c = canvas or _setup_canvas()
    state = label_state or LabelState()
    for i in range(count):
        label(c, "{}\n{}/{}".format(text, i + 1, count), width, height, state=state)
    if canvas is None:
        _finish_rendering(c)


def parse_s(s, full_s, max_s=A4[1]):
    if s.endswith("%"):
        return float(s[:-1]) / 100 * full_s
    val = float(s) * cm
    if val > max_s:
        print("Warning: value", val / cm, ">=", max_s / cm, "(clamped)")
        return max_s
    return val


def get_parameters():
    if len(argv) < 3:
        print("Not enough arguments. Usage: simple_label_pdf.py text W H [L]")
        exit()

    text = argv[0]
    in_width = argv[1]
    in_height = argv[2]
    width = parse_s(in_width, A4[0]) if in_width else default_width
    height = parse_s(in_height, A4[1]) if in_height else default_height

    if len(argv) >= 4:
        # A4[0], because length is like width
        length = parse_s(argv[3], A4[0])
    else:
        length = default_length

    return text, width, height, length


def label_settings(count=1, **kwargs):
    result = {
        "count": count,
    }
    result.update(settings)
    result.update(kwargs)
    return result


def main():
    text, width, height, length = get_parameters()
    save_label(text, width, height, length, label_settings())
    c = _setup_canvas()
    for _ in range(args.repeat):
        label(c, text, width, height)
        if length:
            label(c, text, length, height)
            label(c, text, width, length)
    _finish_rendering(c)


def win_main():
    import tkinter as tk
    from tkinter import ttk

    ui_font = ("TkDefaultFont", 12)

    class Spinbox(tk.Spinbox):
        def __init__(self, *args, **kwargs):
            kwargs["font"] = ui_font
            kwargs["justify"] = "right"
            tk.Spinbox.__init__(self, *args, **kwargs)
            self.bind("<MouseWheel>", self.mouse_wheel)
            self.bind("<Button-4>", self.mouse_wheel)
            self.bind("<Button-5>", self.mouse_wheel)

        def set(self, value):
            self.delete(0, tk.END)
            self.insert(0, value)
            return self

        def mouse_wheel(self, event):
            if event.num == 5 or event.delta < 0:
                self.invoke("buttondown")
            elif event.num == 4 or event.delta > 0:
                self.invoke("buttonup")

    class LabelFormModel:
        def __init__(self):
            self.is_serial = tk.IntVar()
            self.is_round = tk.IntVar()
            self.repeat = tk.IntVar()
            self.filter = tk.StringVar()
            self.print_mode = tk.StringVar(value="Print" if args.print_ else "Generate")
            self.width = tk.DoubleVar()
            self.height = tk.DoubleVar()
            self.text = tk.StringVar()
            self.font_size = tk.StringVar(
                value=str(args.font_size)
            )  # tk.IntVar(value=args.font_size)
            self.last_id = tk.IntVar()

    def ui_label(parent, text, side: Literal["top", "left"] = tk.TOP, **packkw):
        tk.Label(parent, text=text, font=ui_font).pack(side=side, **packkw)

    def set_text(widget, value):
        """Kludge, his should actually be handled by the model."""
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, value)

    def generate(text_widget, width_input, height_input, canvas_state):
        label_text = text_widget.get("1.0", "end").strip()
        w = float(width_input.get().replace(",", ".")) * cm
        h = float(height_input.get().replace(",", ".")) * cm
        settings["round_label"] = label_model.is_round.get() != 0

        c = canvas_state.get("canvas") or _setup_canvas()
        state = canvas_state.get("label_state") or LabelState()

        if label_model.is_serial.get():
            multi_label(
                label_text, w, h, label_model.repeat.get(), canvas=c, label_state=state
            )
        else:
            save_label(label_text, w, h, None, label_settings())
            for _ in range(label_model.repeat.get()):
                label(c, label_text, w, h, state)

        if label_model.print_mode.get() == "Enqueue":
            canvas_state["canvas"] = c
            canvas_state["label_state"] = state
        else:
            _finish_rendering(c)
            canvas_state["canvas"] = None
            canvas_state["label_state"] = None

    def set_current_label(
        height, height_input, previous_id, text, text_widget, width, width_input
    ):
        set_text(text_widget, text)
        width_input.set(width)
        height_input.set(height)
        modified(text_widget, None)
        label_model.last_id.set(previous_id)

    def load_previous(text_widget, width_input, height_input):
        if label_model.filter.get():
            row = get_previous_label_filtered(
                label_model.last_id.get(), label_model.filter.get()
            )
        else:
            row = get_previous_label(current=label_model.last_id.get())

        if row is None:
            print("No [more] previous records")
            return

        previous_id, text, width, height = row
        set_current_label(
            height, height_input, previous_id, text, text_widget, width, width_input
        )

    def load_next(text_widget, width_input, height_input):
        if label_model.filter.get():
            # next is just previous but backwards:
            row = get_previous_label_filtered(
                label_model.last_id.get(), label_model.filter.get(), back=True
            )
        else:
            row = get_next_label(current=label_model.last_id.get())

        if row is None:
            print("No [more] records")
            return

        next_id, text, width, height = row
        set_current_label(
            height, height_input, next_id, text, text_widget, width, width_input
        )

    def modified(text, event):
        text.tag_add("label", "1.0", tk.END)

    def setup_ui(root, label_model):
        root.title("Simple Label")
        dialog = tk.Frame(root)

        ui_label(dialog, "Label text:")
        text = tk.Text(dialog)
        text.focus_set()

        text.tag_config(
            "label", justify="center", font=(fonts_to_try[0], settings["font_size"])  # type: ignore[call-arg]
        )
        text.bind("<Key>", lambda e: modified(text, e))
        text.bind("<<Modified>>", lambda e: modified(text, e))
        text.pack(anchor=tk.N, expand=True, fill="both")

        # Label and font size panel

        size_panel = tk.Frame(dialog)

        ui_label(size_panel, "Width [cm]:", tk.LEFT)
        width = Spinbox(
            size_panel,
            width=8,
            from_=0,
            to=30,
            increment=0.1,
            format="%.1f",
            textvariable=label_model.width,
        )
        width.set("21.0").pack(side=tk.LEFT, padx=10)

        ui_label(size_panel, "Height [cm]:", tk.LEFT)
        height = Spinbox(
            size_panel,
            width=8,
            from_=0,
            to=30,
            increment=0.1,
            format="%.1f",
            textvariable=label_model.height,
        )
        height.set("5.9").pack(side=tk.LEFT, padx=10)

        def change_font(font_variable):
            # this won't work, happens inside tkinter:
            # if not font_variable.get():
            #    return
            try:
                # value = font_variable._tk.globalgetvar(font_variable._name)
                value = font_variable.get()
            except tk.TclError:
                return

            # TODO: fonts_to_try vs last_font?
            settings["font_size"] = int(value)  # int, Tkinter expects int.
            text.tag_config("label", font=(fonts_to_try[0], settings["font_size"]))

        ui_label(size_panel, "Font size [pt]:", tk.LEFT, padx=10)

        # somehow is textvariable not enough...
        font_size = Spinbox(
            size_panel,
            width=8,
            values=list(range(20, 74, 2)),
            textvariable=label_model.font_size,
        )
        font_size.set(settings["font_size"])
        font_size.pack(side=tk.LEFT)

        label_model.font_size.trace("w", lambda *_: change_font(label_model.font_size))

        size_panel.pack(anchor=tk.N, expand=1, fill="x")

        # Repetition settings

        rep_panel = tk.Frame(dialog)

        ui_label(rep_panel, "Repeat count:", tk.LEFT, padx=10)
        serial_count = Spinbox(
            rep_panel, width=8, from_=1, to=100, textvariable=label_model.repeat
        )
        serial_count.pack(side=tk.LEFT)

        tk.Checkbutton(
            rep_panel,
            variable=label_model.is_serial,
            font=ui_font,
            text="Generate serial labels",
        ).pack(anchor=tk.N)

        tk.Checkbutton(
            rep_panel,
            variable=label_model.is_round,
            font=ui_font,
            text="Generate round labels",
        ).pack(anchor=tk.N)

        rep_panel.pack(anchor=tk.N)

        # Print/generate/enqueue  mode

        mode_panel = tk.Frame(dialog)

        ui_label(mode_panel, "Print mode:", tk.LEFT, padx=10)
        PRINT_MODES = ("Generate", "Print", "Enqueue")
        cb_print_mode = ttk.Combobox(mode_panel, textvariable=label_model.print_mode)
        cb_print_mode["values"] = PRINT_MODES
        cb_print_mode.current(PRINT_MODES.index(label_model.print_mode.get()))
        cb_print_mode.pack(side=tk.LEFT)

        mode_panel.pack(anchor=tk.N)

        canvas_state = {
            "canvas": None,
            "label_state": None,
        }

        panel = tk.Frame(dialog)

        tk.Button(
            panel,
            text="<",
            width="3",
            height="3",
            command=lambda: load_previous(text, width, height),
        ).grid(row=0, column=0)
        tk.Button(
            panel,
            textvariable=label_model.print_mode,
            font=ui_font,
            width=47,
            height=3,
            command=lambda: generate(text, width, height, canvas_state),
        ).grid(row=0, column=1)
        tk.Button(
            panel,
            text=">",
            width="3",
            height="3",
            command=lambda: load_next(text, width, height),
        ).grid(row=0, column=2)

        # TODO: filter
        # simple (in a good way) tk docs:
        # https://www.tutorialspoint.com/python/python_gui_programming
        tk.Label(panel, text="Filter:", font=ui_font).grid(row=1, column=0)
        filter_text = tk.Entry(
            panel, width=47, font=ui_font, textvariable=label_model.filter
        )
        filter_text.grid(row=1, column=1, columnspan=1)

        panel.pack(anchor=tk.N)

        dialog.pack(fill=tk.BOTH, expand=1)

        # region: event handlers
        cb_print_mode.bind(
            "<<ComboboxSelected>>",
            lambda e:
            # why no args.print_ = ...? SyntaxError: lambda cannot contain assignment
            setattr(args, "print_", label_model.print_mode.get() == "Print"),
        )
        # endregion

    root = tk.Tk()
    # root needs to be created before IntVars and the like ("default root")
    label_model = LabelFormModel()
    setup_ui(root, label_model)
    root.mainloop()


def db_shell_main(multiline=False):
    try:
        import readline  # pylint disable=unused-import
    except ImportError:
        print("Sorry, no readline")

    try:
        import six
    except ImportError:
        _install_and_die("six")
        raise SystemExit("Six not found, exiting.")

    conn = cursor = None

    def get_query():
        if not multiline:
            return six.moves.input("sqlite> ")

        query = six.moves.input("sqlite> ")

        if query.strip() in ("exit", "quit", ""):
            return query.strip()

        lines = [query.strip()]

        while not lines[-1].endswith(";"):

            lines.append(six.moves.input("... ").strip())

        return "\n".join(lines)

    try:
        conn, cursor = open_database()
        while True:
            query = get_query()

            if query in ("exit", "quit", ""):
                break

            for row in _fetch_all(cursor, query):
                print(row)
            print("-" * 50)
    except EOFError:
        print("EOF exit.")
    finally:
        if conn and cursor:
            print("Closing database.")
            close_database(conn, cursor)


def import_database():
    to_import = getattr(args, "import")
    in_connection = sqlite3.connect(to_import)
    in_cursor = in_connection.cursor()
    run_migrations(in_cursor)
    out_connection = out_cursor = None
    try:
        out_connection, out_cursor = open_database()
        for id_, text, width_cm, height_cm, length_cm in _fetch_all(
            in_cursor, "select id, text, width, height, length from labels"
        ):
            local_id = _fetch_one(
                out_cursor, "select id from labels WHERE text=?", (text,)
            )
            if local_id is None:
                print("Importing label:", text)
                out_cursor.execute(
                    "INSERT INTO labels (text, width, height, length) VALUES (?, ?, ?, ?)",
                    (
                        text,
                        width_cm,
                        height_cm,
                        length_cm,
                    ),
                )
                out_label_id = out_cursor.lastrowid
                my_outprints = set()
            else:
                print("Label {} found.".format(local_id[0]))
                out_label_id = local_id[0]
                my_outprints = set(
                    date
                    for (date,) in _fetch_all(
                        out_cursor,
                        "select outprint_date from outprints where label_id=?",
                        local_id,
                    )
                )

            for outprint_date, settings in _fetch_all(
                in_cursor,
                "select outprint_date, settings from outprints where label_id=?",
                (id_,),
            ):
                if outprint_date in my_outprints:
                    print(
                        "Outprint at {} with settings {} exists.".format(
                            outprint_date, settings
                        )
                    )
                else:
                    print(
                        "Outprint at {} with settings {} migrated.".format(
                            outprint_date, settings
                        )
                    )
                    out_cursor.execute(
                        "insert into outprints (label_id, outprint_date, settings) values (?, ?, ?)",
                        (out_label_id, outprint_date, settings),
                    )
    finally:
        if out_connection and out_cursor:
            close_database(out_connection, out_cursor)
    in_cursor.close()
    in_connection.close()


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")
    args = parser.parse_args()
    # print(args)

    argv = args.args
    settings["font_size"] = args.font_size
    settings["round_label"] = args.round
    # print(settings)

    if args.db_shell:
        db_shell_main(args.multiline)
    elif getattr(args, "import"):
        import_database()
    elif args.gui or len(argv) == 0:
        win_main()
    elif len(argv) == 4 and argv[3].startswith("x"):
        multi_label(
            argv[0], parse_s(argv[1], A4[0]), parse_s(argv[2], A4[1]), int(argv[3][1:])
        )
    else:
        main()
