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

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "json"}


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
    file.save(filepath)

    file_type = filename.rsplit(".", 1)[1].lower()
    text = extract_text(filepath, file_type)
    chunks = chunk_text(text)
    vector_db.add_chunks(chunks, filename)

    os.remove(filepath)
    return jsonify(
        {"message": f"File {filename} processed successfully", "chunks": len(chunks)}
    )


@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    results = vector_db.search(user_query)
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


if __name__ == "__main__":
    app.run(debug=True, port=5001)
