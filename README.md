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

## API Endpoints

The Flask server runs on `http://raspberry_pi_ip:8080/`.

### Get or Update BPM

- GET`/bpm/` Returns the current BPM.`curl http://localhost:8080/bpm/`

  `curl -X GET http://localhost:8080/bpm/`
- PUT `/bpm/` Updates the BPM manually.`{ "bpm": 120 }`

  `curl -X PUT -H "Content-Type: application/json" -d '{"bpm": 150}' http://localhost:8080/bpm/`

### Get or Reset Minimum BPM

- GET `/bpm/min/` Returns the lowest recorded BPM.`curl -X GET http://localhost:8080/bpm/min/`
- DELETE `/bpm/min/` Resets the min BPM.`curl -X DELETE http://localhost:8080/bpm/min/`

### Get or Reset Maximum BPM

- GET `/bpm/max/`  Returns the highest recorded BPM.`curl -X GET http://localhost:8080/bpm/max/`
- DELETE `/bpm/max/`  Resets the max BPM.`curl -X DELETE http://localhost:8080/bpm/max/`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
