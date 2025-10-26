# Morse Touch

Dieses Unterprojekt zeigt, wie sich ein einfacher Taster (z. B. Touch- oder Drucksensor)
als Morsecode-Eingabegerät verwenden lässt. Das Skript wertet die Länge eines Tastendrucks
aus, erkennt daraus Punkte und Striche und setzt sie anschließend wieder zu Buchstaben
und Wörtern zusammen.

## Verwendung

```bash
python touch_morse.py --simulate --log-level INFO
```

Im Simulationsmodus werden zuvor definierte Tastendrücke abgespielt, sodass sich die Logik
auch ohne echte Hardware demonstrieren lässt. Währenddessen erscheinen im Log alle erkannten
Taster-Ereignisse (Drücken, Loslassen, Buchstaben, Wörter). Über den Parameter `--log-level`
kann die Menge der Ausgaben gesteuert werden.

Für den Betrieb auf einem Raspberry Pi kann das Skript ohne den Parameter `--simulate`
gestartet werden. Der Taster muss dabei mit dem physikalischen Pin 11 (BCM 17) verbunden sein.
Die Logausgaben erscheinen ebenfalls auf der Konsole.

## Docker-Compose

Analog zu den anderen Unterprojekten lässt sich das Skript nun auch über Docker Compose
starten:

```bash
docker compose up morse-touch
```

Im Container wird standardmäßig der Simulationsmodus ausgeführt. Soll reale Hardware
angesprochen werden, kann der Dienst im Compose-File um `privileged: true` sowie das
Durchreichen von `/dev/gpiomem` ergänzt und der Start-Befehl entsprechend angepasst werden.

## Funktionsweise

- Jeder Tastendruck wird gemessen.
- Kurze Drücke (< 300 ms) zählen als Punkt, längere Drücke als Strich.
- Die Pausen zwischen den Drücken entscheiden darüber, ob ein Buchstabe oder ein Wort
  abgeschlossen wurde.

Die Schwellenwerte lassen sich über Kommandozeilenargumente anpassen.
