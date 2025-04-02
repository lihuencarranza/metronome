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

## Part II - HTML Dashboard

The dashboard allows users to communicate with the REST API provided by the metronome, making it easier to view and modify BPM values.

### Features

- Display BPM values: View the current BPM, minimum BPM, and maximum BPM.
- Set BPM: Update the metronome to a new BPM value.
- Reset BPM values: Reset the minimum and maximum BPM.
- Auto-refresh: The dashboard updates BPM values every 2 seconds.

### **Project Structure**

```
metronome/
-- metronome.py        # Python script running the REST API (outside the dashboard folder)
-- dashboard/
   +-- index.html      # Main HTML file for the dashboard  
   +-- script.js       # JavaScript file handling API requests  
   +-- style.css       # Basic styling for the dashboard  
```

### **Setup & Usage**

1. **Run the Metronome API**
   Make sure the `metronome.py` script is running. If not, start it with:

   ```sh
   python metronome.py
   ```

   The server should start on `http://127.0.0.1:8080` or your device�s IP address.
2. **Access the Dashboard**
   Open `index.html` in a browser. If running on the same device as the server, use:

   ```
   http://127.0.0.1:8080
   ```

   If accessing from another device on the same network, replace `127.0.0.1` with your Raspberry Pi's IP.
3. **Interacting with the Dashboard**

   - Click **Refresh BPM** to get the latest BPM values.
   - Enter a new BPM value and click **Set BPM** to update it.
   - Click **Reset Min BPM** or **Reset Max BPM** to reset the respective values.
   - The BPM values update automatically every 5 seconds.

### **Troubleshooting**

- If styles or scripts are not loading, ensure they are correctly linked in `index.html`.
- If API requests fail, verify that `metronome.py` is running and that `API_BASE` in `script.js` points to the correct server address.
- If accessing from another device, ensure the Raspberry Pi firewall allows connections to port 8080.

### **Future Improvements**

- Enhance the UI with better styling and animations.
- Add error messages for failed API requests.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
