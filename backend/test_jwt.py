from app.auth.jwt_handler import create_access_token, verify_access_token

data = {
    "sub": "abhishek@gmail.com"
}

token = create_access_token(data)

print("Generated Token:")
print(token)

payload = verify_access_token(token)

print("\nDecoded Payload:")
print(payload)