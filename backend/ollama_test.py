import ollama


response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": (
                "Explain briefly why asking a banking "
                "customer for an OTP can be a fraud indicator."
            )
        }
    ]
)


print("===== OLLAMA TEST =====")
print(response["message"]["content"])