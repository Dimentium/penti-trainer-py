import sys
import termios
import tty
import argparse

from trainer import Trainer


class CliApp:
    _LB = "\r\033[K"
    _LE = "\n"

    @staticmethod
    def read_stdout() -> str:
        fd = sys.stdin.fileno()
        normal_state = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, normal_state)

        return ch

    def get_input_char(self) -> str:
        ch = self.read_stdout()

        if ch in ("\x03", "\x1b"):  # Ctrl+C, Esc
            print("\n\rExecution interrupted by user.")
            quit()

        if ch == "\x7f":
            return ""
        if ch.isprintable():
            return ch

        return None

    def red(self, s: str) -> str:
        return f"\033[91m{s}\033[0m"

    def green(self, s: str) -> str:
        return f"\033[92m{s}\033[0m"

    def blue(self, s: str) -> str:
        return f"\033[93m{s}\033[0m"

    def output(self, s: Trainer.State) -> None:
        l1 = self._LB + s.sentence_done + self.blue(s.sentence_here) + s.sentence_last + self._LE
        l2 = self._LB + s.hint + self._LE
        l3 = self._LB + self.green(s.input) + self.red(s.last_char)
        sys.stdout.write("\033[2A")
        print(l1 + l2 + l3, end="", flush=True)

    def run(self, text: str | None = None) -> None:
        if text:
            t = Trainer(text)
        else:
            t = Trainer()

        print("Using sentence:\n\n\n")
        self.output(t.state)

        while True:
            ch = None
            while ch is None:
                ch = self.get_input_char()

            if t.update(ch):
                self.output(t.state)

            if t.completed:
                print("\n" * 2 + t.results)
                return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple keyboard trainer for Penti layout.",
    )

    parser.add_argument("text", nargs="?")

    args = parser.parse_args()

    CliApp().run(args.text)
