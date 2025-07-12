from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files.get("image")
        width = request.form.get("width")
        height = request.form.get("height")
        percent = request.form.get("percent")

        if not image:
            return "No image provided", 400

        try:
            img = Image.open(image)

            # Convert to RGB if needed
            if img.mode == 'RGBA':
                img = img.convert("RGB")

            original_size = img.size  # (width, height)

            # Decide resizing method
            if percent:
                scale = int(percent) / 100
                new_width = int(img.width * scale)
                new_height = int(img.height * scale)
                img = img.resize((new_width, new_height))
            elif width and height:
                img = img.resize((int(width), int(height)))
            else:
                return "Please provide either width & height or percentage", 400

            # Build download filename
            original_filename = secure_filename(image.filename)
            base_name, _ = os.path.splitext(original_filename)
            new_filename = f"{base_name}_resized.jpg"

            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)

            return send_file(
                buffer,
                as_attachment=True,
                download_name=new_filename,
                mimetype="image/jpeg"
            )

        except Exception as e:
            return f"Error processing image: {e}", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
