from fastapi import FastAPI
from langserve import add_routes
from CodeLLM import CodeLLM
import os
import dotenv

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# gpt-4
# gpt-3.5-turbo
model = "gpt-3.5-turbo"

llm_process_agent = CodeLLM(model, OPENAI_API_KEY)
llm_process_chain = llm_process_agent.get_chain()

app = FastAPI(
  title="Process Description to code",
  version="1.0",
  description="A simple API that converts a process description to code for further execution",
)

add_routes(
    app,
    llm_process_chain,
    path="/llm_process",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)