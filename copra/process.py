import pandas as pd
from tqdm import tqdm
from utils.cls_hl7 import HL7MSG

def process_hl7_to_csv(input_file="hl7_messages.txt"):
    with open(input_file, "r", encoding="ISO-8859-1") as f:
        msgs = f.read().split('\n')

    df_nm_all = []
    for msg_raw in tqdm(msgs):
        if msg_raw.strip() == "": continue
        try:
            msg = HL7MSG(msg_raw)
            df_nm = msg.export_measurement_df(tmsg='OBX', tdata='NM')
            df_nm_all.append(df_nm)
        except Exception as e:
            print(f"Error processing message: {msg_raw[:50]}... Error: {e}")

    if df_nm_all:
        df_ = pd.concat(df_nm_all)
        output_csv = input_file.replace('.txt', '.csv')
        df_.to_csv(output_csv, index=False)
        print(f"Data saved to {output_csv}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    process_hl7_to_csv()
