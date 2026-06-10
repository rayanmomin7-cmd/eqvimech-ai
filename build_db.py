from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer
import os

print("Loading AI model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_or_create_collection(
    "eqvimech"
)

print("Reading PDFs...")

for file in os.listdir("pdfs"):

    if file.endswith(".pdf"):

        print("Processing:", file)

        try:

            reader = PdfReader(
                os.path.join("pdfs", file)
            )

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

            chunks = [
                text[i:i+1000]
                for i in range(
                    0,
                    len(text),
                    1000
                )
            ]

            for idx, chunk in enumerate(chunks):

                embedding = model.encode(
                    chunk
                ).tolist()

                collection.add(
                    ids=[
                        f"{file}_{idx}"
                    ],
                    embeddings=[
                        embedding
                    ],
                    documents=[
                        chunk
                    ]
                )

        except Exception as e:

            print(
                "Error:",
                file,
                e
            )

print("DATABASE READY")