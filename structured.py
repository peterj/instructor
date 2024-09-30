from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException
import instructor
from openai import OpenAI
from pydantic import BaseModel, create_model
from typing import Any, Dict, List, Literal, Optional, Union
from datetime import date, time
import re
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = instructor.from_openai(OpenAI())


class SchemaRequest(BaseModel):
    custom_schema: Dict[str, Any]
    prompt: str


def parse_type(type_str: str) -> Any:
    if type_str in ['str', 'string']:
        return str
    elif type_str in ['int', 'integer']:
        return int
    elif type_str in ['float', 'number']:
        return float
    elif type_str in ['bool', 'boolean']:
        return bool
    elif type_str == 'date':
        return date
    elif type_str == 'time':
        return time
    elif type_str.startswith('List[') or type_str.startswith('list['):
        inner_type = type_str[5:-1]
        return List[parse_type(inner_type)]
    elif type_str.startswith('Optional[') or type_str.startswith('optional['):
        inner_type = type_str[9:-1]
        return Optional[parse_type(inner_type)]
    elif type_str.startswith('Literal[') or type_str.startswith('literal['):
        literals = re.findall(r'"([^"]*)"', type_str)
        return Literal[tuple(literals)]
    else:
        raise ValueError(f"Unsupported type: {type_str}")


def create_dynamic_model(schema: Dict[str, Any]):
    field_definitions = {}
    for field_name, field_type in schema.items():
        if isinstance(field_type, dict):
            # Nested model
            field_definitions[field_name] = (
                create_dynamic_model(field_type), ...)
        elif isinstance(field_type, str):
            try:
                parsed_type = parse_type(field_type)
                field_definitions[field_name] = (parsed_type, ...)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(
                status_code=400, detail=f"Invalid field type for {field_name}")

    return create_model("DynamicModel", **field_definitions)


@app.post("/structured")
async def process_with_schema(request: SchemaRequest):
    try:
        DynamicModel = create_dynamic_model(request.custom_schema)
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=DynamicModel,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )

        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
