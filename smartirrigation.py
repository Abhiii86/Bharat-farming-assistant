from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 🌐 Frontend (HTML + JS)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Irrigation</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding: 40px;
        }
        input, select {
            padding: 10px;
            margin: 8px;
            border-radius: 5px;
            border: none;
            width: 220px;
        }
        button {
            padding: 10px 15px;
            background: #22c55e;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }
        .card {
            margin-top: 20px;
            padding: 20px;
            background: #1e293b;
            border-radius: 10px;
            display: inline-block;
        }
    </style>
</head>
<body>

    <h1>💧 Smart Irrigation System</h1>

    <input type="text" id="crop" placeholder="Crop (Rice, Wheat)">
    <br>
    <select id="stage">
        <option>Germination</option>
        <option>Vegetative</option>
        <option>Flowering</option>
        <option>Maturity</option>
    </select>
    <br>
    <select id="soil">
        <option>Sandy</option>
        <option>Clay</option>
        <option>Loamy</option>
    </select>
    <br>
    <input type="number" id="temp" placeholder="Temperature °C">
    <br>
    <input type="number" id="humidity" placeholder="Humidity %">
    <br>
    <input type="number" id="days" placeholder="Days since last watering">
    <br>

    <button onclick="getIrrigation()">Get Advice</button>

    <div id="result"></div>

    <script>
        function getIrrigation() {
            const data = {
                crop: document.getElementById("crop").value,
                stage: document.getElementById("stage").value,
                soil: document.getElementById("soil").value,
                temp: document.getElementById("temp").value,
                humidity: document.getElementById("humidity").value,
                days: document.getElementById("days").value
            };

            document.getElementById("result").innerHTML = "Analyzing...";

            fetch("/irrigation", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("result").innerHTML = `
                    <div class="card">
                        <h3>💡 Recommendation</h3>
                        <p>${data.advice}</p>
                    </div>
                `;
            })
            .catch(() => {
                document.getElementById("result").innerHTML = "Error";
            });
        }
    </script>

</body>
</html>
"""

# 🏠 Home
@app.route("/")
def home():
    return render_template_string(HTML)

# 💧 Irrigation Logic
@app.route("/irrigation", methods=["POST"])
def irrigation():
    data = request.json

    temp = float(data.get("temp", 0))
    humidity = float(data.get("humidity", 0))
    days = int(data.get("days", 0))
    soil = data.get("soil", "").lower()

    advice = ""

    # 🔥 Simple smart logic
    if temp > 35:
        advice += "High temperature detected. Increase watering. "

    if humidity < 40:
        advice += "Low humidity. Soil dries faster. "

    if days > 3:
        advice += "It's been many days since last irrigation. Water now. "

    if soil == "sandy":
        advice += "Sandy soil drains quickly. Frequent irrigation needed. "
    elif soil == "clay":
        advice += "Clay soil retains water. Avoid overwatering. "
    elif soil == "loamy":
        advice += "Loamy soil is balanced. Moderate watering is enough. "

    if advice == "":
        advice = "Conditions are normal. Maintain regular irrigation schedule."

    return jsonify({"advice": advice})

# ▶ Run app
if __name__ == "__main__":
    app.run(debug=True)