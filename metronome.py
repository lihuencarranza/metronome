import RPi.GPIO as GPIO
import time
import json
import os
from flask import Flask, jsonify, request, send_from_directory

# JSON file to store BPM data
DATA_FILE = "part2/bpm_data.json"

# GPIO Pins
LED_RED = 26      # Red LED (learn mode)
LED_BLUE = 23     # Blue LED (play mode)
BUTTON_RED = 17   # Tap button
BUTTON_BLUE = 24  # Mode switch button

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)
GPIO.setup(BUTTON_RED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_BLUE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Flask setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            static_folder=os.path.join(BASE_DIR, 'part2', 'static'), 
            template_folder=os.path.join(BASE_DIR, 'part2'))

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(BASE_DIR, 'part2'), 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'part2', 'static'), filename)

# State variables
learn_mode = True  # Start in "learn mode"
taps = []  # List to store tap timestamps
min_taps = 4  # Minimum taps required for BPM calculation

# Function to save data to JSON
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"bpm": bpm, "min_bpm": min_bpm, "max_bpm": max_bpm}, f)

# Function to load data from JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return (
                int(data.get("bpm", 0)), 
                int(data.get("min_bpm", 0)) if data.get("min_bpm") is not None else None, 
                int(data.get("max_bpm", 0)) if data.get("max_bpm") is not None else None
            )
    return 0, None, None  # Default values if file doesn't exist


# Load BPM data on startup
bpm, min_bpm, max_bpm = load_data()

# Initial LED blink
GPIO.output(LED_RED, GPIO.HIGH)
GPIO.output(LED_BLUE, GPIO.HIGH)
time.sleep(1)
GPIO.output(LED_RED, GPIO.LOW)
GPIO.output(LED_BLUE, GPIO.LOW)

# Function to calculate BPM
def calculate_bpm():
    global min_bpm, max_bpm
    if len(taps) < min_taps:
        return 0  # Not enough data

    intervals = [taps[i] - taps[i-1] for i in range(1, len(taps))]
    avg_interval = sum(intervals) / len(intervals)
    new_bpm = int(60 / avg_interval)

    # Update min/max BPM
    if min_bpm is None or new_bpm < min_bpm:
        min_bpm = new_bpm
    if max_bpm is None or new_bpm > max_bpm:
        max_bpm = new_bpm

    save_data()  # Save changes
    return new_bpm

# Function to handle red button press (record taps)
def button_red_pressed(channel):
    global taps
    if learn_mode:
        taps.append(time.time())  # Record tap time
        GPIO.output(LED_RED, GPIO.HIGH)
        time.sleep(0.1)  # Small blink effect
        GPIO.output(LED_RED, GPIO.LOW)

# Function to handle blue button press (toggle mode)
def button_blue_pressed(channel):
    global learn_mode, bpm, taps
    GPIO.output(LED_BLUE, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(LED_BLUE, GPIO.LOW)

    learn_mode = not learn_mode  # Toggle mode

    if not learn_mode:  # Switching to "play mode"
        bpm = calculate_bpm()
        print(f"BPM: {bpm}")
        taps = []  # Reset tap list
    else:
        print("Learn Mode On")

    save_data()  # Save changes

# Set up button event detection
GPIO.add_event_detect(BUTTON_RED, GPIO.RISING, callback=button_red_pressed, bouncetime=50)
GPIO.add_event_detect(BUTTON_BLUE, GPIO.RISING, callback=button_blue_pressed, bouncetime=50)

print("Metronome started")
print("Learn Mode On. Press the blue button to switch to Play Mode.")

# ========================
# Flask API
# ========================

@app.route('/bpm/', methods=['GET', 'PUT'])
def handle_bpm():
    global bpm, min_bpm, max_bpm
    if request.method == 'GET':
        return jsonify({"bpm": bpm})

    elif request.method == 'PUT':
        data = request.get_json()
        if "bpm" in data and isinstance(data["bpm"], int) and data["bpm"] > 0:
            bpm = data["bpm"]

            if min_bpm is None or bpm < min_bpm:
                min_bpm = bpm
            if max_bpm is None or bpm > max_bpm:
                max_bpm = bpm

            save_data()
            return jsonify({"message": "BPM updated", "bpm": bpm, "min_bpm": min_bpm, "max_bpm": max_bpm})

        return jsonify({"error": "Invalid BPM value"}), 400


@app.route('/bpm/min/', methods=['GET', 'DELETE'])
def handle_min_bpm():
    global min_bpm
    if request.method == 'GET':
        return jsonify({"min_bpm": min_bpm if min_bpm is not None else 0}) 
    elif request.method == 'DELETE':
        min_bpm = None  
        save_data()
        return jsonify({"message": "Min BPM reset"})

@app.route('/bpm/max/', methods=['GET', 'DELETE'])
def handle_max_bpm():
    global max_bpm
    if request.method == 'GET':
        return jsonify({"max_bpm": max_bpm if max_bpm is not None else 0}) 
    elif request.method == 'DELETE':
        max_bpm = None  
        save_data()
        return jsonify({"message": "Max BPM reset"})


# ========================
#  Start Flask Server
# ========================
import threading
server_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False))
server_thread.daemon = True
server_thread.start()

# ========================
#  Main Loop
# ========================
import time

try:
    last_pulse_time = time.perf_counter()

    while True:
        if not learn_mode and bpm > 0:
            interval = 60 / bpm  # Convert BPM to seconds
            current_time = time.perf_counter()

            if current_time - last_pulse_time >= interval:
                GPIO.output(LED_BLUE, GPIO.HIGH)
                time.sleep(0.05)  # Shorter LED blink
                GPIO.output(LED_BLUE, GPIO.LOW)
                
                last_pulse_time = current_time  # Reset the timer

        time.sleep(0.001)  # Small sleep to prevent CPU overload

except KeyboardInterrupt:
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    GPIO.cleanup()