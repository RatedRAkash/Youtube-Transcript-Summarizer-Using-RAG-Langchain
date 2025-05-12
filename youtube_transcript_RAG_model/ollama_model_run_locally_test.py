from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")

print("Local LLM Response: \n")
response = llm.invoke("Tell me about Lionel Messi World Cup 2022 Journey")

print(response)