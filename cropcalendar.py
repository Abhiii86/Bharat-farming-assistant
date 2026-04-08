from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 🌐 Frontend (HTML + JS)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Crop Calendar</title>
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
            text-align: left;
        }
    </style>
</head>
<body>

    <h1>🌾 Crop Calendar</h1>

    <input type="text" id="crop" placeholder="Crop (Rice, Wheat)">
    <br>

    <select id="season">
        <option>Kharif</option>
        <option>Rabi</option>
        <option>Zaid</option>
    </select>
    <br>

    <input type="text" id="region" placeholder="Region (Karnataka)">
    <br>

    <button onclick="getCalendar()">Generate Calendar</button>

    <div id="result"></div>

    <script>
        function getCalendar() {
            const data = {
                crop: document.getElementById("crop").value,
                season: document.getElementById("season").value,
                region: document.getElementById("region").value
            };

            document.getElementById("result").innerHTML = "Generating...";

            fetch("/calendar", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("result").innerHTML = `
                    <div class="card">
                        <h3>📅 Crop Schedule</h3>
                        <p>${data.calendar}</p>
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

# 🌾 Crop Calendar Logic
@app.route("/calendar", methods=["POST"])
def calendar():
    data = request.json

    crop = data.get("crop", "").lower()
    season = data.get("season")
    region = data.get("region")

    # 📅 Simple calendar logic (based on typical patterns)
    if season == "Kharif":
        calendar = (
            "🌱 Sowing: June - July\n"
            "🌿 Growth: August - September\n"
            "🌾 Harvest: October - November"
        )
    elif season == "Rabi":
        calendar = (
            "🌱 Sowing: October - November\n"
            "🌿 Growth: December - January\n"
            "🌾 Harvest: February - March"
        )
    elif season == "Zaid":
        calendar = (
            "🌱 Sowing: March - April\n"
            "🌿 Growth: April - May\n"
            "🌾 Harvest: June"
        )
    else:
        calendar = "No data available."

    # 🌾 Crop-specific note
    if "rice" in crop:
        calendar += "\n💡 Rice requires high water during growth."
    elif "wheat" in crop:
        calendar += "\n💡 Wheat grows best in cool conditions."
    elif "maize" in crop:
        calendar += "\n💡 Maize needs well-drained soil."

    # 🌍 Region note
    if region:
        calendar += f"\n📍 Region considered: {region}"

    return jsonify({"calendar": calendar})

# ▶ Run app
if __name__ == "__main__":
    app.run(debug=True)