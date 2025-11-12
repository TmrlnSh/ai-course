from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_7EffP4_EQytj5kJFqaW4z6duJYQ75DdDkqdKfhmvY3WnYZ8ZF95fhTgeuVV2tuw9gcQtBQ")
index = pc.Index("wedevx")


index.upsert_records(
    "__default__",
    [
        {
            "_id": "rec1",
            "text": "SDET monthly price is $799/mo if annual, $3995/year",
            "category": "digestive system", 
        },
        {
            "_id": "rec2",
            "text": "DevOps monthly price is $500/mo if annual, $1200/year",
            "category": "cultivation",
        },
        {
            "_id": "rec3",
            "text": "AI Engineer monthly price is $2000/mo if annual, $10000/year",
            "category": "immune system",
        }
    ]
)

