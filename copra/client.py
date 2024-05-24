# import socket
# import csv
# import os

# def reformat_message_to_csv(message):
#     components = message.split(',')
#     return components

    
# #    ncat -nklp 18002 > hl7_messages.csv

# def listen_and_save(port=18022, output_file="hl7_messages.csv"):
#     host = 'localhost'
#     buffer_size = 1024
#     file_exists = os.path.isfile(output_file)
#     with open(output_file, "a", encoding="ISO-8859-1", newline='') as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["Column1", "Column2", "Column3"])

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         try:
#             s.bind((host, port))
#             s.listen()
#             print(f"Listening on port {port}...")
#             while True:
#                 conn, addr = s.accept()
#                 with conn:
#                     print(f"Connected by {addr}")
#                     while True:
#                         data = conn.recv(buffer_size)
#                         if not data:
#                             break
#                         message = data.decode("ISO-8859-1")
#                         csv_data = reformat_message_to_csv(message)
#                         with open(output_file, "a", encoding="ISO-8859-1", newline='') as f:
#                             writer = csv.writer(f)
#                             writer.writerow(csv_data)
#         except Exception as e:
#             print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     listen_and_save()

import socket

def start_server(host='0.0.0.0', port=18022, output_file='hl7_messages.csv'):
    with open(output_file, 'a') as f:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()

            print(f"Listening on {host}:{port}...")

            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    print(f"Connection from {client_address}")
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data.decode('utf-8'))
                        f.flush()

if __name__ == "__main__":
    start_server()
