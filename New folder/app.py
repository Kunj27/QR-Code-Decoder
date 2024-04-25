from flask import Flask, render_template, request
from PIL import Image
from pyzbar.pyzbar import decode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decode_qr_code', methods=['POST'])
def decode_qr_code():
    if 'file' not in request.files:
        return render_template('result.html', error="No file part")
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('result.html', error="No selected file")

    try:
        image = Image.open(file)
        decoded_objects = decode(image)
        
        if decoded_objects:
            decoded_data = decoded_objects[0].data.decode('utf-8')
            return render_template('result.html', decoded_data=decoded_data)
        else:
            return render_template('result.html', error="No QR code found in the image")
    except Exception as e:
        return render_template('result.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
