import tkinter as tk
from tkinter import messagebox, ttk
from similarity_module import SimilarityEngine


BG_COLOR = "#1C1B1F"
BG_SECONDARY = "#2B2930"
FG_COLOR = "#E6E1E5"
FG_SECONDARY = "#CAC4D0"
ENTRY_BG = "#2B2930"
ENTRY_BORDER = "#938F99"
BTN_PRIMARY = "#D0BCFF"
BTN_PRIMARY_FG = "#381E72"
BTN_SECONDARY = "#4A4458"
BTN_SECONDARY_FG = "#E8DEF8"
TEXT_BG = "#2B2930"
TEXT_FG = "#E6E1E5"
ACCENT = "#D0BCFF"


class MusicApp:

    def __init__(self, artist_music):
        self.artist_music = artist_music
        self.engine = SimilarityEngine(artist_music)

        self.window = tk.Tk()
        self.window.title("Music Recommendation System")
        self.window.geometry("720x780")
        self.window.configure(bg=BG_COLOR)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Material.Horizontal.TProgressbar",
            troughcolor=BG_SECONDARY,
            background=ACCENT,
            thickness=8
        )

        main = tk.Frame(self.window, bg=BG_COLOR)
        main.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

        tk.Label(
            main,
            text="🎵 Music Recommendation System",
            bg=BG_COLOR,
            fg=ACCENT,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 20))

        self.method_entry = self._entry_block(
            main,
            "Similarity method (euclidean / cosine / pearson)",
            "euclidean"
        )

        self.input1 = self._entry_block(main, "First input")
        self.input2 = self._entry_block(main, "Second input")

        btn_frame = tk.Frame(main, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        self._button(btn_frame, "Compare Track IDs", self.compare_tracks, BTN_PRIMARY, BTN_PRIMARY_FG)
        self._button(btn_frame, "Compare Artists", self.compare_artists, BTN_SECONDARY, BTN_SECONDARY_FG)
        self._button(btn_frame, "Compare Track Names", self.compare_track_names, BTN_SECONDARY, BTN_SECONDARY_FG)
        self._button(
            btn_frame,
            "Top 5 Recommendations",
            self.get_recommendations,
            BTN_PRIMARY,
            BTN_PRIMARY_FG
        )
        self._button(btn_frame, "Quit", self.window.quit, BG_SECONDARY, FG_COLOR)

        self.output = tk.Text(
            main,
            height=16,
            bg=TEXT_BG,
            fg=TEXT_FG,
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=12,
            pady=12,
            wrap=tk.WORD,
            highlightthickness=2,
            highlightbackground=ENTRY_BORDER,
            highlightcolor=ACCENT
        )
        self.output.pack(fill=tk.BOTH, expand=True, pady=(10, 6))

        self.progress = ttk.Progressbar(
            main,
            orient="horizontal",
            mode="determinate",
            style="Material.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X)

    def _entry_block(self, parent, label, default=None):
        frame = tk.Frame(parent, bg=BG_SECONDARY)
        frame.pack(fill=tk.X, pady=(0, 14))

        inner = tk.Frame(frame, bg=BG_SECONDARY)
        inner.pack(padx=16, pady=12, fill=tk.X)

        tk.Label(
            inner,
            text=label,
            bg=BG_SECONDARY,
            fg=FG_COLOR,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 4))

        entry = tk.Entry(
            inner,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            insertbackground=ACCENT,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            highlightthickness=2,
            highlightbackground=ENTRY_BORDER,
            highlightcolor=ACCENT
        )
        entry.pack(fill=tk.X, ipady=8)

        if default:
            entry.insert(0, default)

        return entry

    def _button(self, parent, text, cmd, bg, fg):
        tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=10,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=6)

    def find_track_id_by_name(self, name):
        for artist in self.artist_music:
            for track_id, track in self.artist_music[artist].items():
                if track["name"].lower() == name.lower():
                    return track_id
        return None

    def get_all_track_ids(self):
        ids = []
        for artist in self.artist_music:
            for track_id in self.artist_music[artist]:
                ids.append(track_id)
        return ids
    
    def get_recommendations(self):
        self._reset()
        try:
            method = self.method_entry.get().lower()
            value = self.input1.get()

            if not value:
                raise ValueError("Please enter a track ID or artist name")

            if value in self.artist_music:
                self.output.insert(tk.END, "Top 5 similar artists:\n")
                results = self.engine.recommend_artists(value, method)

                for artist, score in results:
                    self.output.insert(tk.END, artist + " -> " + str(score) + "\n")

            else:
                self.output.insert(tk.END, "Top 5 similar tracks:\n")
                results = self.engine.recommend_tracks(value, method)

                for track, score in results:
                    self.output.insert(tk.END, track + " -> " + str(score) + "\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def compare_tracks(self):
        self._reset()
        try:
            method = self.method_entry.get().lower()
            track_id = self.input1.get()
            track_id_2 = self.input2.get()

            score = self.engine.track_similarity(track_id, track_id_2, method)
            self.output.insert(tk.END, "Track similarity score:\n")
            self.output.insert(tk.END, str(score) + "\n\n")

            self.output.insert(tk.END, "Top 5 similar tracks:\n")
            results = self.engine.top_5_similar_tracks(track_id, method)

            for t, v in results:
                self.output.insert(tk.END, t + " -> " + str(v) + "\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def compare_artists(self):
        self._reset()
        try:
            method = self.method_entry.get().lower()
            a1 = self.input1.get()
            a2 = self.input2.get()

            score = self.engine.artist_similarity(a1, a2, method)
            self.output.insert(tk.END, f"Artist similarity score:\n{score}\n\n")

            self.output.insert(tk.END, f"Top 5 similar artists to {a1}:\n")
            for artist, val in self.engine.top_5_similar_artists(a1, method):
                self.output.insert(tk.END, f"{artist} -> {val}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def compare_track_names(self):
        self._reset()
        try:
            method = self.method_entry.get().lower()
            n1 = self.input1.get()
            n2 = self.input2.get()

            id1 = self.find_track_id_by_name(n1)
            id2 = self.find_track_id_by_name(n2)

            if not id1 or not id2:
                raise ValueError("Track name not found")

            score = self.engine.track_similarity(id1, id2, method)
            self.output.insert(tk.END, f"Track name similarity score:\n{score}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _reset(self):
        self.output.delete("1.0", tk.END)
        self.progress["value"] = 0

    def run(self):
        self.window.mainloop()
