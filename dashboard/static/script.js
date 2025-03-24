const API_BASE = "http://192.168.8.195:8080"; // Change if running on a different host

// Fetch and update BPM values
async function refreshBpm() {
    try {
        let response = await fetch(`${API_BASE}/bpm/`);
        let data = await response.json();
        document.getElementById("bpm").textContent = data.bpm;
        
        response = await fetch(`${API_BASE}/bpm/min/`);
        data = await response.json();
        document.getElementById("minBpm").textContent = data.min_bpm;

        response = await fetch(`${API_BASE}/bpm/max/`);
        data = await response.json();
        document.getElementById("maxBpm").textContent = data.max_bpm;
    } catch (error) {
        console.error("Error fetching BPM:", error);
    }
}

// Set a new BPM
async function setBpm() {
    const bpm = document.getElementById("bpmInput").value;
    if (bpm > 0) {
        try {
            let response = await fetch(`${API_BASE}/bpm/`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ bpm: parseInt(bpm) })
            });
            let data = await response.json();
            alert(data.message);
            refreshBpm(); // Update values
        } catch (error) {
            console.error("Error setting BPM:", error);
        }
    } else {
        alert("Please enter a valid BPM value.");
    }
}

// Reset the minimum BPM
async function resetMinBpm() {
    try {
        let response = await fetch(`${API_BASE}/bpm/min/`, { method: "DELETE" });
        let data = await response.json();
        alert(data.message);
        refreshBpm();
    } catch (error) {
        console.error("Error resetting min BPM:", error);
    }
}

// Reset the maximum BPM
async function resetMaxBpm() {
    try {
        let response = await fetch(`${API_BASE}/bpm/max/`, { method: "DELETE" });
        let data = await response.json();
        alert(data.message);
        refreshBpm();
    } catch (error) {
        console.error("Error resetting max BPM:", error);
    }
}

// Load BPM values on startup
setInterval(refreshBpm, 2000);

