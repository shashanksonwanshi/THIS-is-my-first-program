# This  

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import os

# ── colour tokens ─────────────────────────────────────────────────────────────
BG       = "#0f1117"
PANEL    = "#1e2130"
ACCENT   = "#4f8ef7"
SUCCESS  = "#2ecc71"
DANGER   = "#e74c3c"
FG       = "#e8eaf6"
FG2      = "#8892b0"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
MONO     = ("Consolas", 9)

# ── helper ────────────────────────────────────────────────────────────────────

def get_items():
    return sorted(Path('').rglob('*'))

# ── main app ──────────────────────────────────────────────────────────────────

class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🗂  File Manager  —  CRUD")
        self.geometry("920x640")
        self.minsize(760, 520)
        self.configure(bg=BG)

        self._build_ui()
        self.refresh_tree()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── left sidebar: file tree ──────────────────────────────────────────
        sidebar = tk.Frame(self, bg=PANEL, width=260)
        sidebar.pack(side="left", fill="y", padx=(12, 0), pady=12)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Directory", bg=PANEL, fg=FG2,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(12, 4))

        tree_frame = tk.Frame(sidebar, bg=PANEL)
        tree_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Tree.Treeview",
                         background=PANEL, fieldbackground=PANEL,
                         foreground=FG, font=MONO, rowheight=22,
                         borderwidth=0)
        style.configure("Tree.Treeview.Heading", background=PANEL,
                         foreground=FG2, font=("Segoe UI", 9, "bold"))
        style.map("Tree.Treeview", background=[("selected", ACCENT)])

        self.tree = ttk.Treeview(tree_frame, style="Tree.Treeview",
                                  show="tree", selectmode="browse")
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        tk.Button(sidebar, text="⟳  Refresh", bg=ACCENT, fg="white",
                  font=FONT_B, bd=0, padx=8, pady=6, cursor="hand2",
                  command=self.refresh_tree).pack(fill="x", padx=8, pady=(0, 12))

        # ── right panel: notebook tabs ───────────────────────────────────────
        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=12, pady=12)

        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL, foreground=FG2,
                         font=FONT_B, padding=[14, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", BG)],
                  foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(right)
        nb.pack(fill="both", expand=True)

        # status bar
        self.status_var = tk.StringVar(value="Ready.")
        self.status_color = tk.StringVar(value=FG2)
        status_bar = tk.Label(right, textvariable=self.status_var,
                               bg=BG, fg=FG2, font=("Segoe UI", 9),
                               anchor="w")
        status_bar.pack(fill="x", pady=(6, 0))
        self._status_label = status_bar

        # tabs
        self._tab_create_file(nb)
        self._tab_read_file(nb)
        self._tab_update_file(nb)
        self._tab_delete_file(nb)
        self._tab_rename_file(nb)
        self._tab_create_folder(nb)
        self._tab_delete_folder(nb)

    # ── status ────────────────────────────────────────────────────────────────

    def set_status(self, msg, ok=True):
        self._status_label.config(fg=SUCCESS if ok else DANGER)
        self.status_var.set(("✅  " if ok else "❌  ") + msg)

    # ── tree refresh ──────────────────────────────────────────────────────────

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for item in get_items():
            icon = "📁" if item.is_dir() else "📄"
            self.tree.insert("", "end", text=f"  {icon}  {item}")

    # ── reusable widget helpers ───────────────────────────────────────────────

    def _make_tab(self, nb, label):
        frame = tk.Frame(nb, bg=BG, padx=24, pady=20)
        nb.add(frame, text=label)
        return frame

    def _label(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=FG2, font=FONT).pack(anchor="w")

    def _entry(self, parent):
        e = tk.Entry(parent, bg=PANEL, fg=FG, insertbackground=FG,
                     font=FONT, bd=0, relief="flat", highlightthickness=1,
                     highlightbackground="#2e3250", highlightcolor=ACCENT)
        e.pack(fill="x", ipady=6, pady=(2, 12))
        return e

    def _text_area(self, parent, height=6):
        t = tk.Text(parent, bg=PANEL, fg=FG, insertbackground=FG,
                    font=MONO, bd=0, relief="flat", highlightthickness=1,
                    highlightbackground="#2e3250", highlightcolor=ACCENT,
                    height=height, wrap="word")
        t.pack(fill="both", expand=True, pady=(2, 12))
        return t

    def _button(self, parent, text, cmd, color=ACCENT):
        tk.Button(parent, text=text, command=cmd,
                  bg=color, fg="white", font=FONT_B,
                  bd=0, padx=16, pady=8, cursor="hand2",
                  activebackground=color, activeforeground="white").pack(anchor="w")

    # ── Tab 1: Create File ────────────────────────────────────────────────────

    def _tab_create_file(self, nb):
        f = self._make_tab(nb, "📄 Create File")
        self._label(f, "File name")
        self.cf_name = self._entry(f)
        self._label(f, "Content")
        self.cf_content = self._text_area(f)
        self._button(f, "Create File", self._do_create_file)

    def _do_create_file(self):
        name = self.cf_name.get().strip()
        if not name:
            self.set_status("Enter a file name.", ok=False); return
        p = Path(name)
        if p.exists():
            self.set_status(f"'{name}' already exists!", ok=False); return
        try:
            p.write_text(self.cf_content.get("1.0", "end-1c"))
            self.set_status(f"File '{name}' created!")
            self.cf_name.delete(0, "end")
            self.cf_content.delete("1.0", "end")
            self.refresh_tree()
        except Exception as e:
            self.set_status(str(e), ok=False)

    # ── Tab 2: Read File ──────────────────────────────────────────────────────

    def _tab_read_file(self, nb):
        f = self._make_tab(nb, "📖 Read File")
        self._label(f, "File name")
        self.rf_name = self._entry(f)
        self._button(f, "Read File", self._do_read_file)
        self._label(f, "Contents")
        self.rf_output = scrolledtext.ScrolledText(
            f, bg=PANEL, fg=SUCCESS, font=MONO, bd=0, relief="flat",
            height=8, state="disabled", wrap="word",
            highlightthickness=1, highlightbackground="#2e3250")
        self.rf_output.pack(fill="both", expand=True, pady=(4, 0))

    def _do_read_file(self):
        name = self.rf_name.get().strip()
        p = Path(name)
        if not p.exists():
            self.set_status(f"'{name}' not found!", ok=False); return
        try:
            text = p.read_text()
            self.rf_output.config(state="normal")
            self.rf_output.delete("1.0", "end")
            self.rf_output.insert("end", text)
            self.rf_output.config(state="disabled")
            self.set_status(f"'{name}' loaded.")
        except Exception as e:
            self.set_status(str(e), ok=False)

    # ── Tab 3: Update File ────────────────────────────────────────────────────

    def _tab_update_file(self, nb):
        f = self._make_tab(nb, "✏️ Update File")
        self._label(f, "File name")
        self.uf_name = self._entry(f)
        self._label(f, "Mode")
        self.uf_mode = tk.StringVar(value="Overwrite")
        row = tk.Frame(f, bg=BG); row.pack(anchor="w", pady=(0, 12))
        for m in ("Overwrite", "Append"):
            tk.Radiobutton(row, text=m, variable=self.uf_mode, value=m,
                           bg=BG, fg=FG, selectcolor=PANEL,
                           activebackground=BG, font=FONT).pack(side="left", padx=(0, 16))
        self._label(f, "Content")
        self.uf_content = self._text_area(f)
        self._button(f, "Update File", self._do_update_file)

    def _do_update_file(self):
        name = self.uf_name.get().strip()
        p = Path(name)
        if not p.exists():
            self.set_status(f"'{name}' does not exist!", ok=False); return
        try:
            flag = "w" if self.uf_mode.get() == "Overwrite" else "a"
            with open(name, flag) as fh:
                fh.write(self.uf_content.get("1.0", "end-1c"))
            self.set_status(f"'{name}' updated ({self.uf_mode.get().lower()}).")
            self.uf_content.delete("1.0", "end")
        except Exception as e:
            self.set_status(str(e), ok=False)

    # ── Tab 4: Delete File ────────────────────────────────────────────────────

    def _tab_delete_file(self, nb):
        f = self._make_tab(nb, "🗑️ Delete File")
        self._label(f, "File name")
        self.df_name = self._entry(f)
        self._button(f, "Delete File", self._do_delete_file, color=DANGER)

    def _do_delete_file(self):
        name = self.df_name.get().strip()
        p = Path(name)
        if not p.exists() or not p.is_file():
            self.set_status(f"'{name}' not found!", ok=False); return
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            try:
                os.remove(p)
                self.set_status(f"'{name}' deleted.")
                self.df_name.delete(0, "end")
                self.refresh_tree()
            except Exception as e:
                self.set_status(str(e), ok=False)

    # ── Tab 5: Rename File ────────────────────────────────────────────────────

    def _tab_rename_file(self, nb):
        f = self._make_tab(nb, "🔤 Rename File")
        self._label(f, "Current name")
        self.ren_old = self._entry(f)
        self._label(f, "New name")
        self.ren_new = self._entry(f)
        self._button(f, "Rename File", self._do_rename_file)

    def _do_rename_file(self):
        old = self.ren_old.get().strip()
        new = self.ren_new.get().strip()
        if not old or not new:
            self.set_status("Fill in both fields.", ok=False); return
        p = Path(old)
        if not p.exists():
            self.set_status(f"'{old}' not found!", ok=False); return
        try:
            p.rename(new)
            self.set_status(f"'{old}' renamed to '{new}'.")
            self.ren_old.delete(0, "end"); self.ren_new.delete(0, "end")
            self.refresh_tree()
        except Exception as e:
            self.set_status(str(e), ok=False)

    # ── Tab 6: Create Folder ──────────────────────────────────────────────────

    def _tab_create_folder(self, nb):
        f = self._make_tab(nb, "📁 Create Folder")
        self._label(f, "Folder name")
        self.mkd_name = self._entry(f)
        self._button(f, "Create Folder", self._do_create_folder)

    def _do_create_folder(self):
        name = self.mkd_name.get().strip()
        p = Path(name)
        if p.exists():
            self.set_status(f"'{name}' already exists!", ok=False); return
        try:
            p.mkdir(parents=True)
            self.set_status(f"Folder '{name}' created.")
            self.mkd_name.delete(0, "end")
            self.refresh_tree()
        except Exception as e:
            self.set_status(str(e), ok=False)

    # ── Tab 7: Delete Folder ──────────────────────────────────────────────────

    def _tab_delete_folder(self, nb):
        f = self._make_tab(nb, "🗑️ Delete Folder")
        self._label(f, "Folder name")
        self.rmd_name = self._entry(f)
        self._button(f, "Delete Folder", self._do_delete_folder, color=DANGER)

    def _do_delete_folder(self):
        name = self.rmd_name.get().strip()
        p = Path(name)
        if not p.exists() or not p.is_dir():
            self.set_status(f"Folder '{name}' not found!", ok=False); return
        if messagebox.askyesno("Confirm", f"Delete folder '{name}'?"):
            try:
                p.rmdir()
                self.set_status(f"Folder '{name}' deleted.")
                self.rmd_name.delete(0, "end")
                self.refresh_tree()
            except Exception as e:
                self.set_status(str(e), ok=False)


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()