from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma


files = [
    "data/refund_policy.txt",
    "data/cancellation_policy.txt",
    "data/escalation_policy.txt"
]


documents = []


for file in files:

    loader = TextLoader(file)

    documents.extend(loader.load())


splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


docs = splitter.split_documents(documents)


embedding = OpenAIEmbeddings()


vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="./chroma_db"
)


retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)