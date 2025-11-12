from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_7EffP4_EQytj5kJFqaW4z6duJYQ75DdDkqdKfhmvY3WnYZ8ZF95fhTgeuVV2tuw9gcQtBQ")
index = pc.Index("wedevx")

results = index.search(
    namespace="__default__", 
    query={
        "inputs": {"text": "SDET"}, 
        "top_k": 2
    },
    fields=["category", "chunk_text"]
)

print(results)

