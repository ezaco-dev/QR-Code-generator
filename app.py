from flask import Flask, request, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

HTML_TEMPLATE = """  
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
    <style>
      body {  
                font-family: Arial, sans-serif;  
                margin: 20px;  
                height: 100vh;  
                background-color: #1e1e1e;  
                color: white;  
                display: flex;  
                flex-direction: column;  
                align-items: center;  
                justify-content: center;  
            }  
            form {  
                text-align: center;  
                background-color: #2e2e2e;  
                padding: 20px;  
                border-radius: 10px;  
                width: 50%;  
            }  
            input, select, button {  
                margin: 10px;  
                padding: 10px;  
                width: 80%;  
            }  
            button {  
                background-color: #00adb5;  
                color: white;  
                border: none;  
                cursor: pointer;  
            }  
    </style>
</head>
<body>
    <h2>Buat QR Code</h2>
    <form action="/" method="post">
        <input type="text" name="text" placeholder="Masukkan teks atau URL" required>
        <button type="submit">Buat QR</button>
    </form>

    {% if qr_img %}
    <h3>QR Code Anda:</h3>
    <img src="data:image/png;base64,{{ qr_img }}" alt="QR Code">
    <br>
    <a href="/download?q={{ text }}">
        <button>Download QR</button>
    </a>
    {% endif %}
</body>
</html>
"""

import base64

@app.route("/", methods=["GET", "POST"])
def index():
    qr_img = None
    text = None
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            img_io = io.BytesIO()
            qr = qrcode.make(text)
            qr.save(img_io, format="PNG")
            img_io.seek(0)
            qr_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")
            qr_img = qr_base64
    return render_template_string(HTML_TEMPLATE, qr_img=qr_img, text=text)

@app.route("/download")
def download_qr():
    text = request.args.get("q")
    if not text:
        return "Masukkan teks!", 400

    img_io = io.BytesIO()
    qr = qrcode.make(text)
    qr.save(img_io, format="PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="qrcode.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)