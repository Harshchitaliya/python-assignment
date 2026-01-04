import tkinter as tk
from tkinter import messagebox, ttk
from similarity_module import SimilarityEngine


BG_COLOR = "#1C1B1F"
FG_COLOR = "#E6E1E5"
ACCENT = "#D0BCFF"
ENTRY_BG = "#2B2930"


class MusicApp:

    def __init__(self, artist_music):
        self.artist_music = artist_music
        self.engine = SimilarityEngine(artist_music)

        self.window = tk.Tk()
        self.window.title("Music Similarity & Recommendation System")
        self.window.geometry("560x620")
        self.window.configure(bg=BG_COLOR)

        style = ttk.Style()
        style.theme_use("clam")

        tk.Label(
            self.window,
            text="Music Similarity & Recommendation",
            bg=BG_COLOR,
            fg=ACCENT,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=14)

        # -------- TASK MODE --------
        self.task_mode = tk.StringVar(value="similarity")

        mode_frame = tk.Frame(self.window, bg=BG_COLOR)
        mode_frame.pack()

        tk.Radiobutton(
            mode_frame,
            text="Similarity",
            variable=self.task_mode,
            value="similarity",
            bg=BG_COLOR,
            fg=FG_COLOR,
            selectcolor=BG_COLOR,
            command=self.update_ui
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            mode_frame,
            text="Top 5 Recommendation",
            variable=self.task_mode,
            value="recommendation",
            bg=BG_COLOR,
            fg=FG_COLOR,
            selectcolor=BG_COLOR,
            command=self.update_ui
        ).pack(side=tk.LEFT, padx=10)

        # -------- METHOD --------
        tk.Label(self.window, text="Similarity method", bg=BG_COLOR, fg=FG_COLOR).pack(pady=(10, 2))

        self.method_box = ttk.Combobox(
            self.window,
            values=["euclidean", "cosine", "pearson"],
            state="readonly"
        )
        self.method_box.pack()
        self.method_box.set("euclidean")

        # -------- ITEM TYPE --------
        self.item_type = tk.StringVar(value="artist")

        tk.Radiobutton(
            self.window,
            text="Artists",
            variable=self.item_type,
            value="artist",
            bg=BG_COLOR,
            fg=FG_COLOR,
            selectcolor=BG_COLOR,
            command=self.update_dropdowns
        ).pack(pady=4)

        tk.Radiobutton(
            self.window,
            text="Tracks",
            variable=self.item_type,
            value="track",
            bg=BG_COLOR,
            fg=FG_COLOR,
            selectcolor=BG_COLOR,
            command=self.update_dropdowns
        ).pack()

        # -------- DROPDOWNS --------
        tk.Label(self.window, text="First selection", bg=BG_COLOR, fg=FG_COLOR).pack(pady=(10, 2))
        self.combo1 = ttk.Combobox(self.window)
        self.combo1.pack()
        self.combo1.bind("<KeyRelease>", self.filter_combo1)

        self.second_frame = tk.Frame(self.window, bg=BG_COLOR)
        self.second_frame.pack(pady=(10, 2))

        self.second_label = tk.Label(
            self.second_frame,
            text="Second selection",
            bg=BG_COLOR,
            fg=FG_COLOR
        )
        self.second_label.pack()

        self.combo2 = ttk.Combobox(self.second_frame)
        self.combo2.pack()
        self.combo2.bind("<KeyRelease>", self.filter_combo2)


        # -------- BUTTONS --------
        self.button_frame = tk.Frame(self.window, bg=BG_COLOR)
        self.button_frame.pack(pady=14)
        
        tk.Button(
            self.button_frame,
            text="Run",
            command=self.run_task,
            bg=ACCENT,
            fg="#381E72",
            padx=24,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.button_frame,
            text="Quit",
            command=self.window.quit,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

        # -------- OUTPUT --------
        self.output = tk.Text(
            self.window,
            height=10,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            wrap=tk.WORD
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.load_data_lists()
        self.update_dropdowns()
        self.update_ui()

    # ---------------- DATA ----------------
    def load_data_lists(self):
        self.artist_list = sorted(self.artist_music.keys())

        self.track_name_to_id = {}
        self.track_names = []

        for artist in self.artist_music:
            for track_id, track in self.artist_music[artist].items():
                self.track_name_to_id[track["name"]] = track_id
                self.track_names.append(track["name"])

        self.track_names = sorted(list(set(self.track_names)))

    def update_dropdowns(self):
        if self.item_type.get() == "artist":
            self.current_list = self.artist_list
        else:
            self.current_list = self.track_names

        self.combo1["values"] = self.current_list
        self.combo2["values"] = self.current_list

        if self.current_list:
            self.combo1.set("")
            self.combo2.set("")

    def update_ui(self):
        if self.task_mode.get() == "recommendation":
            self.second_frame.pack_forget()
        else:
            self.second_frame.pack(before=self.button_frame, pady=(10, 2))


    # ---------------- FILTERING ----------------
    def filter_combo1(self, event):
        self.filter_combobox(self.combo1)

    def filter_combo2(self, event):
        self.filter_combobox(self.combo2)

    def filter_combobox(self, combo):
        typed = combo.get().lower()
        filtered = [item for item in self.current_list if typed in item.lower()]
        combo["values"] = filtered

    # ---------------- ACTION ----------------
    def run_task(self):
        self.output.delete("1.0", tk.END)

        try:
            method = self.method_box.get()
            v1 = self.combo1.get()

            if not v1:
                raise ValueError("Please select an item")

            if self.task_mode.get() == "similarity":
                v2 = self.combo2.get()
                if not v2:
                    raise ValueError("Please select second item")

                if self.item_type.get() == "artist":
                    score = self.engine.artist_similarity(v1, v2, method)
                    self.output.insert(tk.END, f"Artist similarity score:\n{score}")

                else:
                    id1 = self.track_name_to_id[v1]
                    id2 = self.track_name_to_id[v2]
                    score = self.engine.track_similarity(id1, id2, method)
                    self.output.insert(tk.END, f"Track similarity score:\n{score}")

            else:
                if self.item_type.get() == "artist":
                    self.output.insert(tk.END, "Top 5 similar artists:\n")
                    for a, s in self.engine.recommend_artists(v1, method):
                        self.output.insert(tk.END, f"{a} -> {s}\n")
                else:
                    track_id = self.track_name_to_id[v1]
                    self.output.insert(tk.END, "Top 5 similar tracks:\n")
                    for t, s in self.engine.recommend_tracks(track_id, method):
                        self.output.insert(tk.END, f"{t} -> {s}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()
