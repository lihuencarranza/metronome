# BPM Tap Metronome with Raspberry Pi & Flask

This project is a tap-based metronome using a Raspberry Pi with physical buttons and LEDs. It includes a Flask API to interact with the BPM data and uses a JSON file to store BPM values persistently.


## Installation

1. Set up Raspberry Pi GPIO:

`sudo apt update && sudo apt install python3-pip`
`pip install flask RPi.GPIO`

2. Clone the repository:

`git clone https://github.com/your-repo/bpm-metronome.git`

`cd bpm-metronome`

3. Run the script:

`python3 metronome.py`
