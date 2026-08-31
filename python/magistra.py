import os
import json
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox, simpledialog

from practice import PracticeDialog
from editor import EditorWindow, WordList


DATA_DIR = "pair_lists"
CONFIG_PATH = "magistra_config.json"

class MagistraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Magistra")
        # font size from config (applied in _build)
        self.config = self._load_config()
        self.font_size = int(self.config.get('font_size', 12))
        # set initial geometry scaled by font size
        width = 480 + max(0, (self.font_size - 12) * 30)
        height = 260 + max(0, (self.font_size - 12) * 20)
        self.geometry(f"{width}x{height}")
        # if user previously saved welcome window geometry, restore it
        try:
            wg = self.config.get('welcome_geometry') if self.config else None
            if wg:
                self.geometry(wg)
        except Exception:
            pass

        self.user_var = tk.StringVar()
        self.lang_var = tk.StringVar()
        self.mode_var = tk.StringVar(value=self.config.get('mode', 'Basic'))
        self.group_var = tk.IntVar(value=1)
        self.percent_var = tk.IntVar(value=25)

        self._build()
        self._apply_config()
        # No per-user mode lookup; mode is taken from the welcome UI and persisted in the global config

    def _load_config(self):
        if not os.path.exists(CONFIG_PATH):
            return {}
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_config(self):
        # start with existing config so we preserve other keys (e.g., practice_geometry)
        cfg = dict(self.config or {})
        cfg.update({
            'user': self.user_var.get(),
            'language': self.lang_var.get(),
            'group': int(self.group_var.get()),
            'percent': int(self.percent_var.get()),
            'mode': self.mode_var.get(),
            'font_size': int(self.font_size)
        })
        # per-user mode is stored in the user's userdata file (MAGISTRA_META), not in this config
        # always store current main window geometry as welcome_geometry
        try:
            cfg['welcome_geometry'] = self.geometry()
        except Exception:
            pass
        # keep the runtime copy in sync
        self.config = cfg
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(cfg, f)
        except Exception:
            pass

    def _apply_config(self):
        if not self.config:
            return
        if 'user' in self.config:
            self.user_var.set(self.config.get('user', ''))
        if 'group' in self.config:
            try:
                self.group_var.set(int(self.config.get('group', 1)))
            except Exception:
                pass
        if 'percent' in self.config:
            try:
                self.percent_var.set(int(self.config.get('percent', 25)))
            except Exception:
                pass
        if 'mode' in self.config:
            try:
                self.mode_var.set(self.config.get('mode', 'Basic'))
            except Exception:
                pass
        if 'font_size' in self.config:
            try:
                self.font_size = int(self.config.get('font_size', self.font_size))
            except Exception:
                pass
        # base language is not shown on the welcome screen

    def _build(self):
        # slightly smaller outer padding so form fits better
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)

        # create app font and apply to button style
        self.app_font = tkfont.Font(size=self.font_size)
        style = ttk.Style()
        style.configure('TButton', font=self.app_font)
        style.configure('TMenubutton', font=self.app_font)

        # left column label and input; add extra horizontal gap and modest vertical spacing
        ttk.Label(frm, text="Name", font=self.app_font).grid(row=0, column=0, sticky=tk.W, pady=(6,6))
        ttk.Entry(frm, textvariable=self.user_var, font=self.app_font, width=45).grid(row=0, column=1, sticky=tk.W, padx=(12,0), pady=(6,6))

        ttk.Label(frm, text="Language", font=self.app_font).grid(row=1, column=0, sticky=tk.W)
        langs = self._discover_languages()
        default_lang = self.config.get('language') if self.config.get('language') in langs else (langs[0] if langs else 'German')
        self.lang_var.set(default_lang)
        self.lang_opt = ttk.OptionMenu(frm, self.lang_var, self.lang_var.get(), *langs)
        try:
            self.lang_opt.configure(font=self.app_font, width=45)
        except Exception:
            try:
                self.lang_opt.configure(width=45)
            except Exception:
                pass
        self.lang_opt.grid(row=1, column=1, sticky=tk.W, padx=(12,0), pady=(6,6))
        # add 'New language' as last menu item
        try:
            menu = self.lang_opt['menu']
            menu.add_separator()
            menu.add_command(label='New language...', command=self._on_new_language)
        except Exception:
            pass
        ttk.Label(frm, text="Starting group", font=self.app_font).grid(row=2, column=0, sticky=tk.W, pady=(6,6))
        ttk.Entry(frm, textvariable=self.group_var, font=self.app_font, width=10).grid(row=2, column=1, sticky=tk.W, padx=(12,0), pady=(6,6))

        ttk.Label(frm, text="Practice %", font=self.app_font).grid(row=3, column=0, sticky=tk.W, pady=(6,6))
        ttk.Entry(frm, textvariable=self.percent_var, font=self.app_font, width=10).grid(row=3, column=1, sticky=tk.W, padx=(12,0), pady=(6,6))

        # Mode radio buttons
        ttk.Label(frm, text="Mode", font=self.app_font).grid(row=4, column=0, sticky=tk.W, pady=(6,6))
        rfrm = ttk.Frame(frm)
        rfrm.grid(row=4, column=1, sticky=tk.W, padx=(12,0), pady=(6,6))
        rb1 = ttk.Radiobutton(rfrm, text='Basic', variable=self.mode_var, value='Basic', style='TRadiobutton', takefocus=0)
        rb2 = ttk.Radiobutton(rfrm, text='Exact', variable=self.mode_var, value='Exact', style='TRadiobutton', takefocus=0)
        try:
            style.configure('TRadiobutton', font=self.app_font)
        except Exception:
            pass
        rb1.pack(side=tk.LEFT, padx=(0,8))
        rb2.pack(side=tk.LEFT)

        btnfrm = ttk.Frame(frm)
        # reduce extra vertical space around the buttons
        btnfrm.grid(row=5, column=0, columnspan=3, pady=(6, 0))
        ttk.Button(btnfrm, text="Practice", command=self._on_practice).pack(side=tk.LEFT, padx=6)
        ttk.Button(btnfrm, text="Edit word list", command=self._on_edit).pack(side=tk.LEFT, padx=6)
        ttk.Button(btnfrm, text="Quit", command=self._on_quit).pack(side=tk.LEFT, padx=6)

        # leave column 0 narrow for labels and column 1 for inputs; column 1 can expand
        frm.columnconfigure(0, minsize=120)
        frm.columnconfigure(1, weight=1)

    def _discover_languages(self):
        langs = []
        if not os.path.isdir(DATA_DIR):
            return ["German"]
        for fn in os.listdir(DATA_DIR):
            if fn.lower().endswith('.txt'):
                langs.append(os.path.splitext(fn)[0])
        langs.sort()
        return langs

    def _on_practice(self):
        name = self.user_var.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name.")
            return
        language = self.lang_var.get()
        start_group = int(self.group_var.get())
        percent = int(self.percent_var.get())
        # save config before launching
        self._save_config()

        # hide the welcome window while practicing
        self.withdraw()

        # load word list
        path = os.path.join(DATA_DIR, f"{language}.txt")
        if not os.path.exists(path):
            messagebox.showerror("Missing", f"Word list not found: {path}")
            return

        try:
            print("[magistra] loading WordList", path, flush=True)
            wl = WordList(path)
            # load user data (and per-user settings) if present
            userdata_path = f"{name}-{language}.txt"
            try:
                wl.incorporate_user_data_from_file(userdata_path)
            except Exception:
                pass
            print("[magistra] incorporating user data from %s" % userdata_path, flush=True)
            # print("[magistra] selecting all pairs", flush=True)
            wl.set_selected_all()
            print("[magistra] ordering pairs", flush=True)
            wl.set_order(start_group,percent)
            print("[magistra] creating PracticeDialog", flush=True)
            # pass saved practice window geometry if present
            pg = self.config.get('practice_geometry') if self.config else None
            # mode is taken from the welcome UI (most-recent selection)
            final_mode = self.mode_var.get()
            PracticeDialog(self, wl, font_size=self.font_size, initial_geometry=pg, mode=final_mode)
            print("[magistra] PracticeDialog created", flush=True)
        except Exception as e:
            print("[magistra] error launching practice:", e, flush=True)
            messagebox.showerror("Error", f"Failed to start practice: {e}")

    def _on_edit(self):
        # save config before editing
        self._save_config()
        # hide the welcome window while editing
        self.withdraw()
        language = self.lang_var.get()
        path = os.path.join(DATA_DIR, f"{language}.txt")
        if not os.path.exists(path):
            messagebox.showerror("Missing", f"Word list not found: {path}")
            return
        wl = WordList(path)
        # pass saved editor geometry if present
        eg = self.config.get('editor_geometry') if self.config else None
        EditorWindow(self, wl, font_size=self.font_size, initial_geometry=eg)

    def _on_quit(self):
        self._save_config()
        self.quit()

    def _on_new_language(self):
        # Ask for a new language name, create a file, and open the editor for it
        name = simpledialog.askstring("New language", "Enter new language name:", parent=self)
        if not name:
            return
        lang = name.strip()
        if not lang:
            return
        # ensure data directory exists
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
        except Exception:
            pass
        path = os.path.join(DATA_DIR, f"{lang}.txt")
        if not os.path.exists(path):
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    # header: base language name and generic foreign column
                    f.write(f"{lang}\tforeign\n")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create language file: {e}")
                return
        # refresh languages list in the OptionMenu
        try:
            menu = self.lang_opt['menu']
            # avoid duplicates
            existing = [self.lang_opt['menu'].entrycget(i, 'label') for i in range(menu.index('end')+1)] if menu.index('end') is not None else []
        except Exception:
            existing = []
        try:
            if lang not in existing:
                self.lang_opt['menu'].add_command(label=lang, command=lambda v=lang: self.lang_var.set(v))
        except Exception:
            pass
        # select it and open the editor
        try:
            self.lang_var.set(lang)
            wl = WordList(path)
            eg = self.config.get('editor_geometry') if self.config else None
            EditorWindow(self, wl, font_size=self.font_size, initial_geometry=eg)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open editor for {lang}: {e}")


if __name__ == '__main__':
    app = MagistraApp()
    app.mainloop()
"""
Magistra helps you practice foreign language vocabulary or any other word pairs
"""

