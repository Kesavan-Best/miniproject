import os

# Generate a secure secret key
secret_key = os.urandom(24).hex()
print("Your secret key is:", secret_key)