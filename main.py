from data.response import get_response

while True:
    text = str(input("Input:"))
    if text.lower() != "exit":
        print("Response:",get_response(text))
    else:
        print("Response: Exiting...")
        break