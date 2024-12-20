from flask import Flask, request, Response
import os  # For retrieving environment variables
from data_loader import PDFTextProcessor
from Agent import agent as create_agent
from flask_cors import CORS


# Initialize the Flask app
app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return "Welcome to the Resume Transformer API"

@app.route('/process_resume', methods=['POST'])
def process_resume():
    # Check if the request contains files
    if not request.files:
        return Response("No file provided", status=400)

    # Get the first file from the request (you can extend this if you have multiple files)
    file = list(request.files.values())[0]
    if not file:
        return Response("No file provided", status=400)

    # Process the file
    processor = PDFTextProcessor(file)
    cv = processor.process()

    # Run your agent on the processed resume
    outcome = create_agent("Can you transform this into a PM Resume"+cv)

    # Return the outcome as plain text
    return Response(outcome, mimetype='text/plain')

if __name__ == '__main__':
    # Use the environment variable for the port, or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)