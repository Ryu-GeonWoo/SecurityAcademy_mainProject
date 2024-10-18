from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.document_loaders import PyMuPDFLoader

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from langchain.text_splitter import RecursiveCharacterTextSplitter

# llm = ChatOllama(model="Llama-3-Open-Ko-8B-Q8_0:latest", streaming=False)
# llm = ChatOllama(model="None")
llm = ChatOllama(model="Llama-3-Open-Ko-8B-Q8_0:latest")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 AIBot이라는 유용하고 전문적인 비서입니다. 먼저 자신을 소개하고 질문에 답하세요."),
    MessagesPlaceholder(variable_name='messages1'),    
])

chain = prompt | llm | StrOutputParser()

#chain.invoke({"input":"What is stock?"})