from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain import hub

# Initialize database and LLM
db = SQLDatabase.from_uri("sqlite:///main.db")
llm = ChatOpenAI(model="gpt-4", temperature=0)

# def tableList():
#     table_names = db.get_usable_table_names()
#     table_info = {}    
#     for name in table_names:
#         query = f"PRAGMA table_info('{name}')"
#         print(name + " - " + db.run(query))
# tableList()

# Create prompt template
prompt = ChatPromptTemplate.from_template("""
    You are an expert SQL query generator.
    Based on the following user request, generate an efficient and syntactically correct SQL query:
    "{user_request}"

    Instructions:
    - Return **only** the SQL query — do not include explanations.
    - Ensure proper use of SQL clauses such as WHERE, JOIN, GROUP BY, ORDER BY when applicable.
    - Use standard SQL syntax (PostgreSQL/MySQL compatible).
    - Ensure table and column names are referenced correctly based on the schema.
""")

# Create the SQL chain
chain = create_sql_query_chain(llm, db)

# Execute the chain
user_request = "fetch first 5 item from album table and also fetch Artist information at the basis of ArtistId"

response = chain.invoke({
    "question": user_request,
})

print("Generated SQL:\n", response)

# If you want to execute the generated query
result = db.run(response)
print("\nQuery Result:", result)
