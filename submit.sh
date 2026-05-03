#!/bin/bash

API_URL="https://utnxbioqt0.execute-api.us-east-1.amazonaws.com/prod/submit"

echo "Submitting scenario..."

RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo_user",
    "scenario": "amazon_v1",
    "submission_data": {
      "tasks_completed": true,
      "notes": "Initial VM submission test"
    }
  }')

echo "Raw response:"
echo $RESPONSE

echo ""
echo "Parsed feedback:"
echo $RESPONSE | jq -r '.body' | jq
