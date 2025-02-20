# Contents of /resume-analyzer/resume-analyzer/README.md

# Resume Analyzer

This project is a web application designed to help HR professionals review resumes efficiently. It allows users to upload multiple PDF resumes, processes them, and enables users to ask questions regarding the content of the resumes.

## Features

- Upload multiple PDF files.
- Extract and analyze text from resumes.
- Store and retrieve data using Pinecone vector database.
- User-friendly web interface for interaction.

## Project Structure

- `src/backend`: Contains the backend logic of the application.
  - `app.py`: Entry point for the Flask application.
  - `config.py`: Configuration settings for the application.
  - `pdf_processor.py`: Functions for processing PDF files.
  - `vector_store.py`: Handles interactions with the Pinecone vector database.
  
- `src/frontend`: Contains the frontend files.
  - `static`: Contains CSS and JavaScript files.
  - `templates`: Contains HTML templates.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd resume-analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file.

5. Run the application:
   ```
   python src/backend/app.py
   ```

6. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- Navigate to the upload page.
- Select multiple PDF files to upload.
- Ask questions about the resumes after processing.

## License

This project is licensed under the MIT License.