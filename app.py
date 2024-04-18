





#Manage userpassword
import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def check_password(hashed_password, user_password):
    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(user_password.encode(), hashed_password)

# Example usage
password = "my_secret_password"
hashed = hash_password(password)
print("Hashed:", hashed)

# Check the password
is_correct = check_password(hashed, "my_secret_password")
print("Password correct:", is_correct)