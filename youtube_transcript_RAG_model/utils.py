import os

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from ollama_embedding import MyLocalOllamaEmbeddings # My Local Ollama Embeddings

from langchain_core.prompts import PromptTemplate

def get_youtube_transcript(video_id):
    # video_id = "uk6PY3v3038"
    try:
        youtube_transcript_api_obj = YouTubeTranscriptApi()
        transcript_list = youtube_transcript_api_obj.fetch(video_id=video_id, languages=["en"])

        transcript = " ".join(res.text for res in transcript_list)

        # print(transcript)
        return transcript

    except TranscriptsDisabled:
        print("No Captions available for this Video")

    except Exception as e:
        print(f"Unexpected error: {e}")

def indexing_by_text_split(transcript: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    return chunks

def generate_embedding_and_save_in_vector_store(SAVE_MODEL_TO_PATH, chunks, model_name, model_endpoint):
    embeddings = MyLocalOllamaEmbeddings(model=model_name, url=model_endpoint)
    vector_store = FAISS.from_documents(chunks, embeddings)

    # print("All documents in the vector store:\n")
    # for idx, doc_id in vector_store.index_to_docstore_id.items():
    #     document = vector_store.docstore.search(doc_id)
        # print(f"Document ID: {doc_id}")
        # print(f"Content: {document.page_content}")
        # print("-" * 50)

    # saving the Model Locally to given Path
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    SAVE_MODEL_TO_PATH = os.path.join(current_file_dir, SAVE_MODEL_TO_PATH)
    vector_store.save_local(SAVE_MODEL_TO_PATH)


def get_retriever_from_saved_model(LOAD_MODEL_PATH, model_name, model_endpoint):
    # Use the same embedding class you used during saving
    embeddings = MyLocalOllamaEmbeddings(model=model_name, url=model_endpoint)

    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    LOAD_MODEL_PATH = os.path.join(current_file_dir, LOAD_MODEL_PATH)
    # Load from the saved folder, "allow_dangerous_deserialization=True" so that we can load from "Untrusted" source which in this case is our LOCAL
    vector_store = FAISS.load_local(LOAD_MODEL_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    return retriever

def combine_context_and_user_query_to_get_final_augmented_prompt_text(retriever, question):
    prompt = PromptTemplate(
        template="""
          You are a helpful assistant.
          Answer ONLY from the provided transcript context.
          If the context is insufficient, just say you don't know.

          {context}
          Question: {question}
        """,
        input_variables=['context', 'question']
    )

    # retrieved_docs = retriever.invoke(question)
    # print(retrieved_docs)
    # context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    # print(context_text)

    # print(prompt.invoke({"context": context_text, "question": question}))

    return prompt
