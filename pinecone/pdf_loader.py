from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI
from pinecone import Pinecone

# Load PDF and split into pages
loader = PyPDFLoader("System Design.pdf")
pages = loader.load_and_split()

print(pages[0].page_content)

pc = Pinecone(api_key='pcsk_7EffP4_EQytj5kJFqaW4z6duJYQ75DdDkqdKfhmvY3WnYZ8ZF95fhTgeuVV2tuw9gcQtBQ')
index = pc.Index("wedevx")
openai_client = OpenAI()

all_vectors = []

for page in pages:
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=page.page_content,
        dimensions=1024
    )
    embedding = response.data[0].embedding
    page_num = page.metadata.get("page", "unknown")

    vector = {
        "id": f"page_{page_num}", 
        "values": embedding,
        "metadata": {
            "text": page.page_content,
            "source": "System Design Book",
            "page": page_num
        }
    }
    all_vectors.append(vector)

batch_size = 100
for i in range(0, len(all_vectors), batch_size):
    batch = all_vectors[i:i + batch_size]
    index.upsert(vectors=batch)

print("done")