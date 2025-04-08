import fitz
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def fetchTextFromPdf(pdfPath: str) -> str:
    text = ""
    doc = fitz.open(pdfPath)
    for page in doc:
        text += page.get_text()
    return text

def createChatBot(pdfPath: str):
    document_content = fetchTextFromPdf(pdfPath)

    # Create the prompt template
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer the question based on the following DOCUMENT: {document} QUESTION: {question}"
    )
    
    # Initialize the model
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create the chain using the new syntax
    chain = prompt | llm
    
    # Return a function that uses the new invoke syntax
    return lambda question: chain.invoke({
        "document": document_content,
        "question": question
    }).content

if __name__ == "__main__":
    pdfPath = os.path.join(os.getcwd(), "", "docs.pdf")
    question = "Data Preprocessing and Cleaning"

    chatBot = createChatBot(pdfPath)
    print(chatBot(question))
