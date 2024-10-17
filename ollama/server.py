from fastapi import FastAPI
from langserve import add_routes
# from chain_test import chain as myChain
from chain import chain as myChain
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class InputChat(BaseModel): 
    messages1: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

app = FastAPI()

# Edit this to add the chain you want to add
add_routes(
    app,
    myChain.with_types(input_type=InputChat),
    path="/ollama",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9999)


