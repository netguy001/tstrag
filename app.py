from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from groq import Groq
from config import Config
from utils.extractor import extract_text
from utils.chunker import chunk_text
from utils.embeddings import VectorDB

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER

vector_db = VectorDB()
groq_client = Groq(api_key=Config.GROQ_API_KEY)

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "json", "md"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(filepath)

        file_type = filename.rsplit(".", 1)[1].lower()
        text = extract_text(filepath, file_type)

        # Check if text was extracted
        if not text or len(text.strip()) < 10:
            os.remove(filepath)
            return (
                jsonify(
                    {
                        "error": f"File '{filename}' is too small or empty (needs at least 10 characters)"
                    }
                ),
                400,
            )

        chunks = chunk_text(text)

        # Check if chunks were created
        if not chunks or len(chunks) == 0:
            os.remove(filepath)
            return jsonify({"error": f"Could not create chunks from '{filename}'"}), 400

        # Add chunks to vector database
        vector_db.add_chunks(chunks, filename)

        return jsonify(
            {
                "message": f"File {filename} processed successfully",
                "chunks": len(chunks),
            }
        )

    except Exception as e:
        # Clean up file if processing fails
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500


@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        results = vector_db.search(user_query)

        # Check if any results were found
        if not results["documents"] or not results["documents"][0]:
            return jsonify(
                {
                    "answer": "No relevant information found in uploaded documents. Please upload documents first.",
                    "sources": [],
                }
            )

        context = "\n\n".join(results["documents"][0])
        sources = [meta["filename"] for meta in results["metadatas"][0]]

        prompt = f"""Answer the question using ONLY the provided context. If the answer is not in the context, say "Information not found in uploaded documents."

Context:
{context}

Question: {user_query}

Answer:"""

        response = groq_client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer, "sources": list(set(sources))})

    except Exception as e:
        return jsonify({"error": f"Error querying documents: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
