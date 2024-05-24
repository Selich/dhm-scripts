import socket
import time

def send_messages(port=18022, messages=None):
    if messages is None:
        messages = ["msg1,part2,part3", "msg2,part2,part3"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(('localhost', port))
            for message in messages:
                s.sendall(message.encode("ISO-8859-1"))
                print(f"Sent: {message}")
                time.sleep(1)  # Simulate delay between messages
        except Exception as e:
            print(f"An error occurred while sending messages: {e}")

if __name__ == "__main__":
    send_messages()
