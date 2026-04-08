import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load trained model
MODEL_PATH = "crop_disease_model.h5"
model = load_model(MODEL_PATH)

# Update these class names according to your model training order
class_names = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Yellow_Leaf_Curl_Virus",
    "Tomato___mosaic_virus",
    "Tomato___healthy"
]

# Remedies / suggestions
disease_info = {
    "Tomato___Bacterial_spot": "Use copper-based bactericides and remove infected leaves.",
    "Tomato___Early_blight": "Apply fungicides and avoid overhead irrigation.",
    "Tomato___Late_blight": "Use resistant varieties and fungicide sprays immediately.",
    "Tomato___Leaf_Mold": "Improve air circulation and use fungicide if needed.",
    "Tomato___Septoria_leaf_spot": "Remove affected leaves and apply appropriate fungicide.",
    "Tomato___Spider_mites": "Use neem oil or miticides and keep humidity balanced.",
    "Tomato___Target_Spot": "Apply fungicide and avoid leaf wetness for long periods.",
    "Tomato___Yellow_Leaf_Curl_Virus": "Control whiteflies and remove infected plants.",
    "Tomato___mosaic_virus": "Remove infected plants and disinfect tools regularly.",
    "Tomato___healthy": "The plant looks healthy. Maintain proper care and monitoring."
}


def prepare_image(img_path, target_size=(224, 224)):
    """
    Load and preprocess image for model prediction.
    """
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None
    remedy = None
    image_path = None
    error = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "No file uploaded."
            return render_template("index.html", error=error)

        file = request.files["file"]

        if file.filename == "":
            error = "Please select an image."
            return render_template("index.html", error=error)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            try:
                processed_image = prepare_image(filepath)
                predictions = model.predict(processed_image)

                predicted_index = np.argmax(predictions[0])
                predicted_class = class_names[predicted_index]
                predicted_confidence = float(np.max(predictions[0])) * 100

                prediction = predicted_class.replace("___", " - ").replace("_", " ")
                confidence = round(predicted_confidence, 2)
                remedy = disease_info.get(predicted_class, "No remedy information available.")
                image_path = filepath

            except Exception as e:
                error = f"Prediction failed: {str(e)}"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        remedy=remedy,
        image_path=image_path,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)