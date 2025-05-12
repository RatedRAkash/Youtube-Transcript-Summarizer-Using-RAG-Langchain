from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


class BuildChain:

    def format_docs(self, retrieved_docs):
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return context_text

    def build_chain(self, retriever, prompt, llm, question):
        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(self.format_docs),
            'question': RunnablePassthrough()
        })

        parser = StrOutputParser()
        main_chain = parallel_chain | prompt | llm | parser
        ans = main_chain.invoke(question)
        return ans