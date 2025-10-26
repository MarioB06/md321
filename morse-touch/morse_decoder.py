"""Utilities zum Umwandeln zwischen Text und Morsecode."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class MorseCodeAlphabet:
    """Hält die Zuordnung zwischen Buchstaben und Morsecode."""

    forward: Dict[str, str]

    @classmethod
    def international(cls) -> "MorseCodeAlphabet":
        """Liefert das internationale Morsealphabet."""

        mapping = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
        }
        return cls(forward=mapping)

    @property
    def reverse(self) -> Dict[str, str]:
        """Baut das Reverse-Lexikon (Morse -> Buchstabe) dynamisch auf."""

        return {value: key for key, value in self.forward.items()}


class MorseDecoder:
    """Kann Morsecode in Text und zurück wandeln."""

    def __init__(self, alphabet: MorseCodeAlphabet | None = None) -> None:
        self._alphabet = alphabet or MorseCodeAlphabet.international()

    def decode_symbol(self, code: str) -> str:
        """Dekodiert ein einzelnes Symbol. Unbekanntes wird als '?' markiert."""

        return self._alphabet.reverse.get(code, "?")

    def encode_symbol(self, char: str) -> str:
        """Kodiert ein einzelnes Zeichen. Kleinbuchstaben werden groß geschrieben."""

        return self._alphabet.forward.get(char.upper(), "")

    def decode_message(self, codes: str) -> str:
        """Dekodiert einen kompletten Morse-String (Buchstaben durch Leerzeichen getrennt)."""

        letters = [self.decode_symbol(code) for code in codes.split(" ") if code]
        return "".join(letters)

    def encode_message(self, message: str) -> str:
        """Kodiert einen kompletten Text in Morse (Buchstaben durch Leerzeichen getrennt)."""

        symbols = [self.encode_symbol(char) for char in message if char.strip()]
        return " ".join(filter(None, symbols))
