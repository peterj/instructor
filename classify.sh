
# Single-label (each text has only one label)
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{
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
}'


# Multi-label classification (each text can have multiple labels)
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{
        "texts": [
            "My email is jane@example.com and my phone number is 555-1234",
            "The meeting is at 123 Business Ave, don'\''t forget to bring your ID",
            "For privacy concerns, contact privacy@company.com or call our hotline"
        ],
        "tags": [
            {"id": 0, "name": "personal", "instructions": "Personal information"},
            {"id": 1, "name": "phone", "instructions": "Phone number"},
            {"id": 2, "name": "email", "instructions": "Email address"},
            {"id": 3, "name": "address", "instructions": "Address"},
            {"id": 4, "name": "other", "instructions": "Other information"}
        ],
        "multi_label": true
    }'

