import time


class Trainer:
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
        self.state = self.State()
        self.update("")

    @property
    def position(self) -> int:
        return min(len(self.input), len(self.sentence) - 1)

    @property
    def current_char(self) -> str:
        return self.sentence[self.position]

    @property
    def completed(self) -> bool:
        return self.input == self.sentence

    @staticmethod
    def load_chords() -> dict[str, str]:
        chords = {}
        with open("chords.txt", "r") as file:
            for line in file:
                char, chord = line.split(":")
                chords[char.upper()] = chord.strip()
        return chords

    def get_chord(self, c: str) -> str:
        return self.chords.get(c.upper(), "? ???? (?????)")

    def update(self, ch) -> bool:
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
        self.state.sentence_last = self.sentence[self.position + 1 : -1]
        next_char = "⌫" if self.last_char != "" else self.current_char
        self.state.hint = f" `{next_char}` -> `{self.get_chord(next_char)}`"
        self.state.input = self.input
        self.state.last_char = self.last_char

        return True

    @property
    def results(self) -> str:
        end_time = time.time()
        time_spent = end_time - self.start_time
        time_spent_minutes = time_spent / 60
        wpm = len(self.sentence) / 5 / time_spent_minutes

        result = f"Words per minute (WPM): {wpm:.2f} ({time_spent:.2f} seconds spent)"

        return result


if __name__ == "__main__":
    t = Trainer()
    print(t.state.__dict__)
