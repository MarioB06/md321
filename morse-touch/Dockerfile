FROM python:3.11-slim

WORKDIR /app

COPY morse_decoder.py touch_morse.py ./

CMD ["python", "-u", "touch_morse.py", "--simulate"]
