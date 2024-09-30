
import asyncio
from typing import List
from pydantic import BaseModel, Field, ValidationInfo, model_validator
import instructor
from openai import AsyncOpenAI
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

client = instructor.from_openai(AsyncOpenAI())

class Tag(BaseModel):
    id: int
    name: str

    @model_validator(mode="after")
    def validate_ids(self, info: ValidationInfo):
        context = info.context
        if context:
            tags: List[Tag] = context.get("tags")
            assert self.id in {tag.id for tag in tags}, f"Tag ID {self.id} not found in context"
            assert self.name in {tag.name for tag in tags}, f"Tag name {self.name} not found in context"
        return self

class TagWithInstructions(Tag):
    instructions: str

class TagWithConfidence(Tag):
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="The confidence of the prediction, 0 is low, 1 is high",
    )

class ClassificationRequest(BaseModel):
    texts: List[str]
    tags: List[TagWithInstructions]
    multi_label: bool = False

class ClassificationResponse(BaseModel):
    texts: List[str]
    predictions: List[List[TagWithConfidence]]

async def classify_single_text(text: str, tags: List[TagWithInstructions], multi_label: bool) -> List[TagWithConfidence]:
    allowed_tags_str = ", ".join([f"`{tag.id}: {tag.name}`" for tag in tags])

    response_model = List[TagWithConfidence] if multi_label else TagWithConfidence

    result = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class text classification system.",
            },
            {
                "role": "user",
                "content": f"Classify the following text: `{text}`"
            },
            {
                "role": "user",
                "content": f"Allowed tags: {allowed_tags_str}",
            },
            {
                "role": "user",
                "content": "Provide confidence scores for each prediction.",
            },
        ],
        response_model=response_model,
        validation_context={"tags": tags},
    )

    return [result] if not multi_label else result

app = FastAPI()

@app.post("/classify", response_model=ClassificationResponse)
async def classify(request: ClassificationRequest) -> ClassificationResponse:
    predictions = await asyncio.gather(
        *[classify_single_text(text, request.tags, request.multi_label) for text in request.texts]
    )
    return ClassificationResponse(
        texts=request.texts,
        predictions=predictions,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
