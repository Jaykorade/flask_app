from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        # Save the uploaded file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        # Process the file (you can replace this with your own processing logic)
        with open(file_path, 'r') as file:
            processed_data = file.read().upper()  # Example: Convert text to uppercase

        # Save the processed data to a new file
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + uploaded_file.filename)
        with open(processed_file_path, 'w') as processed_file:
            processed_file.write(processed_data)

        # Provide the processed file for download
        return send_file(processed_file_path, as_attachment=True)

    return "No file uploaded."

if __name__ == '__main__':
    app.run(debug=True)
