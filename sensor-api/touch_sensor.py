from RPi import GPIO
import time, signal, sys

TOUCH = 11  # BOARD (phys. Pin 11 = BCM 17)

def do_smt(ch):
    print("Touch wurde erkannt")

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Touch-Sensor läuft (Polling)…")
    last = GPIO.input(TOUCH)
    try:
        while True:
            v = GPIO.input(TOUCH)
            # Flanke High->Low (active-low Taster/Touch)
            if last == 1 and v == 0:
                do_smt(TOUCH)
                time.sleep(0.2)  # einfache Entprellung
            last = v
            time.sleep(0.01)     # 10ms Polling
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
