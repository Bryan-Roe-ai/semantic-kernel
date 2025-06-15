#!/bin/bash
# Quick API endpoint test script

BASE_URL="http://localhost:8007"
echo "🔍 Testing AI Workspace API Endpoints"
echo "======================================"

# Test health endpoints
echo "✅ Testing health endpoints:"
curl -s -w "  /health: %{http_code}\n" -o /dev/null "$BASE_URL/health"
curl -s -w "  /api/health: %{http_code}\n" -o /dev/null "$BASE_URL/api/health"

# Test model endpoints
echo "✅ Testing model endpoints:"
curl -s -w "  /api/models: %{http_code}\n" -o /dev/null "$BASE_URL/api/models"
curl -s -w "  /api/models/gpt2: %{http_code}\n" -o /dev/null "$BASE_URL/api/models/gpt2"

# Test training endpoints
echo "✅ Testing training endpoints:"
curl -s -w "  /api/training: %{http_code}\n" -o /dev/null "$BASE_URL/api/training"
curl -s -w "  /api/training/status: %{http_code}\n" -o /dev/null "$BASE_URL/api/training/status"

# Test static files
echo "✅ Testing static files:"
curl -s -w "  /static/custom-llm-studio.html: %{http_code}\n" -o /dev/null "$BASE_URL/static/custom-llm-studio.html"
curl -s -w "  /docs: %{http_code}\n" -o /dev/null "$BASE_URL/docs"

# Test POST endpoints
echo "✅ Testing POST endpoints:"
curl -s -w "  POST /api/chat: %{http_code}\n" -o /dev/null \
  -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

curl -s -w "  POST /api/generate: %{http_code}\n" -o /dev/null \
  -X POST "$BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

echo ""
echo "🎉 API endpoint testing complete!"
echo "All 200 responses indicate working endpoints."
