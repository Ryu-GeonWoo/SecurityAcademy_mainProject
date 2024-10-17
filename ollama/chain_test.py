from typing import List
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableMap, RunnablePassthrough

# 1. PDF 파일 로드
loader = PyMuPDFLoader("HTML.pdf")
pages = loader.load()

# 2. 문서 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
splits = text_splitter.split_documents(pages)

# 3. 안전한 임베딩 클래스를 정의합니다.
class SafeHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    def embed_query(self, query: str) -> List[float]:
        if isinstance(query, dict):
            query_text = query.get("page_content", "")
        else:
            query_text = query
        return super().embed_query(query_text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        processed_texts = []
        for text in texts:
            if isinstance(text, dict):
                processed_texts.append(text.get("page_content", ""))
            else:
                processed_texts.append(str(text))
        return super().embed_documents(processed_texts)

# 4. 임베딩 모델 설정 (수정된 클래스 사용)
embeddings = SafeHuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True},
)

# 5. 벡터스토어 생성 및 저장
vectorstore = FAISS.from_documents(splits, embedding=embeddings)
MY_FAISS_INDEX = "MY_FAISS_INDEX"
vectorstore.save_local(MY_FAISS_INDEX)

# 6. 벡터스토어 로드
vectorstore = FAISS.load_local(MY_FAISS_INDEX, embeddings, allow_dangerous_deserialization=True)

# 7. 리트리버 생성
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
retrieved_docs = retriever.invoke("RFC")
print("rerieved_docs==========", retrieved_docs)

# 11. 프롬프트 템플릿 생성 (context 포함)
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Answer in Korean.

    #Context: 
    {context}

    #Question:
    {question}

    #Answer:"""
)

# 12. LLM 객체 생성
llm = ChatOllama(model="Llama-3-Open-Ko-8B-Q8_0:latest")

# 14. 체인 구성
chain = (    
    {"context": retriever, "question": RunnablePassthrough()}    
    | prompt
    | llm
    | StrOutputParser()
)

# question = "RFC에 대해 설명해줘"
# response = chain.invoke(question)
# print("Assistant:", response)

# question = "대전이란"
# response = chain.invoke(question)
# print("Assistant:", response)