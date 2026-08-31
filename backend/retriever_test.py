from services.retriever import Retriever


retriever = Retriever()


query = """
The customer received a message asking them
to provide an OTP and visit a banking website.
"""


results = retriever.retrieve(
    query,
    top_k=3
)


print("===== RETRIEVAL TEST =====")

for index, result in enumerate(results, start=1):

    print()
    print(f"RESULT {index}")

    print("FILE:")
    print(result["document"]["filename"])

    print("DISTANCE:")
    print(result["distance"])

    print("TEXT:")
    print(result["document"]["text"])