import socket
import csv

def start_server(host='0.0.0.0', port=18022, output_file='hl7_messages.csv'):
    # Define the columns
    columns = [
        "Segment", "Field1", "Field2", "Field3", "Field4", "Field5", "Field6", "Field7", "Field8", "Field9", "Field10",
        "Field11", "Field12", "Field13", "Field14", "Field15", "Field16", "SetID", "ValueType", "ObservationIdentifier",
        "ObservationSubID", "ObservationValue", "Units", "ReferencesRange", "AbnormalFlags", "Probability",
        "NatureOfAbnormalTest", "ObservationResultStatus", "DateLastObservationNormalValue", "UserDefinedAccessChecks",
        "DateTimeOfTheObservation", "ProducerID", "ResponsibleObserver", "ObservationMethod"
    ]
    
    with open(output_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='|')
        
        # Write the header
        csv_writer.writerow(columns)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()
            
            print(f"Listening on {host}:{port}...")
            
            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    print(f"Connection from {client_address}")
                    buffer = ""
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        buffer += data.decode('ISO-8859-1')
                        if "\r" in buffer:
                            lines = buffer.split("\r")
                            for line in lines[:-1]:
                                if line:
                                    fields = line.split('|')
                                    segment = fields[0]
                                    row = [segment] + fields[1:] + [''] * (len(columns) - len(fields) - 1)
                                    csv_writer.writerow(row)
                                    csvfile.flush()
                            buffer = lines[-1]

if __name__ == "__main__":
    start_server()
