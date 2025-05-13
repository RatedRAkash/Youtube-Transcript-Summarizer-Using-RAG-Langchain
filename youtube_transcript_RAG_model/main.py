from langchain_ollama import OllamaLLM
from build_chain import BuildChain
from utils import *

from dotenv import load_dotenv
import os

# Load .env file from the current directory
load_dotenv()

# loading Variables from .env
VECTOR_DATABASE_MODEL_PATH = os.getenv("VECTOR_DATABASE_MODEL_PATH")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
EMBEDDING_MODEL_API_URL = os.getenv("EMBEDDING_MODEL_API_URL")
FINAL_QUESTION = os.getenv("FINAL_QUESTION", "Can you summarize the video") # 2nd Parameter is the Default Value if Not Provided in .env


def get_summary_main(youtube_url_id, question):
    transcript = get_youtube_transcript(youtube_url_id)
    chunks = indexing_by_text_split(transcript)
    # print(len(chunks))
    # print(chunks[6])

    # Saving Model
    SAVE_MODEL_PATH = VECTOR_DATABASE_MODEL_PATH
    generate_embedding_and_save_in_vector_store(SAVE_MODEL_PATH, chunks, EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_API_URL)

    # Retrieving saved Model
    LOAD_MODEL_PATH = SAVE_MODEL_PATH
    retriever = get_retriever_from_saved_model(LOAD_MODEL_PATH, EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_API_URL)

    # retriever.invoke("PM and Sri Lanka")
    final_prompt = combine_context_and_user_query_to_get_final_augmented_prompt_text(retriever=retriever, question=question)
    # print("=====================Final Augmented Prompt Passed to LLM========================\n")
    # print(final_prompt)

    # initializing Ollama LLM Model
    llm = OllamaLLM(model=LLM_MODEL)
    # answer = llm.invoke(final_prompt)
    # FINAL_QUESTION = "Can you summarize the video"
    final_answer = BuildChain().build_chain(retriever=retriever, prompt=final_prompt, llm=llm, question=FINAL_QUESTION)

    return final_answer


# Main Function
if __name__ == '__main__':
    final_answer = get_summary_main("uk6PY3v3038", "is the topic about Sri Lanka Crisis & Nadir on the Go")
    print("=====================Final Summary========================\n")
    print(final_answer)