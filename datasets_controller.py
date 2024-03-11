from mongodb_connector import vietnamese_legal_collection as collections

def find_similar_documents(embedding: list):
    documents = collections.aggregate([
        {
            "$vectorSearch": {
                "queryVector": embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": 5,
                "index": "vietnameseLegalIndex",
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1, 
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    return documents

if __name__ == "__main__":
    collections.delete_many({})
