import re
import pandas as pd

def parse_hl7_to_csv(input_text, output_csv):
    # Define a regex pattern to extract HL7 segments
    pattern = re.compile(r"(?P<segment>[A-Z]{3})\|(?P<fields>.*?)\r")
    matches = pattern.findall(input_text)
    
    # Create a list to hold the parsed data
    data = []
    
    # Iterate over the matches and parse the segments and fields
    for match in matches:
        segment = match[0]
        fields = match[1].split('|')
        data.append([segment] + fields)
    
    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False, header=False)
    print(f"Data saved to {output_csv}")

# Example input HL7 text from the image
hl7_text = """
MSH|^~\&|CINDI|CCZPAS7I|COPRA6|20240524140710||ORU^R01|ORU_R01|20240524140710335134|P|2.7||||||8859/1
PV1||^1
OBR||1|cindi^device data^L|20240524140710
OBX|1|ST|^CINDI_HOSTNAME|DHM-COPRAB-012.dhmdom.intern.dhm.mhn.de||||||O
OBX|1|ST|^CINDI_PLUG_URI||cindi://dhm-coprab-012.dhmdom.intern.dhm.mhn.de/box/CC6GZVHW/plug/CCZPAS7I||||||O
OBX|1|ST|^CINDI_PLUGID||CCZPAS7I||||||O
OBX|1|ST|^CINDI_BOXID||CC6GZVHW||||||O
OBX|1|ST|^CINDI_MEDICALDEVICEID||ICP-GE3Z-0001||||||O
OBX|1|ST|^CINDI_MANUFACTURER_NAME||GE Healthcare||||||O
OBX|1|ST|^CINDI_PRODUCT_NAME||Carescape Monitor B650||||||O
OBX|1|ST|^CINDI_DRIVERPACKETID||83b8efe60-c41-47a8-a01f-e1593d175c53||||||O
OBX|1|NM|^CO_Vital_HF||61|/min||||R
OBX|1|NM|^CO_Vital_AF||121|/min||||R
OBX|1|NM|^NBP_sys||106|mmHg||||R|20240524140005
OBX|1|NM|^NBP_mean||77|mmHg||||R|20240524140005
OBX|1|NM|^NBP_dia||58|mmHg||||R|20240524140005
OBX|1|ST|^CINDI_PLUG_URI||cindi://dhm-coprab-012.dhmdom.intern.dhm.mhn.de/box/CC6GZVHW/plug/CCZPAS7I||||||O
OBX|1|ST|^CINDI_BOXID||CC6GZVHW||||||O
OBX|1|ST|^CINDI_MEDICALDEVICEID||ICP-GE3Z-0001||||||O
OBX|1|ST|^CINDI_MANUFACTURER_NAME||GE Healthcare||||||O
OBX|1|ST|^CINDI_PRODUCT_NAME||Carescape Monitor B650||||||O
OBX|1|ST|^CINDI_DRIVERPACKETID||fe2d436e-719a-4afb-bf1b-d40b8e0b0163||||||O
OBX|1|NM|^CO_Vital_HF||61|/min||||R
OBX|1|NM|^CO_Vital_AF||131|/min||||R
OBX|1|NM|^NBP_sys||106|mmHg||||R|20240524140005
OBX|1|NM|^NBP_mean||77|mmHg||||R|20240524140005
OBX|1|NM|^NBP_dia||58|mmHg||||R|20240524140005
OBX|1|NM|^CO_Vital_SpO2||95|%||||R
OBX|1|NM|^ART_sys||141|mmHg||||R|20240524140005
OBX|1|NM|^ART_dia||56|mmHg||||R|20240524140005
OBX|1|NM|^CO_Vital_P||69|mmHg||||R
OBX|1|NM|^CO_Vital_ZVP||16|mmHg||||R
"""

# Specify the output CSV file
output_csv = "hl7_messages.csv"

# Call the function to parse HL7 text and save to CSV
parse_hl7_to_csv(hl7_text, output_csv)