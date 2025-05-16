import time

CHORDS: list[tuple[str, str]] = [
    (" ", "# ---- (ALPHA)"),
    ("A", "# --#- (ALPHA)"),
    ("B", "# -##- (ALPHA)"),
    ("C", "- #-#- (ALPHA)"),
    ("D", "# ---# (ALPHA)"),
    ("E", "- -#-- (ALPHA)"),
    ("F", "# #--- (ALPHA)"),
    ("G", "- --## (ALPHA)"),
    ("H", "# #--# (ALPHA)"),
    ("I", "- --#- (ALPHA)"),
    ("J", "- #--# (ALPHA)"),
    ("K", "- #### (ALPHA)"),
    ("L", "- ##-- (ALPHA)"),
    ("M", "- -### (ALPHA)"),
    ("N", "- ---# (ALPHA)"),
    ("O", "- -##- (ALPHA)"),
    ("P", "# ###- (ALPHA)"),
    ("Q", "# #-#- (ALPHA)"),
    ("R", "# -#-- (ALPHA)"),
    ("S", "- #--- (ALPHA)"),
    ("T", "# -### (ALPHA)"),
    ("U", "- ###- (ALPHA)"),
    ("V", "- #-## (ALPHA)"),
    ("W", "# #### (ALPHA)"),
    ("X", "# #-## (ALPHA)"),
    ("Y", "# --## (ALPHA)"),
    ("Z", "# ##-- (ALPHA)"),
    ('"', "# ##-- (PUNCT)"),
    (",", "- #-#- (DIGIT)"),
    (".", "# ---# (DIGIT)"),
    ("⌫", "- _#-- (=SL2=)"),
]


class PentiTrainer:
    __DEFAULT_SENTENCE: str = '"The quick brown fox jumps over the lazy dog."'

    class State:
        sentence_done: str
        sentence_here: str
        sentence_last: str
        hint: str
        input: str
        last_char: str

    def __init__(self, text: str = __DEFAULT_SENTENCE):
        self.sentence: str = text
        self.chords: dict[str, str] = self.load_chords()
        self.input: str = ""
        self.last_char: str = ""
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.state = self.State()
        self.update("")

    @property
    def position(self) -> int:
        return min(len(self.input), len(self.sentence) - 1)

    @property
    def next_char(self) -> str:
        return "" if self.completed else self.sentence[self.position] if self.last_char == "" else "⌫"

    @property
    def current_char(self) -> str:
        return "" if self.completed else self.sentence[self.position]

    @property
    def next_chord(self) -> str:
        return self.get_chord(self.next_char)

    @property
    def completed(self) -> bool:
        return self.input == self.sentence

    @staticmethod
    def load_chords() -> dict[str, str]:
        chords = {}
        for char, chord in CHORDS:
            chords[char.upper()] = chord.strip()
        return chords

    def get_chord(self, c: str) -> str:
        return self.chords.get(c.upper(), "? ???? (?????)")

    def update(self, ch) -> bool:
        if self.completed:
            return False

        if (ch == self.current_char) and self.last_char == "":
            self.input += ch
            if self.start_time == 0:
                self.start_time = time.time()

        elif ch == "" or ch == "\x7f":
            self.last_char = ""

        elif self.last_char == "" and ch.isprintable():
            self.last_char = ch

        else:
            return False

        self.state.sentence_done = self.sentence[0 : self.position]
        self.state.sentence_here = self.current_char
        self.state.sentence_last = self.sentence[self.position + 1 :]
        self.state.hint = f" `{self.next_char}` -> `{self.next_chord}`" if not self.completed else ""
        self.state.input = self.input
        self.state.last_char = self.last_char

        if self.completed and self.end_time == 0:
            self.end_time = time.time()

        return True

    @property
    def results(self) -> str:
        time_spent = self.end_time - self.start_time
        time_spent_minutes = time_spent / 60
        wpm = len(self.sentence) / 5 / time_spent_minutes

        result = f"WPM: {wpm:.2f} ({time_spent:.2f} seconds spent)"

        return result


if __name__ == "__main__":
    t = PentiTrainer()
    print(t.state.__dict__)
