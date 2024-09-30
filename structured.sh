# Basic example
curl -X POST "http://localhost:8000/structured" \
     -H "Content-Type: application/json" \
     -d '{
        "custom_schema": {
          "name": "str",
          "age": "int",
          "is_student": "bool"
        },
        "prompt": "This is where we talk about John who is 25 years old and is not a student, but he likes pizza."
      }'

curl -X POST "http://localhost:8000/structured" \
     -H "Content-Type: application/json" \
     -d '{
          "custom_schema": {
            "name": "str",
            "age": "int"
          },
          "prompt": "John Doe is thirty-five years old."
        }'

# Nested
curl -X POST "http://localhost:8000/structured" -H "Content-Type: application/json" \
     -d '{
            "custom_schema": {
              "person": {
                "name": "str",
                "age": "int"
              },
              "occupation": {
                "job_title": "str",
                "company": "str"
              }
            },
            "prompt": "Alice, 30, works as a software engineer at TechCorp."
          }'


# Lists
curl -X POST "http://localhost:8000/structured" \
     -H "Content-Type: application/json" \
     -d '{
  "custom_schema": {
    "fruits": "List[str]",
    "quantities": "List[int]"
  },
  "prompt": "I need to buy 3 apples, 2 bananas, and 5 oranges."
}'

# Enums
curl -X POST "http://localhost:8000/structured" \
     -H "Content-Type: application/json" \
     -d '{
  "custom_schema": {
    "day_of_week": "Literal[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Sunday\"]",
    "mood": "Literal[\"happy\", \"sad\", \"excited\", \"tired\"]"
  },
  "prompt": "It'\''s Wednesday and I'\''m feeling excited about the upcoming weekend."
}'

# Optional
curl -X POST "http://localhost:8000/structured" \
     -H "Content-Type: application/json" \
     -d '{
  "custom_schema": {
    "name": "str",
    "age": "int",
    "email": "Optional[str]",
    "phone": "Optional[str]"
  },
  "prompt": "Contact info: Bob Smith, 42 years old, email is bob@example.com"
}'

# Date/time
curl -X POST "http://localhost:8000/structured" \
     -H "Content-Type: application/json" \
     -d '{
          "custom_schema": {
            "event_date": "date",
            "start_time": "time",
            "duration_minutes": "int"
          },
          "prompt": "The meeting is scheduled for March 15, 2024 at 2:30 PM and will last for 90 minutes."
        }'
