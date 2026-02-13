from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama




llm = ChatOllama(
    model = "deepseek-r1:1.5b",
    temperature = 0
)



# llm = ChatGoogleGenerativeAI(
#     model='gemini-3-flash-preview'
# )