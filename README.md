# Talent Match

This project is a web application using LLM + RAG technique, designed to help HR professionals review resumes efficiently. It allows users to upload multiple PDF resumes, store them in vector store, and enables users to compare and ask questions regarding the content of the resumes.

## Features
- Select multiple PDF files to upload to the Pinecone vector store.
- Enter your job description.
- Click `compare` button to compare these resumes.
![TalentMatch Demo](/public/demo-talent-match-1080p-part1.gif)

- You can see the comparison result in the LLM Response field:
![Comparison Result](/public/query-response.png)

- You can also ask questions to the resumes:
![Comparison Result](/public/demo-talent-match-1080p-part2.gif)


## Project Structure

- `src/backend`: Contains the backend logic of the application.
  - `app.py`: Entry point for the Flask application.
  - `config.py`: Configuration settings for the application.
  - `pdf_processor.py`: Functions for processing PDF files.
  - `vector_store.py`: Handles interactions with the Pinecone vector database.
  
- `src/frontend`: Contains the frontend files.
  - `static`: Contains CSS and JavaScript files.
  - `templates`: Contains HTML templates.

## Quick Start

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ResumeGPT-Assistant
   ```

2. Create a virtual environment and activate it:
   ```
   # Install pipenv if not installed
   brew install pipenv

   # Install from Pipfile
   pipenv install

   # Activate pipenv virtual environment
   pipenv shell
   ```

3. Set up environment variables in the `.env` file, you can refer to `.env.example`.

4. Run the application:
   ```
   python src/backend/app.py
   ```

5. Open your web browser and go to `http://127.0.0.1:5000`.


## License

This project is licensed under the MIT License.