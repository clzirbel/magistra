import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import unicodedata
import re
import collections
import os
import time

def _normalize_text(s: str) -> str:
    if s is None:
        return ''
    # lowercase and strip
    t = s.lower().strip()
    # map common ligatures and special letters before decomposition
    t = t.replace('ß', 'ss').replace('æ', 'ae').replace('œ', 'oe')
    t = t.replace('Æ', 'ae').replace('Œ', 'oe').replace('ø', 'o').replace('ø', 'o')
    t = t.replace('Ø', 'o').replace('ł', 'l').replace('Ł', 'l')
    # decompose accents and remove combining marks
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Mn')
    # remove punctuation except keep hyphen and apostrophe, remove inverted punctuation like ¿ ¡ and other symbols
    cleaned = []
    for ch in t:
        if ch.isalnum() or ch.isspace() or ch in ("-", "'", "’"):
            cleaned.append(ch)
        # skip all other punctuation
    t = ''.join(cleaned)
    # normalize whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def _evaluate_known(pair_data,mode):
    """
    Evaluate the contribution of pair_data to the total Known in the given mode
    """
    if mode == 'Exact':
        if pair_data.endswith('++') or pair_data.endswith('P+'):
            return 1
        else:
            return 0
    elif mode == 'Basic':
        if pair_data.endswith('++') or pair_data.endswith('P+'):
            return 1
        elif pair_data.endswith('&&') or pair_data.endswith('P&'):
            return 1
        elif pair_data.endswith('&+') or pair_data.endswith('+&'):
            return 1
        else:
            return 0

def get_best_match(raw, L, text):
    """
    Return (best_candidate, prefix_len, exact_match).
    Chooses the candidate with the longest case-insensitive matching prefix
    with the user's `text`. Exact matches (case-sensitive or -insensitive)
    are reported as exact_match=True with prefix_len equal to full length.
    """
    candidates = [s.strip() for s in raw.split(';')]
    a = (text or '').strip()
    if not candidates:
        return ('', 0, False)
    # check exact matches first
    for c in candidates:
        if a == c:
            return (c, len(c), True)
    al = a.lower()
    for c in candidates:
        if c.lower() == al:
            return (c, len(c), True)
    # find candidate with longest prefix match (case-insensitive)
    best = candidates[0]
    best_len = 0
    for c in candidates:
        i = 0
        cl = c.lower()
        while i < len(al) and i < len(cl) and al[i] == cl[i]:
            i += 1
        if i > best_len:
            best_len = i
            best = c
    return (best, best_len, False)

def portion_correct(raw, L, text):
    best, n, exact = get_best_match(raw, L, text)
    # return prefix (correct part) and remainder separated by arrow for debugging
    return best[:n] + ' -> ' + text[n:]

class PracticeDialog(tk.Toplevel):
    def __init__(self, master, wordlist, font_size=None, initial_geometry=None, mode=None):
        super().__init__(master)
        self.title("Practice")
        self.wl = wordlist
        self.direction = 0  # 0: base->foreign, 1: foreign->base
        self.mode = mode
        self.index = 0
        self.history = ""
        # determine font size: explicit param, or master's config, or default 12
        if font_size is not None:
            self.font_size = int(font_size)
        else:
            try:
                self.font_size = int(master.config.get('font_size', 12))
            except Exception:
                self.font_size = 12

        # self._build() gets run only once; changes to fields happen immediately
        self._build()

        self._load_pair()

        # ensure mode is set (fallback to master's mode_var if needed)
        try:
            if not self.mode and hasattr(self.master, 'mode_var'):
                self.mode = self.master.mode_var.get()
        except Exception:
            pass
        # ensure the practice window asks before closing
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # make window transient to master only if master is visible; otherwise keep as standalone
        try:
            if self.master is not None and str(self.master.state()) != 'withdrawn':
                self.transient(self.master)
        except Exception:
            pass
        # ensure dialog is visible and on top, then schedule focusing the entry
        try:
            # apply saved geometry if provided
            try:
                if initial_geometry:
                    self.geometry(initial_geometry)
            except Exception:
                pass
            # if no saved geometry, apply a wider default so buttons fit
            try:
                if not initial_geometry:
                    width = 640 + max(0, (self.font_size - 12) * 30)
                    height = 320 + max(0, (self.font_size - 12) * 20)
                    self.geometry(f"{width}x{height}")
            except Exception:
                pass
            self.deiconify()
            self.lift()
            self.update_idletasks()
            # lock minimum size to the opening size so it doesn't shrink during updates
            try:
                w = self.winfo_width()
                h = self.winfo_height()
                if w > 0 and h > 0:
                    self.minsize(w, h)
            except Exception:
                pass
        except Exception:
            pass
        # try:
        #     # wait a short time for the window to become visible before focusing the entry
        #     self.after(150, lambda: self.entry.focus_set())
        # except Exception:
        #     pass

        # try another way to put the focus on the entry field
        # print('Pausing')
        # time.sleep(0.2)
        # print('Setting focus')
        # self.entry.focus_set()

        self.after(100, lambda: (
        self.lift(),
        self.focus_force(),
        self.entry.focus_force()
        ))

        self.after(100, self.entry.focus_force)

    def _build(self):
        """
        Set up the practice window, once per session.
        """

        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        # fonts
        self.text_font = tkfont.Font(size=self.font_size)

        # group number on the first (top) line, left-justified
        ttk.Label(frm, text="Group", font=self.text_font).grid(row=0, column=0, sticky=tk.W)
        self.group_val = ttk.Label(frm, text="", font=self.text_font)
        self.group_val.grid(row=0, column=1, sticky=tk.W, padx=(12,0))

        # base language prompt and word (aligned)
        ttk.Label(frm, text=self.wl.get_language(0), font=self.text_font).grid(row=1, column=0, sticky=tk.W, pady=(6,0))
        self.word_lbl = ttk.Label(frm, text="", font=self.text_font)
        self.word_lbl.grid(row=1, column=1, sticky=tk.W, pady=(6,0), padx=(12,0))

        # input prompt (placed below group)
        ttk.Label(frm, text=self.wl.get_language(1), font=self.text_font).grid(row=2, column=0, sticky=tk.W, pady=(6,0))
        self.entry = ttk.Entry(frm, width=40, font=self.text_font)
        self.entry.grid(row=2, column=1, sticky=tk.EW, padx=(12,0), pady=(6,0))
        self.entry.bind('<Return>', self._on_submit)

        # Feedback label and result area: label (no colon) + inline labels for prefix and incorrect part
        # feedback/preview label (text changes per-pair)
        self.feedback_label = ttk.Label(frm, text="Feedback", font=self.text_font)
        self.feedback_label.grid(row=4, column=0, sticky=tk.W, pady=(8,0))
        feedback_frame = ttk.Frame(frm)
        feedback_frame.grid(row=4, column=1, sticky=tk.W, pady=(8,0), padx=(12,0))
        # configure strike font (create before labels so it's available)
        try:
            self.strike_font = tkfont.Font(size=self.font_size, overstrike=1)
        except Exception:
            self.strike_font = tkfont.Font(size=self.font_size)
        # correct prefix (black)
        self.result_prefix = ttk.Label(feedback_frame, text="", font=self.text_font)
        self.result_prefix.pack(side=tk.LEFT, padx=0)
        # incorrect trailing part (red + strikethrough)
        self.result_incorrect = ttk.Label(feedback_frame, text="", font=self.strike_font, foreground='red')
        self.result_incorrect.pack(side=tk.LEFT, padx=0)

        # history label (no colon) - placed above the buttons and aligned with input
        ttk.Label(frm, text="History", font=self.text_font).grid(row=5, column=0, sticky=tk.W, pady=(8,0))
        self.history_val = ttk.Label(frm, text="", font=self.text_font)
        self.history_val.grid(row=5, column=1, sticky=tk.W, pady=(8,0), padx=(12,0))

        # Mode status line (between History and Known)
        ttk.Label(frm, text="Mode", font=self.text_font).grid(row=6, column=0, sticky=tk.W)
        self.mode_status = ttk.Label(frm, text="", font=self.text_font)
        self.mode_status.grid(row=6, column=1, sticky=tk.W, padx=(12,0))

        # Known label under Mode
        ttk.Label(frm, text="Known", font=self.text_font).grid(row=7, column=0, sticky=tk.W)
        self.known_val = ttk.Label(frm, text="0", font=self.text_font)
        self.known_val.grid(row=7, column=1, sticky=tk.W, padx=(12,0))

        btnfrm = ttk.Frame(frm)
        btnfrm.grid(row=8, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btnfrm, text="Skip once", command=self._skip_once).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnfrm, text="Skip forever", command=self._skip_forever).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnfrm, text="A-", command=self._decrease_font).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnfrm, text="A+", command=self._increase_font).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnfrm, text="Switch direction", command=self._switch_dir).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnfrm, text="Save and close", command=self._save_and_close).pack(side=tk.LEFT, padx=8)

        frm.columnconfigure(1, weight=1)
        # make left column wider so prompt values align with entry
        # leave column sizing to grid but provide modest left column width
        try:
            frm.grid_columnconfigure(0, minsize=max(80, self.font_size * 6))
        except Exception:
            pass

    def _load_pair(self):

        # track recently-correctly-answered pair ids to avoid immediate repetition
        # self.recently_correct = collections.deque(maxlen=12)

        # track the number of attempts to be able to give credit for a correct answer
        self.attempt_number = 0

        if self.index >= self.wl.get_num_to_practice():
            # no pairs to practice
            self.word_lbl.config(text="")
            self._set_result_text("No more pairs to practice")
            try:
                self.entry.configure(state='disabled')
            except Exception:
                pass
            return

        wp = self.wl.get_selected_pair(self.index)
        self.current_wp = wp

        # show base word when direction==0, otherwise show foreign
        if self.direction == 0:
            self.word_lbl.config(text=wp.base)
        else:
            self.word_lbl.config(text=wp.foreign)

        # clear the input text field
        self.entry.delete(0, tk.END)

        # show all of the groups that this word pair is in
        groups = ",".join([str(g) for g in wp.groups]) if (wp.groups and len(wp.groups) > 0) else ''
        self.group_val.config(text=groups)

        # show cleaned user history
        user_history = (wp.user_data or "")
        cleaned_history = user_history[-40:]
        # convert internal symbols to simplified display.
        if getattr(self, 'mode', None) == 'Exact':
            # in Exact mode, show '&' as '&' (do not convert it to '+')
            disp = cleaned_history.replace('#', '+').replace('_', '-').replace('=', '-')
        else:
            # Basic mode: merge +/#/& -> + and -/_/= -> -
            disp = cleaned_history.replace('#', '+').replace('_', '-').replace('=', '-').replace('&', '+')
        self.history_val.config(text=disp)

        # Diagnostic: print base word then history + pair idx

        # adjust feedback/preview label: show 'Preview' when the pair has never
        # been presented (no user_data), otherwise show 'Feedback'
        try:
            if not user_history:
                self.feedback_label.config(text="Preview")
            else:
                self.feedback_label.config(text="Feedback")
        except Exception:
            pass

        # If this pair has never been presented before, behave as a Preview
        # show the correct answer but DO NOT modify history yet; only when the
        # user subsequently types the correct answer do we record the preview
        # in the user_data (as 'P'). Mark the dialog as preview-active so other
        # handlers can adjust behavior.
        if user_history:
            # user has practiced this pair before
            self._set_result_text("")
        else:
            target = wp.foreign if self.direction == 0 else wp.base
            try:
                self._set_result_text(target)
            except Exception:
                pass

        # compute known count (ensure accurate before first display)
        try:
            # compute known count according to current mode
            self._update_known_display()
        except Exception:
            try:
                self.known_val.config(text=str(self.wl.get_num_known()))
            except Exception:
                self.known_val.config(text='0')

        # schedule focus for the entry so user can type immediately once visible
        # why does this not work when the window is first opened?
        try:
            self.after(150, lambda: self.entry.focus_set())
        except Exception:
            pass


    def _on_submit(self, event=None):

        mode = getattr(self, 'mode', None) or getattr(self.master, 'config', {}).get('mode', 'Basic')

        # increment the attempt number
        self.attempt_number += 1

        # Rewritten submission handling with mode-aware correctness
        # trim trailing spaces from user input; exact comparisons also strip internally
        answer = self.entry.get()
        if answer is None:
            answer = ''
        # remove only trailing spaces here as requested
        answer = answer.rstrip()

        # get pair information
        wp = self.current_wp

        target = wp.foreign if self.direction == 0 else wp.base
        if target is None:
            target = ''
        target = target.rstrip()

        user_history = wp.user_data or ''

        # if the user presses Enter with no response at all, reveal the target
        # and force the user to type it
        # raise the attempt counter so the user history gets marked wrong
        if answer == "":
            if self.attempt_number < 20:
                if self.direction == 1:
                    wp.modify_pair_data('=')
                elif mode == 'Basic':
                    wp.modify_pair_data('_')
                else:
                    wp.modify_pair_data('-')
                self.attempt_number = 20
            try:
                self._set_result_text(target)
                self.result_prefix.config(foreground='black')
            except Exception:
                pass
            return

        # if entry blank and user has not yet asked for reveal, reveal correct and require typing
        # (do not use this path while waiting for the single retry after a wrong attempt)
        # if answer == "" and not getattr(self, 'awaiting_forced_entry', False) and not getattr(self, 'awaiting_second_try', False):
        #     # reveal correct answer and force typing
        #     # record that the pair was presented (append '-' or '_' once depending on mode) so presentation is saved
        #     mode = getattr(self, 'mode', None) or getattr(self.master, 'config', {}).get('mode', 'Basic')
        #     if wp.first_result == '?':
        #         # do not mark preview here; marking occurs on correct typing
        #         # but record that it was presented as a reveal marker: use '-' for Exact, '_' for Basic
        #         mark = '-' if mode != 'Basic' else '_'
        #         wp.modify_pair_data(mark)
        #         wp.set_first_result(mark)
        #         try:
        #             print((wp.user_data or ''), wp.idx, flush=True)
        #         except Exception:
        #             pass
        #     self._set_result_text(target)
        #     self.awaiting_forced_entry = True
        #     return

        # evaluate a non-empty answer

        # allowable answers are separated by ;
        candidates = [s.strip() for s in target.split(';')]

        # exact match to one of the correct answers
        exact_ok = any(c == answer for c in candidates)

        basic_ok = exact_ok
        if mode == 'Exact':
            ok = exact_ok
        elif mode == 'Basic':
            # Basic mode: accept normalized match as well
            norm_answer = _normalize_text(answer)
            basic_ok = any(_normalize_text(c) == norm_answer for c in candidates)
            ok = exact_ok or basic_ok

        if ok:
            # correct answer
            if not user_history:
                # handle previewed pairs: mark 'P' in user history
                wp.modify_pair_data('P')

                # now that the user got this pair right, re-insert this pair about
                # 12 pairs later so the user has to practice it again
                try:
                    self.wl.revisit_later(self.index, 12)
                except Exception:
                    pass

            else:
                # record correct answer if it was given quickly enough
                if self.attempt_number <= 2:
                    if self.direction == 1:
                        wp.modify_pair_data('#')
                    elif mode == 'Basic':
                        # in Basic mode: exact matches get '+', normalized-only matches get '&'
                        if exact_ok:
                            wp.modify_pair_data('+')
                            wp.set_first_result('+')
                        else:
                            wp.modify_pair_data('&')
                            wp.set_first_result('&')
                    else:
                        wp.modify_pair_data('+')
                        wp.set_first_result('+')

            # diagnostic printing
            # try:
            #     print(wp.idx, (wp.user_data or ''), basic_ok, exact_ok, flush=True)
            # except Exception:
            #     pass

            # user history for the pair just finished does not need to be updated; next pair will be shown
            # clear result and update history display
            # self._set_result_text("")
            # self.awaiting_second_try = False
            # user_history = (wp.user_data or "")
            # if len(user_history) > 1 and wp.first_result != '?' and user_history.endswith(wp.first_result):
            #     cleaned_history = user_history[:-1][-40:]
            # else:
            #     cleaned_history = user_history[-40:]
            #     try:
            #         if getattr(self, 'mode', None) == 'Exact':
            #             disp = cleaned_history.replace('#', '+').replace('_', '-').replace('=', '-')
            #         else:
            #             disp = cleaned_history.replace('#', '+').replace('&', '+').replace('_', '-').replace('=', '-')
            #         self.history_val.config(text=disp)
            #     except Exception:
            #         pass

            # known count will be updated when the next word pair is presented, no need to do it here
            # re-compute and update known count
            # try:
            #     self._update_known_display()
            # except Exception:
            #     try:
            #         self._update_known_display()
            #     except Exception:
            #         try:
            #             self.known_val.config(text=str(self.wl.get_num_known()))
            #         except Exception:
            #             pass

            # save the user history after each correct answer even though it's overkill
            try:
                self.wl.write_user_data()
            except Exception:
                pass

            # if Basic mode and normalized match but not exact, show full correct in blue briefly
            if mode == 'Basic' and basic_ok and not exact_ok:
                correct_display = candidates[0]

                try:
                    self.result_prefix.config(text=correct_display, foreground='blue')
                    self.result_incorrect.config(text="")
                except Exception:
                    pass

                def _continue():
                    try:
                        self.result_prefix.config(foreground='black')
                    except Exception:
                        pass

                # have tkinter change the text color and display it
                self.update_idletasks()

                try:
                    # show blue full-correct for 1.5 seconds in Basic mode
                    # self.after(1500, _continue)
                    time.sleep(1.5)
                    # self.result_prefix.config(foreground='black')
                except Exception:
                    pass

            # advance to the next word pair in the ordering
            self.index += 1
            self._load_pair()

            return

        if self.attempt_number >= 2 and self.attempt_number < 20:
            # typed correctly but not on the first or second try
            if self.direction == 1:
                wp.modify_pair_data('=')
            elif mode == 'Basic':
                wp.modify_pair_data('_')
            else:
                wp.modify_pair_data('-')
            self.attempt_number = 20

        # incorrect answer: compute best match and show feedback
        # choose candidate with longest normalized prefix match

        # For Basic mode, compute original-character prefix length matching under normalization
        if mode == 'Basic':
            def orig_norm_prefix_len(orig, user):
                maxk = min(len(orig), len(user))
                k = 0
                for j in range(maxk):
                    if _normalize_text(orig[:j+1]) == _normalize_text(user[:j+1]):
                        k = j+1
                    else:
                        break
                return k

            norm_candidates = [(c, _normalize_text(c)) for c in candidates]
            best_c = candidates[0]
            best_norm = norm_candidates[0][1]
            best_len = 0
            for orig, nc in norm_candidates:
                # compute normalized common prefix length
                i = 0
                while i < len(nc) and i < len(norm_answer) and nc[i] == norm_answer[i]:
                    i += 1
                if i > best_len:
                    best_len = i
                    best_c = orig
                    best_norm = nc

            k = orig_norm_prefix_len(best_c, answer)
            correct_prefix = best_c[:k]
            if len(answer) > 0 and len(_normalize_text(answer)) < len(_normalize_text(best_c)) and _normalize_text(best_c).startswith(_normalize_text(answer)):
                incorrect_part = '---'
            else:
                incorrect_part = answer[k:]
        else:
            # Use the original get_best_match for Exact-like feedback
            best_candidate, i, exact = get_best_match(target, 1 - self.direction, answer)
            correct_prefix = best_candidate[:i]
            incorrect_part = answer[i:]
            if len(answer) > 0 and len(answer) < len(best_candidate) and best_candidate.lower().startswith(answer.lower()):
                correct_prefix = answer
                incorrect_part = '---'

        # record what parts were right and wrong, _build will color them
        self._set_result_text((correct_prefix, incorrect_part))
        try:
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
        except Exception:
            pass

        # # Second and later wrong: reveal full correct answer and mark as wrong.
        # if wp.first_result == '?' and not getattr(self, 'preview_active', False):
        #     mark = '_' if mode == 'Basic' else '-'
        #     wp.modify_pair_data(mark)
        #     wp.set_first_result(mark)
        #     try:
        #         print(wp.idx, (wp.user_data or ''), flush=True)
        #     except Exception:
        #         pass

        # self.awaiting_second_try = False
        # self.awaiting_forced_entry = False

        # show full correct answer (first candidate), then move on
        # correct_full = candidates[0] if candidates else target
        # self._set_result_text(correct_full)

        # no need to update the display of the history while they are re-trying the pair
        # update history display now that wrong symbol was recorded
        # user_history = (wp.user_data or "")
        # if len(user_history) > 1 and wp.first_result != '?' and user_history.endswith(wp.first_result):
        #     cleaned_history = user_history[:-1][-40:]
        # else:
        #     cleaned_history = user_history[-40:]
        # try:
        #     if getattr(self, 'mode', None) == 'Exact':
        #         disp = cleaned_history.replace('#', '+').replace('_', '-').replace('=', '-')
        #     else:
        #         disp = cleaned_history.replace('#', '+').replace('&', '+').replace('_', '-').replace('=', '-')
        #     self.history_val.config(text=disp)
        # except Exception:
        #     pass

        # def _advance_after_wrong():
        #     try:
        #         self.index += 1
        #         self._load_pair()
        #     except Exception:
        #         pass

        # try:
        #     self.after(1200, _advance_after_wrong)
        # except Exception:
        #     self.index += 1
        #     self._load_pair()

    def _skip_once(self):
        self.index += 1
        self._load_pair()

    def _skip_forever(self):
        self.current_wp.modify_pair_data('f')
        self.history += 'f'
        # Diagnostic: print updated history after skip-forever
        try:
            print((self.current_wp.user_data or ''), self.current_wp.idx, flush=True)
        except Exception:
            pass
        self.index += 1
        self._load_pair()

    def _switch_dir(self):
        self.direction = 1 - self.direction
        self._load_pair()

    def _save_and_close(self):
        # save this dialog's geometry into the master's config so next run restores it
        try:
            geom = self.geometry()
            if hasattr(self, 'master') and hasattr(self.master, 'config'):
                try:
                    self.master.config['practice_geometry'] = geom
                    if hasattr(self.master, '_save_config'):
                        self.master._save_config()
                except Exception:
                    pass
        except Exception:
            pass
        # persist per-user mode into the user's userdata meta before writing
        # write user data only (do not persist mode in the userdata file)
        try:
            self.wl.write_user_data()
        except Exception:
            pass
        # restore the master (welcome) window if it was hidden
        try:
            if self.master is not None:
                try:
                    self.master.deiconify()
                except Exception:
                    pass
        except Exception:
            pass
        self.destroy()

    def _on_close(self):
        # Ask user: Save your progress? Yes/No/Cancel
        res = messagebox.askyesnocancel("Save your progress?", "Save your progress?")
        if res is None:
            # Cancel
            return
        if res is True:
            # Yes: save and close
            self._save_and_close()
            return
        # No: do not save, just close and restore master
        try:
            if self.master is not None:
                try:
                    self.master.deiconify()
                except Exception:
                    pass
        except Exception:
            pass
        self.destroy()

    def _increase_font(self):
        self.font_size += 2
        self._apply_font()

    def _decrease_font(self):
        if self.font_size > 6:
            self.font_size -= 2
        self._apply_font()

    def _apply_font(self):
        # update font object and reconfigure widgets
        try:
            self.text_font.configure(size=self.font_size)
        except Exception:
            self.text_font = tkfont.Font(size=self.font_size)
        for w in (self.word_lbl, self.entry, self.history_val, self.group_val, self.known_val):
            try:
                w.configure(font=self.text_font)
            except Exception:
                pass
        # update strike font and result_text tag
        try:
            self.strike_font.configure(size=self.font_size)
        except Exception:
            self.strike_font = tkfont.Font(size=self.font_size, overstrike=1)
        try:
            # apply fonts to result labels
            self.result_prefix.configure(font=self.text_font)
            self.result_incorrect.configure(font=self.strike_font, foreground='red')
        except Exception:
            pass
    def _update_known_display(self):
        # Update the Known count label according to mode.
        try:
            mode = getattr(self, 'mode', None) or getattr(self.master, 'config', {}).get('mode', 'Basic')
            if mode == 'Basic':
                # count pairs whose user_data ends with one of the Basic-mode known markers
                # Basic-mode known markers: '&&', 'P&', 'P+', '++', '&+', '+&'
                count = 0
                for p in self.wl.pair_table.values():
                    ud = (p.user_data or '')
                    if ud.endswith('&&') or ud.endswith('P&') or ud.endswith('P+') or ud.endswith('++') or ud.endswith('&+') or ud.endswith('+&'):
                        count += 1
                self.wl.num_known = count
                try:
                    # set Mode status text and Known count (number only)
                    self.mode_status.config(text="Basic: OK to miss accents, capitalization, and punctuation")
                except Exception:
                    pass
            else:
                # count pairs whose user_data ends with one of the Basic-mode known markers
                # Basic-mode known markers: '&&', 'P&', 'P+', '++', '&+', '+&'
                count = 0
                for p in self.wl.pair_table.values():
                    ud = (p.user_data or '')
                    if ud.endswith('&&') or ud.endswith('P&') or ud.endswith('P+') or ud.endswith('++') or ud.endswith('&+') or ud.endswith('+&'):
                        count += 1
                self.wl.num_known = count
                try:
                    # set Mode status text and Known count (number only)
                    self.mode_status.config(text="Exact: type every character correctly")
                except Exception:
                    pass
            try:
                self.known_val.config(text=str(count))
            except Exception:
                pass
        except Exception:
            try:
                self.known_val.config(text=str(0))
            except Exception:
                self.known_val.config(text='0')
        # update global button style and save config via master
        try:
            style = ttk.Style()
            style.configure('TButton', font=self.text_font)
        except Exception:
            pass
        try:
            # persist new font size in master config
            if hasattr(self.master, 'config'):
                self.master.config['font_size'] = int(self.font_size)
            if hasattr(self.master, 'font_size'):
                self.master.font_size = int(self.font_size)
            if hasattr(self.master, '_save_config'):
                self.master._save_config()
        except Exception:
            pass
        # also resize the window proportionally so larger fonts don't overflow
        try:
            width = 640 + max(0, (self.font_size - 12) * 30)
            height = 320 + max(0, (self.font_size - 12) * 20)
            self.geometry(f"{width}x{height}")
        except Exception:
            pass
        try:
            # update minsize to current geometry so later operations don't shrink the window
            w = self.winfo_width()
            h = self.winfo_height()
            if w > 0 and h > 0:
                self.minsize(w, h)
        except Exception:
            pass

    def _set_result_text(self, content):
        """
        Set the result area. content may be:
           - a plain string: show that string
           - a tuple (correct_prefix, incorrect_part): show prefix normal and incorrect_part struck-through
        """
        try:
            if isinstance(content, tuple):
                    correct_prefix, incorrect_part = content
                    # trim trailing/leading spaces to avoid visible gap between labels
                    if correct_prefix:
                        # show the original-cased correct prefix as-is
                        self.result_prefix.config(text=correct_prefix.rstrip() or "")
                    else:
                        self.result_prefix.config(text="")
                    if incorrect_part:
                        self.result_incorrect.config(text=incorrect_part.lstrip())
                    else:
                        self.result_incorrect.config(text="")
            else:
                # plain string: show as full correct prefix
                s = str(content)
                self.result_prefix.config(text=s)
                self.result_incorrect.config(text="")
        except Exception:
            pass

