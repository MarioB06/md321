# Morse Touch

Dieses Unterprojekt zeigt, wie sich ein einfacher Taster (z. B. Touch- oder Drucksensor)
als Morsecode-Eingabegerät verwenden lässt. Das Skript wertet die Länge eines Tastendrucks
aus, erkennt daraus Punkte und Striche und setzt sie anschließend wieder zu Buchstaben
und Wörtern zusammen.

## Verwendung

```bash
python touch_morse.py --simulate
```

Im Simulationsmodus werden zuvor definierte Tastendrücke abgespielt, sodass sich die Logik
auch ohne echte Hardware demonstrieren lässt. Für den Betrieb auf einem Raspberry Pi kann
das Skript ohne den Parameter gestartet werden. Der Taster muss dabei mit dem physikalischen
Pin 11 (BCM 17) verbunden sein.

## Funktionsweise

- Jeder Tastendruck wird gemessen.
- Kurze Drücke (< 300 ms) zählen als Punkt, längere Drücke als Strich.
- Die Pausen zwischen den Drücken entscheiden darüber, ob ein Buchstabe oder ein Wort
  abgeschlossen wurde.

Die Schwellenwerte lassen sich über Kommandozeilenargumente anpassen.
