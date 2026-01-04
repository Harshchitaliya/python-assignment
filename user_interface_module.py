import tkinter as tk
from tkinter import messagebox, ttk
from similarity_module import SimilarityEngine


# Material Design 3 Dark Theme Colors
BG_COLOR = "#1C1B1F"           # Surface
BG_SECONDARY = "#2B2930"       # Surface Container
FG_COLOR = "#E6E1E5"           # On Surface
FG_SECONDARY = "#CAC4D0"       # On Surface Variant
ENTRY_BG = "#2B2930"           # Surface Container High
ENTRY_BORDER = "#938F99"       # Outline
BTN_PRIMARY = "#D0BCFF"        # Primary
BTN_PRIMARY_FG = "#381E72"     # On Primary
BTN_SECONDARY = "#4A4458"      # Secondary Container
BTN_SECONDARY_FG = "#E8DEF8"   # On Secondary Container
TEXT_BG = "#2B2930"            # Surface Container
TEXT_FG = "#E6E1E5"            # On Surface
ACCENT = "#D0BCFF"             # Primary
ERROR_COLOR = "#F2B8B5"        # Error


class MusicApp:

    def __init__(self, artist_music):

        self.artist_music = artist_music
        self.engine = SimilarityEngine(artist_music)

        self.window = tk.Tk()
        self.window.title("Music Recommendation System")
        self.window.geometry("700x750")
        self.window.configure(bg=BG_COLOR)
        
        # Configure ttk style for Material Design
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure progress bar style
        style.configure("Material.Horizontal.TProgressbar",
                       troughcolor=BG_SECONDARY,
                       bordercolor=BG_COLOR,
                       background=ACCENT,
                       lightcolor=ACCENT,
                       darkcolor=ACCENT,
                       thickness=8)
        
        # Main container with padding
        main_frame = tk.Frame(self.window, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎵 Music Recommendation System",
            bg=BG_COLOR,
            fg=ACCENT,
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(0, 24))
        
        # Method selection card
        method_card = tk.Frame(main_frame, bg=BG_SECONDARY)
        method_card.pack(fill=tk.X, pady=(0, 16))
        
        method_inner = tk.Frame(method_card, bg=BG_SECONDARY)
        method_inner.pack(padx=16, pady=12)
        
        tk.Label(
            method_inner,
            text="Similarity Method",
            bg=BG_SECONDARY,
            fg=FG_COLOR,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))
        
        self.method_entry = tk.Entry(
            method_inner,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            insertbackground=ACCENT,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            width=40,
            highlightthickness=2,
            highlightbackground=ENTRY_BORDER,
            highlightcolor=ACCENT
        )
        self.method_entry.pack(fill=tk.X, ipady=8)
        self.method_entry.insert(0, "euclidean")
        
        tk.Label(
            method_inner,
            text="Options: euclidean, cosine, pearson",
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(4, 0))
        
        # Mode selection card
        mode_card = tk.Frame(main_frame, bg=BG_SECONDARY)
        mode_card.pack(fill=tk.X, pady=(0, 16))
        
        mode_inner = tk.Frame(mode_card, bg=BG_SECONDARY)
        mode_inner.pack(padx=16, pady=12)
        
        tk.Label(
            mode_inner,
            text="Comparison Mode",
            bg=BG_SECONDARY,
            fg=FG_COLOR,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))
        
        self.mode = tk.StringVar()
        self.mode.set("track")
        
        radio_frame = tk.Frame(mode_inner, bg=BG_SECONDARY)
        radio_frame.pack(fill=tk.X)
        
        for text, value in [("Track IDs", "track"), ("Artists", "artist"), ("Track Names", "name")]:
            tk.Radiobutton(
                radio_frame,
                text=text,
                variable=self.mode,
                value=value,
                bg=BG_SECONDARY,
                fg=FG_COLOR,
                selectcolor=BG_SECONDARY,
                activebackground=BG_SECONDARY,
                activeforeground=ACCENT,
                font=("Segoe UI", 10),
                highlightthickness=0,
                bd=0
            ).pack(anchor="w", pady=2)
        
        # Input fields card
        input_card = tk.Frame(main_frame, bg=BG_SECONDARY)
        input_card.pack(fill=tk.X, pady=(0, 16))
        
        input_inner = tk.Frame(input_card, bg=BG_SECONDARY)
        input_inner.pack(padx=16, pady=12)
        
        # First input
        tk.Label(
            input_inner,
            text="First Input",
            bg=BG_SECONDARY,
            fg=FG_COLOR,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 4))
        
        self.input1 = tk.Entry(
            input_inner,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            insertbackground=ACCENT,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            highlightthickness=2,
            highlightbackground=ENTRY_BORDER,
            highlightcolor=ACCENT
        )
        self.input1.pack(fill=tk.X, ipady=8, pady=(0, 12))
        
        # Second input
        tk.Label(
            input_inner,
            text="Second Input",
            bg=BG_SECONDARY,
            fg=FG_COLOR,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 4))
        
        self.input2 = tk.Entry(
            input_inner,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            insertbackground=ACCENT,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            highlightthickness=2,
            highlightbackground=ENTRY_BORDER,
            highlightcolor=ACCENT
        )
        self.input2.pack(fill=tk.X, ipady=8)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.pack(pady=(0, 16))
        
        compare_btn = tk.Button(
            button_frame,
            text="Compare",
            command=self.compare,
            bg=BTN_PRIMARY,
            fg=BTN_PRIMARY_FG,
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            padx=32,
            pady=10,
            cursor="hand2",
            activebackground=ACCENT,
            activeforeground=BTN_PRIMARY_FG
        )
        compare_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        quit_btn = tk.Button(
            button_frame,
            text="Quit",
            command=self.window.quit,
            bg=BTN_SECONDARY,
            fg=BTN_SECONDARY_FG,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            padx=32,
            pady=10,
            cursor="hand2",
            activebackground=BG_SECONDARY,
            activeforeground=BTN_SECONDARY_FG
        )
        quit_btn.pack(side=tk.LEFT)
        
        # Output text area
        output_frame = tk.Frame(main_frame, bg=BG_SECONDARY)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        output_inner = tk.Frame(output_frame, bg=BG_SECONDARY)
        output_inner.pack(padx=16, pady=12, fill=tk.BOTH, expand=True)
        
        tk.Label(
            output_inner,
            text="Results",
            bg=BG_SECONDARY,
            fg=FG_COLOR,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))
        
        self.output = tk.Text(
            output_inner,
            height=15,
            bg=TEXT_BG,
            fg=TEXT_FG,
            relief=tk.FLAT,
            font=("Consolas", 10),
            padx=12,
            pady=12,
            wrap=tk.WORD,
            highlightthickness=2,
            highlightbackground=ENTRY_BORDER,
            highlightcolor=ACCENT
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=450,
            mode="determinate",
            style="Material.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X, pady=(0, 4))

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

    def compare(self):
        method = self.method_entry.get().lower()
        first = self.input1.get()
        second = self.input2.get()

        self.output.delete("1.0", tk.END)
        self.progress["value"] = 0

        try:
            if self.mode.get() == "track":
                score = self.engine.track_similarity(first, second, method)
                self.output.insert(tk.END, "Track similarity score:\n")
                self.output.insert(tk.END, str(score) + "\n\n")

                self.output.insert(tk.END, "Finding top 5 similar tracks...\n")

                track_ids = self.get_all_track_ids()
                self.progress["maximum"] = len(track_ids)

                results = []

                for i, track_id in enumerate(track_ids):
                    if track_id != first:
                        value = self.engine.track_similarity(first, track_id, method)
                        results.append((track_id, value))

                    self.progress["value"] = i + 1
                    self.window.update_idletasks()

                results.sort(key=lambda x: x[1], reverse=True)

                self.output.insert(tk.END, "\nTop 5 similar tracks:\n")
                for t, v in results[:5]:
                    self.output.insert(tk.END, t + " -> " + str(v) + "\n")

            elif self.mode.get() == "artist":
                score = self.engine.artist_similarity(first, second, method)
                self.output.insert(tk.END, "Artist similarity score:\n")
                self.output.insert(tk.END, str(score) + "\n\n")

                self.output.insert(
                    tk.END,
                    "Top 5 similar artists to " + first + ":\n"
                )

                top = self.engine.top_5_similar_artists(first, method)

                for artist, value in top:
                    self.output.insert(tk.END, artist + " -> " + str(value) + "\n")

            else:
                id1 = self.find_track_id_by_name(first)
                id2 = self.find_track_id_by_name(second)

                if id1 is None or id2 is None:
                    raise ValueError("Track name not found")

                score = self.engine.track_similarity(id1, id2, method)
                self.output.insert(tk.END, "Track name similarity score:\n")
                self.output.insert(tk.END, str(score) + "\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()
