"""Liest Tastendrücke ein und interpretiert sie als Morsecode."""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Sequence, Tuple

try:
    from RPi import GPIO  # type: ignore
except ImportError:  # pragma: no cover - auf Nicht-RPi-Systemen erwartet
    GPIO = None

from morse_decoder import MorseDecoder

BUTTON_PIN = 11  # BOARD-Nummerierung (physikalischer Pin 11 = BCM 17)


@dataclass
class MorseTimingConfig:
    """Enthält die Zeit-Schwellen zur Interpretation des Morsesignals."""

    dot_max: float = 0.3
    letter_gap: float = 0.7
    word_gap: float = 1.5
    poll_interval: float = 0.01

    def symbol_for(self, duration: float) -> str:
        """Ermittelt, ob ein Tastendruck ein Punkt oder Strich war."""

        return "." if duration <= self.dot_max else "-"


@dataclass
class MorseState:
    """Puffer für aktuell eingehende Morse-Symbole."""

    current_symbol: List[str] = field(default_factory=list)
    current_word: List[str] = field(default_factory=list)
    last_release: float | None = None
    pressed_since: float | None = None


class TouchMorseInterpreter:
    """Konvertiert Tastendrücke in Text."""

    def __init__(
        self,
        decoder: MorseDecoder,
        config: MorseTimingConfig,
        on_letter: Callable[[str], None] | None = None,
        on_word: Callable[[str], None] | None = None,
    ) -> None:
        self.decoder = decoder
        self.config = config
        self.on_letter = on_letter
        self.on_word = on_word
        self.state = MorseState()

    def handle_press(self, timestamp: float) -> None:
        self.state.pressed_since = timestamp

    def handle_release(self, timestamp: float) -> None:
        if self.state.pressed_since is None:
            return
        duration = timestamp - self.state.pressed_since
        symbol = self.config.symbol_for(duration)
        self.state.current_symbol.append(symbol)
        self.state.pressed_since = None
        self.state.last_release = timestamp

    def update_idle(self, timestamp: float) -> None:
        if self.state.pressed_since is not None or self.state.last_release is None:
            return

        gap = timestamp - self.state.last_release
        if gap >= self.config.word_gap:
            self._flush_letter()
            self._flush_word()
        elif gap >= self.config.letter_gap:
            self._flush_letter()

    def _flush_letter(self) -> None:
        if not self.state.current_symbol:
            return
        code = "".join(self.state.current_symbol)
        letter = self.decoder.decode_symbol(code)
        self.state.current_word.append(letter)
        self.state.current_symbol.clear()
        if self.on_letter:
            self.on_letter(letter)

    def _flush_word(self) -> None:
        if not self.state.current_word:
            return
        word = "".join(self.state.current_word)
        if self.on_word:
            self.on_word(word)
        else:
            print(word)
        self.state.current_word.clear()

    # Simulation ---------------------------------------------------------
    def simulate(self, sequence: Sequence[Tuple[float, float]]) -> None:
        """Spielt eine Sequenz aus (press_duration, gap_duration) ab."""

        now = time.monotonic()
        for press_duration, gap in sequence:
            press_start = now
            self.handle_press(press_start)
            release_time = press_start + press_duration
            self.handle_release(release_time)
            now = release_time + gap
            self.update_idle(now)
        # Abschluss
        self.update_idle(now + self.config.word_gap)


def run_gpio_loop(interpreter: TouchMorseInterpreter) -> None:
    if GPIO is None:
        raise RuntimeError("RPi.GPIO ist nicht verfügbar. Verwende stattdessen --simulate.")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Morse-Touch läuft. Drücke STRG+C zum Beenden.")
    try:
        while True:
            now = time.monotonic()
            value = GPIO.input(BUTTON_PIN)
            if value == 0 and interpreter.state.pressed_since is None:
                interpreter.handle_press(now)
            elif value == 1 and interpreter.state.pressed_since is not None:
                interpreter.handle_release(now)
            interpreter.update_idle(now)
            time.sleep(interpreter.config.poll_interval)
    except KeyboardInterrupt:
        print("\nBeendet.")
    finally:
        GPIO.cleanup()


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dot-max", type=float, default=0.3, help="Maximale Dauer eines Punktes (s)")
    parser.add_argument(
        "--letter-gap", type=float, default=0.7, help="Pause (s) bis ein Buchstabe abgeschlossen wird"
    )
    parser.add_argument("--word-gap", type=float, default=1.5, help="Pause (s) bis ein Wort abgeschlossen wird")
    parser.add_argument("--poll", type=float, default=0.01, help="Polling-Intervall in Sekunden")
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Startet eine Beispiel-Simulation für das Morse-Interface",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    config = MorseTimingConfig(
        dot_max=args.dot_max,
        letter_gap=args.letter_gap,
        word_gap=args.word_gap,
        poll_interval=args.poll,
    )
    decoder = MorseDecoder()
    interpreter = TouchMorseInterpreter(decoder, config)

    if args.simulate:
        # SOS (... --- ...)
        sample_sequence = [
            (0.1, 0.2),
            (0.1, 0.2),
            (0.1, 0.9),
            (0.6, 0.2),
            (0.6, 0.2),
            (0.6, 0.9),
            (0.1, 0.2),
            (0.1, 0.2),
            (0.1, 2.0),
        ]
        interpreter.on_word = lambda word: print(f"Simuliert: {word}")
        interpreter.simulate(sample_sequence)
        return 0

    run_gpio_loop(interpreter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
