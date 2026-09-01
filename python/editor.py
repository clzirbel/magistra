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
            # indices is a list of strings
            indices = group_to_indices.get(g,[])

            # shuffle the order of indices
            indices = list(indices)
            random.shuffle(indices)

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
        self.current_selected_idx = None
        self.displayed_indices = []
        self._suspend_filter_update = False
        self.filter_locked = False
        self.saved_filter_values = {'base': '', 'foreign': '', 'groups': ''}
        self.last_group_value = ''
        self.enter_add_next = False
        self._suspend_tree_select_event = False
        self.pair_id_populated = False
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
        # ensure the word-list area is wide enough to display full pairs
        try:
            self.minsize(1200, 520)
        except Exception:
            pass
        self._load_list()

    def _build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frm, columns=('pair_id', 'base', 'foreign', 'groups'), show='headings', height=24)
        self.tree.heading('pair_id', text='Pair ID', anchor=tk.W)
        self.tree.heading('base', text=self.wl.get_language(0), anchor=tk.W)
        self.tree.heading('foreign', text=self.wl.get_language(1), anchor=tk.W)
        self.tree.heading('groups', text='Group(s)', anchor=tk.W)
        self.tree.column('pair_id', width=80, anchor=tk.W, stretch=False)
        self.tree.column('base', width=360, anchor=tk.W, stretch=True)
        self.tree.column('foreign', width=360, anchor=tk.W, stretch=True)
        self.tree.column('groups', width=120, anchor=tk.W, stretch=False)
        self.tree.grid(row=0, column=0, rowspan=8, sticky=tk.NSEW, padx=(0, 12))
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        try:
            st = ttk.Style()
            st.configure('Treeview', font=self.text_font, rowheight=max(20, self.font_size + 8))
            st.configure('Treeview.Heading', font=self.text_font)
        except Exception:
            pass

        yscroll = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tree.yview)
        yscroll.grid(row=0, column=3, rowspan=8, sticky=tk.NS)
        self.tree.configure(yscrollcommand=yscroll.set)

        ttk.Label(frm, text='Pair ID', font=self.text_font).grid(row=0, column=1, sticky=tk.W)
        self.pair_id_var = tk.StringVar(value='')
        pair_id_entry = ttk.Entry(frm, textvariable=self.pair_id_var, font=self.text_font, width=10)
        pair_id_entry.grid(row=0, column=2, sticky=tk.W, pady=(0, 2))
        pair_id_entry.bind('<KeyRelease>', self._on_pair_id_changed)
        pair_id_entry.bind('<FocusOut>', self._on_pair_id_changed)
        pair_id_entry.bind('<Return>', self._on_pair_id_changed)
        ttk.Button(frm, text='New pair', command=self._new_pair).grid(row=1, column=2, sticky=tk.W, pady=(0, 4))

        ttk.Label(frm, text=self.wl.get_language(0), font=self.text_font).grid(row=2, column=1, sticky=tk.W)
        self.base_var = tk.StringVar()
        self.base_entry = ttk.Entry(frm, textvariable=self.base_var, font=self.text_font, width=60)
        self.base_entry.grid(row=2, column=2, sticky=tk.EW)
        self.base_var.trace_add('write', self._on_base_or_foreign_changed)
        self.base_entry.bind('<Return>', self._on_enter_update)

        ttk.Label(frm, text=self.wl.get_language(1), font=self.text_font).grid(row=3, column=1, sticky=tk.W)
        self.foreign_var = tk.StringVar()
        self.foreign_entry = ttk.Entry(frm, textvariable=self.foreign_var, font=self.text_font, width=60)
        self.foreign_entry.grid(row=3, column=2, sticky=tk.EW)
        self.foreign_var.trace_add('write', self._on_base_or_foreign_changed)
        self.foreign_entry.bind('<Return>', self._on_enter_update)

        ttk.Label(frm, text='Group(s)', font=self.text_font).grid(row=4, column=1, sticky=tk.W)
        self.groups_var = tk.StringVar()
        groups_entry = ttk.Entry(frm, textvariable=self.groups_var, font=self.text_font, width=60)
        groups_entry.grid(row=4, column=2, sticky=tk.EW)
        self.groups_var.trace_add('write', self._on_filter_changed)
        groups_entry.bind('<Return>', self._on_enter_update)

        ttk.Button(frm, text='Add/Update', command=self._add_update).grid(row=5, column=2, sticky=tk.W)
        ttk.Button(frm, text='Remove', command=self._remove).grid(row=5, column=2, sticky=tk.E)
        ttk.Button(frm, text='Clear', command=self._clear_fields).grid(row=6, column=2, sticky=tk.W)
        ttk.Button(frm, text='Save and Close', command=self._save_and_close).grid(row=6, column=2, sticky=tk.E)

        frm.columnconfigure(2, weight=1)
        # keep right-side controls anchored at top
        frm.rowconfigure(7, weight=1)
        # ensure we save geometry when user closes via window manager
        try:
            self.protocol('WM_DELETE_WINDOW', self._on_close)
        except Exception:
            pass
        # keyboard shortcuts: Esc (and common macOS analogue) clears editor fields
        try:
            self.bind('<Escape>', self._on_escape_clear)
        except Exception:
            pass

    def _matches_filters(self, wp, base_filter, foreign_filter, group_filter):
        if base_filter and base_filter not in (wp.base or '').lower():
            return False
        if foreign_filter and foreign_filter not in (wp.foreign or '').lower():
            return False
        if group_filter is not None:
            try:
                groups = list(wp.groups) if wp.groups else []
            except Exception:
                groups = []
            if group_filter not in groups:
                return False
        return True

    def _load_list(self, keep_pair_id=True):
        previous_pair_id = self._get_pair_id_number()
        if self.filter_locked:
            base_source = self.saved_filter_values.get('base', '')
            foreign_source = self.saved_filter_values.get('foreign', '')
            groups_source = self.saved_filter_values.get('groups', '')
        else:
            base_source = self.base_var.get() or ''
            foreign_source = self.foreign_var.get() or ''
            groups_source = self.groups_var.get() or ''

        base_filter = base_source.strip().lower()
        foreign_filter = foreign_source.strip().lower()
        groups_text = groups_source.strip()
        group_filter = None
        if groups_text:
            try:
                group_filter = int(groups_text)
            except Exception:
                # invalid integer filter -> no rows shown
                group_filter = '__invalid__'

        for iid in self.tree.get_children():
            self.tree.delete(iid)
        self.displayed_indices = []
        for idx in self.wl.indices:
            wp = self.wl.pair_table[idx]
            if wp.removed:
                continue
            if self._matches_filters(wp, base_filter, foreign_filter, group_filter):
                self.displayed_indices.append(idx)

        for i, idx in enumerate(self.displayed_indices, start=1):
            wp = self.wl.pair_table[idx]
            self.tree.insert(
                '',
                tk.END,
                iid=str(i),
                values=(str(i), wp.base, wp.foreign, ','.join(map(str, wp.groups)))
            )

        if not self.displayed_indices:
            self.current_selected_idx = None
            self.pair_id_var.set('')
            self.pair_id_populated = False
            try:
                self.tree.selection_remove(self.tree.selection())
            except Exception:
                pass
            return

        if keep_pair_id and previous_pair_id is not None and 1 <= previous_pair_id <= len(self.displayed_indices):
            target_pair_id = previous_pair_id
            self.pair_id_var.set(str(target_pair_id))
            self.current_selected_idx = self.displayed_indices[target_pair_id - 1]
            self.pair_id_populated = True
            try:
                self._suspend_tree_select_event = True
                self.tree.selection_set(str(target_pair_id))
                self.tree.see(str(target_pair_id))
            except Exception:
                pass
            finally:
                self._suspend_tree_select_event = False
        else:
            self.current_selected_idx = None
            self.pair_id_var.set('')
            self.pair_id_populated = False
            try:
                self.tree.selection_remove(self.tree.selection())
            except Exception:
                pass

    def _capture_filter_values_before_pair_selection(self):
        self.saved_filter_values = {
            'base': self.base_var.get() or '',
            'foreign': self.foreign_var.get() or '',
            'groups': self.groups_var.get() or ''
        }

    def _restore_saved_filter_values(self):
        self._suspend_filter_update = True
        try:
            self.base_var.set(self.saved_filter_values.get('base', ''))
            self.foreign_var.set(self.saved_filter_values.get('foreign', ''))
            self.groups_var.set(self.saved_filter_values.get('groups', ''))
        finally:
            self._suspend_filter_update = False

    def _activate_pair_selection(self, idx, pair_id):
        if idx is None:
            return
        if not self.filter_locked:
            self._capture_filter_values_before_pair_selection()
        self.filter_locked = True
        self.current_selected_idx = idx
        self._fill_fields_from_idx(idx)
        self.pair_id_var.set(str(pair_id))
        self.enter_add_next = False
        self.pair_id_populated = True
        try:
            current = self.tree.selection()
            if not current or current[0] != str(pair_id):
                self._suspend_tree_select_event = True
                self.tree.selection_set(str(pair_id))
                self.tree.see(str(pair_id))
        except Exception:
            pass
        finally:
            self._suspend_tree_select_event = False

    def _next_index(self):
        highest = 0
        for raw_idx in self.wl.indices:
            s = str(raw_idx).strip()
            if s.isdigit():
                n = int(s)
                if n > highest:
                    highest = n
        return str(highest + 1)

    def _get_pair_id_number(self):
        try:
            n = int((self.pair_id_var.get() or '').strip())
        except Exception:
            return None
        if n < 1:
            return None
        return n

    def _get_idx_for_pair_id(self):
        pair_id = self._get_pair_id_number()
        if pair_id is None:
            return None
        if pair_id > len(self.displayed_indices):
            return None
        return self.displayed_indices[pair_id - 1]

    def _fill_fields_from_idx(self, idx):
        if idx is None or idx not in self.wl.pair_table:
            return
        wp = self.wl.pair_table[idx]
        self._suspend_filter_update = True
        try:
            self.base_var.set(wp.base)
            self.foreign_var.set(wp.foreign)
            self.groups_var.set(','.join(map(str, wp.groups)))
        finally:
            self._suspend_filter_update = False

    def _on_pair_id_changed(self, event=None):
        idx = self._get_idx_for_pair_id()
        if idx is None:
            self.current_selected_idx = None
            self.pair_id_populated = False
            if not (self.pair_id_var.get() or '').strip():
                try:
                    self.tree.selection_remove(self.tree.selection())
                except Exception:
                    pass
            return
        pair_id = self._get_pair_id_number()
        if pair_id is None:
            return
        self._activate_pair_selection(idx, pair_id)

    def _on_base_or_foreign_changed(self, *args):
        # When both text fields are filled and Group(s) is empty, reuse the most
        # recently saved Group(s) value to speed up adding many pairs.
        if not self._suspend_filter_update:
            base_text = (self.base_var.get() or '').strip()
            foreign_text = (self.foreign_var.get() or '').strip()
            groups_text = (self.groups_var.get() or '').strip()
            if base_text and foreign_text and (not groups_text) and self.last_group_value:
                self._suspend_filter_update = True
                try:
                    self.groups_var.set(self.last_group_value)
                finally:
                    self._suspend_filter_update = False
        self._on_filter_changed()

    def _on_filter_changed(self, *args):
        if self._suspend_filter_update:
            return
        if self.filter_locked:
            return
        self._load_list(keep_pair_id=True)

    def _on_select(self, event=None):
        if self._suspend_tree_select_event:
            return
        sel = self.tree.selection()
        if not sel:
            self.current_selected_idx = None
            self.pair_id_populated = False
            return
        try:
            pair_id = int(str(sel[0]))
        except Exception:
            return
        list_row = pair_id - 1
        if list_row < 0 or list_row >= len(self.displayed_indices):
            return
        idx = self.displayed_indices[list_row]
        self._activate_pair_selection(idx, pair_id)

    def _on_enter_update(self, event=None):
        base_text = (self.base_var.get() or '').strip()
        foreign_text = (self.foreign_var.get() or '').strip()
        groups_text = (self.groups_var.get() or '').strip()

        if self.pair_id_populated and self.current_selected_idx is not None:
            if base_text and foreign_text and groups_text:
                self._add_update(force_new=False)
            return 'break'

        if self.enter_add_next:
            if base_text and foreign_text and groups_text:
                self._add_update(force_new=True)
                self.enter_add_next = False
            return 'break'

        # if search/filter currently shows no pairs, Enter can create a new pair
        if len(self.displayed_indices) == 0:
            if base_text and foreign_text and groups_text:
                self._add_update(force_new=True)
        return 'break'

    def _on_escape_clear(self, event=None):
        self._clear_fields()
        return 'break'

    def _add_update(self, force_new=False):
        base = self.base_var.get()
        foreign = self.foreign_var.get()
        groups_text_raw = self.groups_var.get() or ''
        # strip surrounding quotes if user pasted strings with quotes
        if len(base) >= 2 and base[0] == '"' and base[-1] == '"':
            base = base.replace('"', '')
        if len(foreign) >= 2 and foreign[0] == '"' and foreign[-1] == '"':
            foreign = foreign.replace('"', '')
        groups = [int(g) for g in groups_text_raw.replace(',', ' ').split() if g.strip().isdigit()]
        if groups_text_raw.strip():
            self.last_group_value = groups_text_raw.strip()

        idx = None
        was_existing = False
        if not force_new:
            idx = self._get_idx_for_pair_id()
            if idx is not None:
                existing = self.wl.pair_table.get(idx)
                if existing is None or existing.removed:
                    idx = None
                else:
                    was_existing = True
        if not idx:
            idx = self._next_index()

        wp = WordPair(idx, base, foreign, groups)
        self.wl.pair_table[idx] = wp
        if idx not in self.wl.indices:
            self.wl.indices.append(idx)
        self.current_selected_idx = idx
        if was_existing:
            self.filter_locked = True
        self._load_list(keep_pair_id=True)

    def _remove(self):
        if not self.pair_id_populated:
            return
        idx = self._get_idx_for_pair_id()
        if idx in self.wl.pair_table:
            self.wl.pair_table[idx].removed = True
        self.current_selected_idx = None
        self.pair_id_populated = False
        self.filter_locked = False
        self.pair_id_var.set('')
        self._restore_saved_filter_values()
        self._load_list(keep_pair_id=True)

    def _clear_fields(self):
        self.filter_locked = False
        self.current_selected_idx = None
        self.pair_id_populated = False
        self.enter_add_next = False
        self._suspend_filter_update = True
        try:
            self.base_var.set('')
            self.foreign_var.set('')
            self.groups_var.set('')
            self.pair_id_var.set('')
        finally:
            self._suspend_filter_update = False
        self.saved_filter_values = {'base': '', 'foreign': '', 'groups': ''}
        self._load_list(keep_pair_id=False)
        try:
            self.base_entry.focus_set()
        except Exception:
            pass

    def _new_pair(self):
        self._capture_filter_values_before_pair_selection()
        self.filter_locked = True
        self.current_selected_idx = None
        self.pair_id_populated = False
        self.pair_id_var.set('')
        self.enter_add_next = True
        self._suspend_filter_update = True
        try:
            self.base_var.set('')
            self.foreign_var.set('')
            if self.last_group_value:
                self.groups_var.set(self.last_group_value)
        finally:
            self._suspend_filter_update = False
        try:
            self.tree.selection_remove(self.tree.selection())
        except Exception:
            pass

    def _save_wordlist(self, show_message=True):
        try:
            # persist editor window geometry into master config before saving
            self._persist_editor_geometry()
            with open(self.wl.filename, 'w', encoding='utf-8') as out:
                out.write(f"{self.wl.languages[0]}\t{self.wl.languages[1]}\n")
                for idx in self.wl.indices:
                    wp = self.wl.pair_table[idx]
                    if wp.removed:
                        continue
                    groups_field = ','.join(map(str, wp.groups))
                    out.write(f"{idx}\t{wp.base}\t{wp.foreign}\t{groups_field}\n")
            if show_message:
                messagebox.showinfo('Saved', 'Word list saved')
            return True
        except Exception as e:
            messagebox.showerror('Error', str(e))
            return False

    def _persist_editor_geometry(self):
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

    def _return_to_welcome(self):
        try:
            if hasattr(self, 'master') and self.master is not None:
                self.master.deiconify()
                self.master.lift()
                self.master.focus_force()
        except Exception:
            pass

    def _save_and_close(self):
        if self._save_wordlist(show_message=False):
            try:
                self.destroy()
            except Exception:
                pass
            self._return_to_welcome()

    def _on_close(self):
        choice = messagebox.askyesnocancel(
            'Close editor',
            'Save changes before closing?\n\nYes = Save\nNo = Quit without saving\nCancel = Cancel'
        )
        if choice is None:
            return
        if choice:
            if not self._save_wordlist(show_message=False):
                return
        # choice == False means quit without saving
        self._persist_editor_geometry()
        try:
            self.destroy()
        except Exception:
            pass
        self._return_to_welcome()
