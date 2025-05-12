from langchain_ollama import OllamaLLM
from build_chain import BuildChain
from utils import *

def get_summary_main(youtube_url_id, question):
    transcript = get_youtube_transcript(youtube_url_id)
    chunks = indexing_by_text_split(transcript)
    # print(len(chunks))
    # print(chunks[6])
    SAVE_MODEL_PATH = "saved_model_faiss_store"
    generate_embedding_and_save_in_vector_store(SAVE_MODEL_PATH, chunks)

    LOAD_MODEL_PATH = SAVE_MODEL_PATH
    retriever = get_retriever_from_saved_model(LOAD_MODEL_PATH)

    # retriever.invoke("PM and Sri Lanka")
    final_prompt = combine_context_and_user_query_to_get_final_augmented_prompt_text(retriever=retriever, question=question)
    # print("----------------------Final Augmented Prompt Passed to LLM----------------------\n")
    # print(final_prompt)

    # initializing Ollama LLM Model
    llm = OllamaLLM(model="llama3.1:8b")
    # answer = llm.invoke(final_prompt)
    final_question = "Can you summarize the video"
    final_answer = BuildChain().build_chain(retriever=retriever, prompt=final_prompt, llm=llm, question=final_question)

    print("----------------------Final Summary----------------------\n")
    print(final_answer)
    return final_answer


# Main Function
if __name__ == '__main__':
    get_summary_main("uk6PY3v3038", "is the topic about Sri Lanka Crisis")