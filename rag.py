from ollama import chat
from search import search_documents


def generate_answer_with_ollama(question, context):

    prompt = f"""
You are an AI assistant.

Answer the question using only the provided context.

If the answer is not available in the context, say:
"Information not found in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    response = chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def ask_question(question):

    results = search_documents(
        question,
        n_results=3
    )

    # Extract only the text from each search result
    documents = []

    for result in results:
        documents.append(result["text"])

    # Combine retrieved chunks into one context
    context = "\n\n".join(documents)

    # Send question + retrieved context to Ollama
    answer = generate_answer_with_ollama(
        question,
        context
    )

    return answer


if __name__ == "__main__":

    question = "What is the payment deadline?"

    answer = ask_question(question)

    print(answer)