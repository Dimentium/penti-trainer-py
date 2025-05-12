import sys
import termios
import tty
import time


def load_chords(file_path):
    chords = {}
    with open(file_path, "r") as file:
        for line in file:
            char, chord = line.split(":")
            chords[char] = chord.strip()
    return chords


def get_input_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    except KeyboardInterrupt:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        raise
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def main():
    start_time = time.time()

    default_sentence = '"The quick brown fox jumps over the lazy dog."'
    sentence = sys.argv[1] if len(sys.argv) > 1 else default_sentence
    print(f"Using sentence:      {sentence}\n")

    chords = load_chords("chords.txt")

    input_line = ""

    for char in sentence:
        chord = chords.get(char.upper(), "? ???? (?????)")
        print(f"\r {char} : {chord} : {input_line}", end="", flush=True)

        correct = False
        current_char = ""
        need_correction = False
        while True:
            input_char = get_input_char()

            if input_char in ("\x03", "\x1b"):  # Ctrl+C, Esc
                print("\nExecution interrupted by user.")
                quit()

            if (input_char == char) and (not need_correction):
                current_char = f"\033[92m{input_char}\033[0m"  # Green for correct
                correct = True
            else:
                need_correction = True
                if input_char == "\x7f":
                    current_char = ""
                    need_correction = False
                elif not input_char.isprintable():  # Ignore non-printable characters
                    continue
                elif bool(current_char) ^ (need_correction):
                    current_char = f"\033[91m{input_char}\033[0m"  # Red for incorrect
                    print(
                        f"\r ⌫ : {chords.get('⌫', '? ???? (?????)')} : {input_line}{current_char}", end="", flush=True
                    )
                    continue
                elif current_char and need_correction:
                    print(
                        f"\r ⌫ : {chords.get('⌫', '? ???? (?????)')} : {input_line}{current_char}", end="", flush=True
                    )
                    continue

            print(f"\r {char} : {chord} : {input_line}{current_char}", end="", flush=True)

            if correct:
                break

        input_line += current_char

    end_time = time.time()
    time_spent = end_time - start_time
    time_spent_minutes = time_spent / 60
    wpm = len(sentence) / 5 / time_spent_minutes

    print(f"\n\nTime spent: {time_spent:.2f} seconds")
    print(f"Words per minute (WPM): {wpm:.2f}")


if __name__ == "__main__":
    main()
