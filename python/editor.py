import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox


class WordPair:
    def __init__(self, idx, base, foreign, groups):
        self.idx = str(idx)
        self.base = base
        self.foreign = foreign
        self.groups = list(groups)
        self.user_data = ""
        self.first_result = '?'
        self.removed = False

    def compare_strings(self, L, text):
        # L not used here because the object holds both words; keep API simple
        raw = (self.foreign if L == 1 else self.base)
        # split on semicolon alternatives
        candidates = [s.strip() for s in raw.split(';')]
        a = text.strip()
        # try exact match first (case-sensitive), then case-insensitive
        if a in candidates:
            return True
        al = a.lower()
        for c in candidates:
            if c.lower() == al:
                return True
        return False

    def modify_pair_data(self, s):
        self.user_data += s

    def set_first_result(self, ch):
        self.first_result = ch


class WordList:
    def __init__(self, filename):
        self.filename = filename
        self.languages = ["base", "foreign"]
        self.pair_table = {}
        self.indices = []
        self.selected = []
        self.order = []
        self.num_known = 0
        self.userdata_filename = None
        self.user_settings = {}
        self._read()

    def _read(self):
        with open(self.filename, encoding='utf-8') as f:
            first = f.readline().strip().split('\t')
            if len(first) >= 2:
                self.languages[0] = first[0]
                self.languages[1] = first[1]
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                idx = parts[0]
                base = parts[1] if len(parts) > 1 else ''
                foreign = parts[2] if len(parts) > 2 else ''
                # strip surrounding double quotes if present (some files wrap words in quotes)
                if len(base) >= 2 and base[0] == '"' and base[-1] == '"':
                    base = base.replace('"', '')
                if len(foreign) >= 2 and foreign[0] == '"' and foreign[-1] == '"':
                    foreign = foreign.replace('"', '')
                groups = []
                if len(parts) > 3:
                    # support comma or space separated groups
                    groups = [int(g) for g in parts[3].replace(',', ' ').split() if g.strip().isdigit()]
                else:
                    groups = [1]
                wp = WordPair(idx, base, foreign, groups)
                self.pair_table[idx] = wp
                self.indices.append(idx)

    def incorporate_user_data_from_file(self, userdata_path):
        self.userdata_filename = userdata_path
        if not os.path.exists(userdata_path):
            return
        with open(userdata_path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    idx = parts[0]
                    pdata = parts[1]
                    # legacy meta lines ignored
                    if idx == 'MAGISTRA_META':
                        continue
                    if idx in self.pair_table:
                        self.pair_table[idx].user_data = pdata
        # count known pairs using same rules as the Java version
        self.num_known = sum(self.evaluate_pair_data(wp.user_data) for wp in self.pair_table.values())

    def set_selected_all(self):
        self.selected = list(self.indices)

    def get_practice_probability(self,ud,repeat_percentage):
        """
        Compute a practice probability from user history ud
        """

        practiceProbability = repeat_percentage / 100.0

        # Empty history or most-recent wrong-like char => always practice (pp=1)
        if not ud:
            # no history, not yet practiced, probability 1
            pp = 1.0
        elif ud.endswith('f'):
            # skipped forever, do not practice
            pp = 0.0
        else:
            last = ud[-1]
            # wrong-like or preview/new => always practice
            if last in ('-', '_', '=', 'P'):
                pp = 1.0
            else:
                # trailing right-like block consists of +, &, # characters
                # find the contiguous trailing run of these chars
                run_chars = ''
                for ch in reversed(ud):
                    if ch in ('+', '&', '#'):
                        run_chars = ch + run_chars
                    else:
                        break
                if run_chars == '':
                    # no trailing right-run; use base practiceProbability
                    pp = practiceProbability
                else:
                    # ignore the very last correct character in the run for reduction
                    reducible = run_chars[:-1]
                    count_plus = reducible.count('+')
                    count_amp = reducible.count('&')
                    count_hash = reducible.count('#')
                    denom = (2 ** count_plus) * (1.5 ** count_amp) * (1.25 ** count_hash)
                    pp = practiceProbability / denom

        return pp

    def set_priorities2025(self, starting_group, repeat_percentage):
        # simplified: attach a numeric priority on each pair object (higher means practice)
        import random

        practiceProbability = repeat_percentage / 100.0

        for idx in self.indices:
            wp = self.pair_table[idx]
            ud = wp.user_data
            g = wp.groups[0] if (wp.groups and len(wp.groups) > 0) else 0

            # New logic: compute per-pair practice probability `pp` from trailing history.
            # Empty history or most-recent wrong-like char => always practice (pp=1)
            if not ud or ud.endswith('f'):
                # treat unseen as high priority; 'f' is handled separately below
                if not ud:
                    pp = 1.0
                else:
                    pp = 0.0
            else:
                last = ud[-1]
                # wrong-like or preview/new => always practice
                if last in ('-', '_', '=', 'P'):
                    pp = 1.0
                else:
                    # trailing right-like block consists of +, &, # characters
                    # find the contiguous trailing run of these chars
                    run_chars = ''
                    for ch in reversed(ud):
                        if ch in ('+', '&', '#'):
                            run_chars = ch + run_chars
                        else:
                            break
                    if run_chars == '':
                        # no trailing right-run; use base practiceProbability
                        pp = practiceProbability
                    else:
                        # ignore the very last correct character in the run for reduction
                        reducible = run_chars[:-1]
                        count_plus = reducible.count('+')
                        count_amp = reducible.count('&')
                        count_hash = reducible.count('#')
                        denom = (2 ** count_plus) * (1.5 ** count_amp) * (1.25 ** count_hash)
                        # avoid division by zero
                        if denom <= 0:
                            denom = 1.0
                        pp = practiceProbability / denom
            # if explicit skip-forever marker, make pp effectively zero by assigning large negative priority later
            if ud.endswith('f'):
                pp = 0.0
            # remember starting group for ordering behavior
            try:
                self._starting_group = int(starting_group)
            except Exception:
                self._starting_group = starting_group

            # groupScore: highest when g == starting_group
            if g >= starting_group:
                groupScore = 1000 - (g - starting_group)
            else:
                groupScore = 20

            if pp > 0 and random.random() < pp:
                score = groupScore + random.random()
            else:
                score = random.random()

            wp._priority = score
            # tiny jitter to break ties deterministically caused by similar random seeds
            score += random.random() * 1e-6

            wp._priority = score

    def set_order(self,sg,practice_percentage):

        import random

        print('starting group ', sg)

        # Group pairs by their first group number and sort within groups by priority.
        group_to_indices = {}
        for idx in self.selected:
            wp = self.pair_table.get(idx)
            if not wp:
                continue
            try:
                # get group memberships at or after starting group
                if wp.groups and len(wp.groups) > 0:
                    groups = wp.groups
                    if max(groups) >= sg:
                        g = min([g for g in wp.groups if g >= sg])
                    else:
                        g = min(groups)
                else:
                    g = 999999
            except Exception:
                g = 999999
            # add this index to the list of indices for group g
            group_to_indices.setdefault(g, []).append(idx)

        all_groups = sorted(group_to_indices.keys())

        groups_in_order = sorted([g for g in all_groups if g >= sg]) + sorted([g for g in all_groups if g < sg])

        practice_indices = []
        defer_indices = []

        for g in groups_in_order:
            # take the indices in this group in random order
            indices = group_to_indices.get(g,[])

            if len(indices) > 0:
                for index in indices:
                    wp = self.pair_table.get(index)
                    ud = wp.user_data or ''
                    pp = self.get_practice_probability(ud,practice_percentage)

                    if random.random() < pp:
                        practice_indices.append(index)
                    elif pp > 0:
                        defer_indices.append(index)

        self.order = practice_indices + defer_indices

        # diagnostic: print word pairs in this order
        # for index in self.order:
        #     wp = self.pair_table.get(index)
        #     print("%4s %8s %-30s %-30s %-30s" % (index,wp.groups,wp.base,wp.foreign,wp.user_data))

    def get_num_to_practice(self):
        return len(self.order)

    def get_selected_pair(self, n):
        if n < 0 or n >= len(self.order):
            return None
        return self.pair_table[self.order[n]]

    def get_language(self, L):
        return self.languages[L]

    def change_num_known(self, c):
        self.num_known += c

    def revisit_later(self, n, L):
        # move item some positions later (with a small random jitter)
        # If L is None, use default distance=7; if L is an int>0, use that
        if n < 0 or n >= len(self.order):
            return
        import random
        try:
            distance = int(L) if L is not None else 10
        except Exception:
            distance = 7
        item = self.order.pop(n)
        jitter = random.randint(-1, 1)
        pos = n + distance + jitter
        if pos > len(self.order):
            pos = len(self.order)
        if pos < 0:
            pos = 0
        self.order.insert(pos, item)

    def write_user_data(self):
        if not self.userdata_filename:
            return
        # write entries sorted by (first_group, numeric index)
        entries = []
        for idx in self.indices:
            wp = self.pair_table.get(idx)
            if not wp:
                continue
            # determine first group (use large value if missing)
            try:
                g = int(wp.groups[0]) if wp.groups and len(wp.groups) > 0 else 999999
            except Exception:
                g = 999999
            try:
                ni = int(str(idx).strip())
            except Exception:
                try:
                    ni = int(''.join(ch for ch in str(idx) if ch.isdigit()) or 0)
                except Exception:
                    ni = 0
            entries.append((g, ni, idx, wp))

        entries.sort(key=lambda t: (t[0], t[1]))

        with open(self.userdata_filename, 'w', encoding='utf-8') as out:
            for g, ni, idx, wp in entries:
                if wp.user_data or wp.first_result != '?':
                    # avoid duplicating the first_result if it's already the trailing char of user_data
                    tail = wp.user_data or ''
                    fr = wp.first_result if wp.first_result != '?' else ''
                    if fr and tail.endswith(fr):
                        out.write(f"{idx}\t{tail}\n")
                    else:
                        out.write(f"{idx}\t{tail}{fr}\n")
                    # reset the transient first_result after writing so next interaction starts fresh
                    wp.first_result = '?'



class EditorWindow(tk.Toplevel):
    def __init__(self, master, wordlist, font_size=None, initial_geometry=None):
        super().__init__(master)
        self.title('Editor')
        self.wl = wordlist
        # apply saved geometry if provided
        try:
            if initial_geometry:
                self.geometry(initial_geometry)
        except Exception:
            pass
        # determine font size from parameter or master's config
        if font_size is not None:
            self.font_size = int(font_size)
        else:
            try:
                self.font_size = int(master.config.get('font_size', 12))
            except Exception:
                self.font_size = 12
        self.text_font = tkfont.Font(size=self.font_size)
        self._build()
        self._load_list()

    def _build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(frm, height=20)
        self.listbox.grid(row=0, column=0, rowspan=6, sticky=tk.NSEW)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        ttk.Label(frm, text='Index', font=self.text_font).grid(row=0, column=1, sticky=tk.W)
        self.idx_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.idx_var, font=self.text_font).grid(row=0, column=2, sticky=tk.EW)

        ttk.Label(frm, text='Base', font=self.text_font).grid(row=1, column=1, sticky=tk.W)
        self.base_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.base_var, font=self.text_font).grid(row=1, column=2, sticky=tk.EW)

        ttk.Label(frm, text='Foreign', font=self.text_font).grid(row=2, column=1, sticky=tk.W)
        self.foreign_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.foreign_var, font=self.text_font).grid(row=2, column=2, sticky=tk.EW)

        ttk.Label(frm, text='Groups (comma separated)', font=self.text_font).grid(row=3, column=1, sticky=tk.W)
        self.groups_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.groups_var, font=self.text_font).grid(row=3, column=2, sticky=tk.EW)

        ttk.Button(frm, text='Add/Update', command=self._add_update).grid(row=4, column=1)
        ttk.Button(frm, text='Remove', command=self._remove).grid(row=4, column=2)
        ttk.Button(frm, text='Save word list', command=self._save_wordlist).grid(row=5, column=1, columnspan=2)

        frm.columnconfigure(2, weight=1)
        frm.rowconfigure(0, weight=1)
        # ensure we save geometry when user closes via window manager
        try:
            self.protocol('WM_DELETE_WINDOW', self._on_close)
        except Exception:
            pass

    def _load_list(self):
        self.listbox.delete(0, tk.END)
        for idx in self.wl.indices:
            wp = self.wl.pair_table[idx]
            if not wp.removed:
                self.listbox.insert(tk.END, f"{idx}: {wp.base} | {wp.foreign} [{','.join(map(str, wp.groups))}]")

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        text = self.listbox.get(sel[0])
        idx = text.split(':', 1)[0]
        wp = self.wl.pair_table[idx]
        self.idx_var.set(wp.idx)
        self.base_var.set(wp.base)
        self.foreign_var.set(wp.foreign)
        self.groups_var.set(','.join(map(str, wp.groups)))

    def _add_update(self):
        idx = self.idx_var.get().strip()
        if not idx:
            messagebox.showwarning('Index required', 'Please enter an index')
            return
        base = self.base_var.get()
        foreign = self.foreign_var.get()
        # strip surrounding quotes if user pasted strings with quotes
        if len(base) >= 2 and base[0] == '"' and base[-1] == '"':
            base = base.replace('"', '')
        if len(foreign) >= 2 and foreign[0] == '"' and foreign[-1] == '"':
            foreign = foreign.replace('"', '')
        groups = [int(g) for g in self.groups_var.get().replace(',', ' ').split() if g.strip().isdigit()]
        wp = WordPair(idx, base, foreign, groups)
        self.wl.pair_table[idx] = wp
        if idx not in self.wl.indices:
            self.wl.indices.append(idx)
        self._load_list()

    def _remove(self):
        idx = self.idx_var.get().strip()
        if idx in self.wl.pair_table:
            self.wl.pair_table[idx].removed = True
        self._load_list()

    def _save_wordlist(self):
        try:
            # persist editor window geometry into master config before saving
            try:
                geom = self.geometry()
                if hasattr(self, 'master') and hasattr(self.master, 'config'):
                    try:
                        self.master.config['editor_geometry'] = geom
                        if hasattr(self.master, '_save_config'):
                            self.master._save_config()
                    except Exception:
                        pass
            except Exception:
                pass
            with open(self.wl.filename, 'w', encoding='utf-8') as out:
                out.write(f"{self.wl.languages[0]}\t{self.wl.languages[1]}\n")
                for idx in self.wl.indices:
                    wp = self.wl.pair_table[idx]
                    if wp.removed:
                        continue
                    groups_field = ','.join(map(str, wp.groups))
                    out.write(f"{idx}\t{wp.base}\t{wp.foreign}\t{groups_field}\n")
            messagebox.showinfo('Saved', 'Word list saved')
        except Exception as e:
            messagebox.showerror('Error', str(e))
    def _on_close(self):
        # save editor geometry into master config and close
        try:
            geom = self.geometry()
            if hasattr(self, 'master') and hasattr(self.master, 'config'):
                try:
                    self.master.config['editor_geometry'] = geom
                    if hasattr(self.master, '_save_config'):
                        self.master._save_config()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass
