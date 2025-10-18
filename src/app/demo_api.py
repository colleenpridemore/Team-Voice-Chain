from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from src.client.asi_client import call_model, ASIClientError

app = FastAPI(title="ASI1-mini Demo API")

class InferenceRequest(BaseModel):
    input: Any

class InferenceResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/infer", response_model=InferenceResponse)
def infer(req: InferenceRequest):
    try:
        result = call_model(req.input)
    except ASIClientError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    # Wrap result in consistent structure; adapt to actual model response shape
    return InferenceResponse(output={"model_response": result})
