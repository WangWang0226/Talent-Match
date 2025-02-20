import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from config import UPLOAD_FOLDER
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

# Create handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
# Create formatters
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Add formatters to handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Add handlers to logger
app.logger.addHandler(console_handler)
app.logger.addHandler(file_handler)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize vector store and PDF processor
vector_store = VectorStore()
vector_store.delete_all_documents()
pdf_processor = PDFProcessor(vector_store.vector_store)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_files():
    try:
        vector_store.delete_all_documents()

        app.logger.debug(f"Files in request: {request.files}")

        if "files[]" not in request.files:
            app.logger.error("No files[] in request")
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist("files[]")
        app.logger.debug(f"Number of files received: {len(files)}")

        if not files:
            app.logger.error("Empty files list")
            return jsonify({"error": "Empty files"}), 400

        processed_files = []
        for file in files:
            if file and file.filename.endswith(".pdf"):
                try:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    app.logger.debug(f"Saving file to: {filepath}")
                    file.save(filepath)
                    pdf_processor.process_pdf(filepath)
                    processed_files.append(filename)
                except Exception as e:
                    app.logger.error(f"Error processing file {file.filename}: {str(e)}")
                    return (
                        jsonify({"error": f"Error processing file {file.filename}"}),
                        500,
                    )
        # Run cleanup of old files
        pdf_processor.cleanup_old_files(hours=24)

        app.logger.info(
            f"Successfully processed {len(processed_files)} files: {processed_files}"
        )
        return jsonify(
            {
                "message": f'Successfully processed files: {", ".join(processed_files)}',
                "processed_count": len(processed_files),
            }
        )

    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "No query provided"}), 400

    response = pdf_processor.query_documents(data["query"])
    return jsonify({"response": response})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "No question provided"}), 400

    response = pdf_processor.ask(data["query"])
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
