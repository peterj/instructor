# Instructor examples

Instructor: https://python.useinstructor.com/

1. Create a `.env` file with `OPENAI_API_KEY` variable set.
2. Run `pip install -r requirements.txt` to install the required packages.

## Structured outputs (`structured.py`)

Implements an endpoint that returns a structured output based on the input schema and prompt. Run the code with `python structured.py` and then use the sample requests from `structured.sh` file.

Example request:

```json
{
  "custom_schema": {
    "name": "str",
    "age": "int",
    "is_student": "bool"
  },
  "prompt": "Extract information about John who is 25 years old and is not a student."
}
```

Returns:

```json
{
    "name": "John",
    "age": 25,
    "is_student": false
}
```

## Classification (`classify.py`)

Implements an endpoint that classifies the input text into one or more of the provided tags. Tags are provided with insturctions. The output also contains the confidence score for each classification. Run the code with `python classify.py` and then use the sample requests from `classify.sh` file.

Example input:

```json
{
  "texts": [
    "What is your phone number?",
    "Please send the documents to john@example.com",
    "I live at 123 Main St, Anytown, USA"
  ],
  "tags": [
    {"id": 0, "name": "personal", "instructions": "Personal information"},
    {"id": 1, "name": "phone", "instructions": "Phone number"},
    {"id": 2, "name": "email", "instructions": "Email address"},
    {"id": 3, "name": "address", "instructions": "Address"},
    {"id": 4, "name": "other", "instructions": "Other information"}
  ],
  "multi_label": false
}
```

Example output:

```json
{
  "texts": ["What is your phone number?", "Please send the documents to john@example.com", "I live at 123 Main St, Anytown, USA"],
  "predictions": [[{ "id": 1, "name": "phone", "confidence": 0.95 }], [{ "id": 2, "name": "email", "confidence": 0.98 }], [{ "id": 3, "name": "address", "confidence": 0.95 }]]
}
```
