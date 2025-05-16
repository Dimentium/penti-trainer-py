import pyxel
from penti_trainer import PentiTrainer


SYMBOL_KEYS: list[int, dict[int, tuple[str, str]]] = [
    {
        # Standard English layout
        pyxel.KEY_BACKQUOTE: ("`", "~"),
        pyxel.KEY_1: ("1", "!"),
        pyxel.KEY_2: ("2", "@"),
        pyxel.KEY_3: ("3", "#"),
        pyxel.KEY_4: ("4", "$"),
        pyxel.KEY_5: ("5", "%"),
        pyxel.KEY_6: ("6", "^"),
        pyxel.KEY_7: ("7", "&"),
        pyxel.KEY_8: ("8", "*"),
        pyxel.KEY_9: ("9", "("),
        pyxel.KEY_0: ("0", ")"),
        pyxel.KEY_MINUS: ("-", "_"),
        pyxel.KEY_EQUALS: ("=", "+"),
        pyxel.KEY_LEFTBRACKET: ("[", "{"),
        pyxel.KEY_RIGHTBRACKET: ("]", "}"),
        pyxel.KEY_BACKSLASH: ("\\", "|"),
        pyxel.KEY_SEMICOLON: (";", ":"),
        pyxel.KEY_QUOTE: ("'", '"'),
        pyxel.KEY_COMMA: (",", "<"),
        pyxel.KEY_PERIOD: (".", ">"),
        pyxel.KEY_SLASH: ("/", "?"),
    },
]


class App:
    def __init__(self):
        self.keys: dict[int, str] = {value: key for key, value in vars(pyxel).items() if key.startswith("KEY_")}
        self.t = PentiTrainer()
        pyxel.init(200, 120, title="Penti Typing Practice", fps=30)
        self.x = 0
        pyxel.FONT_WIDTH = 300
        pyxel.run(self.update, self.draw)

    def read_key(self) -> str:
        self.shift_mode = pyxel.btn(pyxel.KEY_SHIFT)

        for key in range(97, 123):  # 'a' ~ 'z'
            if pyxel.btnp(key):
                return chr(key).upper() if self.shift_mode else chr(key)

        for key, (normal_char, shift_char) in SYMBOL_KEYS[0].items():
            if pyxel.btnp(key):
                return shift_char if self.shift_mode else normal_char

        if pyxel.btnp(pyxel.KEY_SPACE):
            return " "

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            return ""

        if pyxel.btnp(pyxel.KEY_RETURN):
            return "RETURN"

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            return "ESCAPE"

        return None

    def update(self):
        self.x = (self.x + 1) % pyxel.width

        key = self.read_key()
        match key:
            case None:
                return
            case "ESCAPE":
                self.t = PentiTrainer()
            case "RETURN":
                if self.t.completed:
                    self.t = PentiTrainer()
            case _:
                self.t.update(key)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)

        pyxel.text(10, 10, self.t.state.sentence_done, pyxel.COLOR_GRAY)
        pyxel.text(self.t.position * 4 + 10, 10, self.t.state.sentence_here, pyxel.COLOR_WHITE)
        pyxel.text(self.t.position * 4 + 14, 10, self.t.state.sentence_last, pyxel.COLOR_GRAY)

        pyxel.text(10, 20, self.t.input, 3)
        pyxel.text(self.t.position * 4 + 10, 20, self.t.last_char, pyxel.COLOR_RED)

        pyxel.text(10, 50, self.t.state.hint, pyxel.COLOR_YELLOW)

        if self.t.completed:
            pyxel.text(10, 70, self.t.results, pyxel.COLOR_LIME)


App()
