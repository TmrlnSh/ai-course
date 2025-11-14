from pinecone import Pinecone
from openai import OpenAI


pc = Pinecone(api_key="pcsk_7EffP4_EQytj5kJFqaW4z6duJYQ75DdDkqdKfhmvY3WnYZ8ZF95fhTgeuVV2tuw9gcQtBQ")
index = pc.Index(name="wedevx")


search_prompt = "give me tutorial about key value store"

openai_client = OpenAI()

response = openai_client.embeddings.create(
            model="text-embedding-3-large",
            input=search_prompt,
            dimensions=1024
        )


results = index.query(vector=response.data[0].embedding, top_k=5, include_metadata=True)

print(f"Found {len(results.matches)} results:\n")

for match in results.matches:
    print(f"Score: {match.score:.4f}")
    print(f"ID: {match.id}")
    if match.metadata:
        print(f"Page: {match.metadata.get('page', 'N/A')}")
        print(f"Text: {match.metadata.get('text', '')}...")
    print("-" * 50)
