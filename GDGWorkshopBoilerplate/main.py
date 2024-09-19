import os
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import traceback
import anthropic
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Folder where uploaded files are stored
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# # Set your Anthropic API key
# ANTHROPIC_API_KEY = 'your-api-key'
# client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def extract_text_from_pdf(file_path, page_limit=2):
#     try:
#         with open(file_path, 'rb') as file:
#             reader = PdfReader(file)
#             text = ""
#             for i, page in enumerate(reader.pages):
#                 if i < page_limit:
#                     page_text = page.extract_text()
#                     text += page_text + "\n" if isinstance(page_text, str) else str(page_text) + "\n"
#                 else:
#                     break
#             return text
#     except Exception as e:
#         raise ValueError(f"Error extracting text from PDF: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

# def generate_flashcards(text):
#     prompt = f"""
#     Turn the following text into a series of flashcards. Each flashcard should have a question and a corresponding answer. Structure the result in the format:
#     Q: [Question 1]
#     A: [Answer 1]
#     Q: [Question 2]
#     A: [Answer 2]
#     Text:
#     {text[:15000]}
#     """
#     response = client.messages.create(
#         model="claude-3-opus-20240229",
#         max_tokens=4000,
#         temperature=0.5,
#         system="You are an expert study assistant, skilled at creating concise yet comprehensive flashcards.",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.content

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            # extracted_text = extract_text_from_pdf(file_path, page_limit=2)
            # flashcards = generate_flashcards(extracted_text)
            
            # Log the type and content of flashcards
            app.logger.debug(f"Type of flashcards: {type(flashcards)}")
            app.logger.debug(f"Content of flashcards: {flashcards}")
            
            # # Extract the text content if flashcards is a TextBlock object or a list containing a TextBlock
            # if isinstance(flashcards, list) and len(flashcards) > 0 and hasattr(flashcards[0], 'text'):
            #     flashcards = flashcards[0].text
            # elif hasattr(flashcards, 'text'):
            #     flashcards = flashcards.text
            # elif not isinstance(flashcards, str):
            #     flashcards = str(flashcards)
            
            # Remove the introductory text if present
            # flashcards = flashcards.replace("Here are the flashcards based on the provided text:\n\n", "")
            
            # Log the final flashcards content being sent to the client
            # app.logger.debug(f"Final flashcards content: {flashcards}")
            
            # return jsonify({'flashcards': flashcards}), 200
        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}")
            app.logger.error(traceback.format_exc())
            return jsonify({'error': f"Server Error: {str(e)}"}), 500
        finally:
            os.remove(file_path)
    else:
        return jsonify({'error': 'File type not allowed'}), 400
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)