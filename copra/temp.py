import pandas as pd

def parse_hl7_message(hl7_message):
    lines = hl7_message.strip().split('\n')
    data = {}
    for line in lines:
        segments = line.split('|')
        if line.startswith("MSH"):
            data["MSH_Encoding_Characters"] = segments[1]
            data["MSH_Sending_Application"] = segments[2]
            data["MSH_Sending_Facility"] = segments[3]
            data["MSH_Receiving_Application"] = segments[4]
            data["MSH_Receiving_Facility"] = segments[5]
            data["MSH_DateTime_Of_Message"] = segments[6]
            data["MSH_Security"] = segments[7]
            data["MSH_Message_Type"] = segments[8]
            data["MSH_Message_Control_ID"] = segments[9]
            data["MSH_Processing_ID"] = segments[10]
            data["MSH_Version_ID"] = segments[11]
            data["MSH_Character_Set"] = segments[17]
        elif line.startswith("PV1"):
            data["PV1"] = line
        elif line.startswith("OBR"):
            data["OBR"] = line
        elif line.startswith("OBX"):
            key = segments[3].split('^')[1]
            value = segments[5]
            if key not in data:
                data[key] = []
            data[key].append(value)
    # Flatten lists into strings for each key
    for key in data:
        if isinstance(data[key], list):
            data[key] = ', '.join(data[key])
    return data

with open('./test.csv', 'r') as file:
    hl7_message = file.read()

messages = hl7_message.split('||||||||||||||||||||||||||||||||')

all_data = []
for message in messages:
    if message.strip():
        message_data = parse_hl7_message(message)
        all_data.append(message_data)

df = pd.DataFrame(all_data)

df_carescape = df[df['CINDI_PRODUCT_NAME'] == 'Carescape Monitor B650']
df_spacecom = df[df['CINDI_PRODUCT_NAME'] == 'SpaceCom']

df_carescape.to_csv('Carescape_Monitor_B650_output.csv', index=False)
df_spacecom.to_csv('SpaceCom_output.csv', index=False)

print("Data has been successfully saved to Carescape_Monitor_B650_output.csv and SpaceCom_output.csv")
