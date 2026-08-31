import ollama


MODEL_NAME = "llama3.2:3b"


def generate_investigation_reasoning(
    complaint: str,
    extracted_text: str,
    entities: dict,
    analysis: dict,
    retrieved_knowledge: list
):

    knowledge_text = "\n\n".join(
        [
            (
                f"Source: {item['document']['filename']}\n"
                f"{item['document']['text']}"
            )
            for item in retrieved_knowledge
        ]
    )

    prompt = f"""
You are an AI assistant helping a bank fraud investigator.

Your job is to analyze evidence and provide a careful,
evidence-grounded investigation assessment.

IMPORTANT RULES:

- Use only information present in the evidence and
  retrieved banking knowledge.
- Do not invent transaction details.
- Do not claim that a person is definitely a criminal.
- Clearly distinguish observed evidence from interpretation.
- The rule-based risk score is a signal, not proof of fraud.
- Keep the report concise and useful to an investigator.

CUSTOMER COMPLAINT:
{complaint}

EXTRACTED EVIDENCE:
{extracted_text}

EXTRACTED ENTITIES:
{entities}

RULE-BASED RISK ANALYSIS:

Risk Score:
{analysis["risk_score"]}/100

Risk Level:
{analysis["risk_level"]}

Indicators:
{analysis["indicators"]}

RETRIEVED BANKING KNOWLEDGE:
{knowledge_text}

Produce an investigation report with exactly these sections:

1. SUMMARY
2. OBSERVED EVIDENCE
3. SUSPICIOUS INDICATORS
4. RELEVANT BANKING GUIDANCE
5. RECOMMENDED INVESTIGATOR ACTION

Do not add unsupported facts.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]