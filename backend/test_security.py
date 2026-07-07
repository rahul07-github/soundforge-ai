from app.auth.security import hash_password, verify_password

password = "mypassword123"

hashed = hash_password(password)
print("Hashed Password:", hashed)
print("original:", password) 


print("Verify Correct:", verify_password(password, hashed))
print("Verify Wrong:", verify_password("wrongpassword", hashed))

