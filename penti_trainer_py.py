import sys
import termios
import tty
import time


class Trainer:
    DEFAULT_SENTENCE: str = '"The quick brown fox jumps over the lazy dog."'

    def __init__(self, sentence: str):
        self.sentence: str = sentence
        self.chords: dict[str, str] = self.load_chords()
        self.input: str = ""
        self.last_char: str = ""
        self.start_time: float = 0.0

    @property
    def position(self) -> int:
        return min(len(self.input), len(self.sentence) - 1)

    @property
    def current_char(self) -> str:
        return self.sentence[self.position]

    @staticmethod
    def load_chords() -> dict[str, str]:
        chords = {}
        with open("chords.txt", "r") as file:
            for line in file:
                char, chord = line.split(":")
                chords[char.upper()] = chord.strip()
        return chords

    def get_input_char(self) -> str:
        fd = sys.stdin.fileno()
        normal_state = termios.tcgetattr(fd)
        while True:
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, normal_state)

            if ch in ("\x03", "\x1b"):  # Ctrl+C, Esc
                print("\n\rExecution interrupted by user.")
                quit()

            if ch == "\x7f":
                return ""
            if ch.isprintable():
                return ch

    @staticmethod
    def red(s: str) -> str:
        return f"\033[91m{s}\033[0m"

    @staticmethod
    def green(s: str) -> str:
        return f"\033[92m{s}\033[0m"

    @staticmethod
    def blue(s: str) -> str:
        return f"\033[93m{s}\033[0m"

    def get_chord(self, c: str) -> str:
        return self.chords.get(c.upper(), "? ???? (?????)")

    def output(self) -> None:
        if self.start_time:
            sys.stdout.write("\033[2A")
        else:
            print("Using sentence:\n")

        line_1 = f"\r\033[K{self.sentence[0 : self.position]}{self.blue(self.current_char)}{self.sentence[self.position + 1 : -1]} \n"
        line_3 = "\r\033[K"

        line_3 += self.green(self.input)

        if self.last_char != "":
            line_3 += self.red(self.last_char)
            next_char = "⌫"
        else:
            next_char = self.current_char

        line_2 = f"\r\033[K `{next_char}` -> `{self.get_chord(next_char)}`\n"

        print(line_1 + line_2 + line_3, end="", flush=True)

    def run(self) -> None:
        for char in self.sentence:
            self.last_char = ""

            while True:
                self.output()

                char = self.get_input_char()
                if self.start_time == 0:
                    self.start_time = time.time()

                if (char == self.current_char) and self.last_char == "":
                    self.input += char
                    break

                if char == "":
                    self.last_char = ""

                elif self.last_char == "":
                    self.last_char = char

        self.results()

    def results(self) -> None:
        self.output()
        end_time = time.time()
        time_spent = end_time - self.start_time
        time_spent_minutes = time_spent / 60
        wpm = len(self.sentence) / 5 / time_spent_minutes

        print(f"\n\nTime spent: {time_spent:.2f} seconds")
        print(f"Words per minute (WPM): {wpm:.2f}")


if __name__ == "__main__":
    sentence = sys.argv[1] if len(sys.argv) > 1 else Trainer.DEFAULT_SENTENCE

    trainer = Trainer(sentence)
    trainer.run()
