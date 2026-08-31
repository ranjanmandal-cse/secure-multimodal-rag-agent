from services.knowledge_loader import load_documents


documents = load_documents()

print("===== KNOWLEDGE BASE =====")

for document in documents:
    print()
    print("FILE:", document["filename"])
    print(document["text"][:200])