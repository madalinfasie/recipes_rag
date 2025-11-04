import fastapi
from services import llm
from pydantic import BaseModel

app = fastapi.FastAPI()


class Query(BaseModel):
    question: str


@app.post("/query")
async def query(query: Query):
    answer = llm.ask(query.question)
    return {"answer": answer}
