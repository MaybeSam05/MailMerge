from dotenv import load_dotenv
import os

load_dotenv()

emailKey = os.getenv("GMAIL_KEY")

def main():
    platform = "Mac" # Dropdown with Mac and Windows

    if platform == "Mac":
        Mac()
    else:
        Windows()

def Mac():
    print("hi")

def Windows():
    print("Hi")


if __name__ == "__main__":
    main()