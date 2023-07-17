# Make sure to set token before running this: export token=""

# curl -X POST http://api.qa.spiritualdata.org/chat/response \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer $token"\
# -d '{"message":"Is there evidence that we can communicate through telepathy while in our physical bodies?", "chat_id": "", "return_results": false, "answer_model":"gpt-3.5-turbo"}'


# Save the response in a variable
response=$(curl -X POST http://localhost:8000/chat/response \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $token" \
-d '{"message":"Is there evidence that we can communicate through telepathy while in our physical bodies?", "chat_id": "", "return_results": false, "answer_model":"gpt-3.5-turbo", "save": true}'
)

# Extract the chat_id from the response
chat_id=$(echo $response | jq -r '.chat_id')

echo "Chat ID: $chat_id"

# Use the chat_id in /chat/get request
curl -X GET "http://localhost:8000/chat/get?chat_id=$chat_id" \
-H "Authorization: Bearer $token"\

# Use the chat_id in /chat/delete request
curl -X DELETE "http://localhost:8000/chat/delete?chat_id=$chat_id" \
-H "Authorization: Bearer $token"\
