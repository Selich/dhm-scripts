import socket
import csv
import os
import time

def reformat_message_to_csv(message):
    components = message.split(',')
    return components


def listen_and_save(port=18022, output_file="hl7_messages.csv"):
    host = 'localhost'
    buffer_size = 1024
    file_exists = os.path.isfile(output_file)
    with open(output_file, "a", encoding="ISO-8859-1", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Column1", "Column2", "Column3"])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            s.listen()
            print(f"Listening on port {port}...")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(buffer_size)
                        if not data:
                            break
                        message = data.decode("ISO-8859-1")
                        csv_data = reformat_message_to_csv(message)
                        with open(output_file, "a", encoding="ISO-8859-1", newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(csv_data)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # listen_and_save()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 18022))
    while True:
        data = client_socket.recv(512)
        message = data.decode("ISO-8859-1")
        csv_data = reformat_message_to_csv(message)
        output_file="hl7_messages.csv"
        with open(output_file, "a", encoding="ISO-8859-1", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_data)

        print("RECEIVED: %s" % data)
