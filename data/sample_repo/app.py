from auth import login_user
from database import get_database_connection


def main():
    print("Welcome to the sample application.")

    connection = get_database_connection()

    if connection:
        print("Database connection successful.")

    username = input("Enter username: ")
    password = input("Enter password: ")

    result = login_user(username, password)

    print(result)


if __name__ == "__main__":
    main()