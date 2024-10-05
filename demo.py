import openai

# Set up your API key
openai.api_key = 'your-api-key-here'

# Function to generate a quiz question or respond to student queries
def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use 'gpt-3.5-turbo' for faster results, if available
        prompt=prompt,
        max_tokens=150,  # Adjust based on how long your expected response is
        temperature=0.5  # Controls randomness. Lower values give more focused answers.
    )
    return response.choices[0].text.strip()

# Example use-case for generating a quiz question
prompt = """
Based on this content from the children’s math book:
"Hindu-Arabic numerals are 0, 1, 2, 3, 4, 5, 6, 7, 8, 9."
Generate a quiz question about Hindu-Arabic numerals.
"""

quiz_question = ask_chatgpt(prompt)
print("Generated Quiz Question:", quiz_question)

# Example use-case for answering student queries
student_query = """
What is the Hindu-Arabic numeral for five?
"""

response = ask_chatgpt(f"Student Question: {student_query}")
print("ChatGPT Answer:", response)

