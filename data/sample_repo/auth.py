def login_user(username, password):
    """
    Simulate a basic login process.

    This function is for demonstrating code search only.
    It does not implement real authentication.
    """

    if not username or not password:
        return "Username and password are required."

    if username == "admin" and password == "admin123":
        return "Login successful."

    return "Invalid credentials."


def logout_user(username):
    """
    Simulate logging out a user.
    """

    return f"User {username} logged out."