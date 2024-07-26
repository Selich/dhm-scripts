import paramiko
import psutil
import time
import csv
from datetime import datetime

def get_pi_stats(ip, user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password)
    
    stdin, stdout, stderr = ssh.exec_command("vcgencmd measure_temp")
    temp = stdout.read().decode().strip().split('=')[1].split('\'')[0]
    
    stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)'")
    cpu_usage = stdout.read().decode().strip().split(',')[0].split('%')[0].split()[-1]
    
    ssh.close()
    
    return float(temp), float(cpu_usage)

def get_workstation_stats():
    temp = psutil.sensors_temperatures()
    cpu_temp = temp['coretemp'][0].current if 'coretemp' in temp else 0.0
    
    cpu_usage = psutil.cpu_percent(interval=1)
    
    return cpu_temp, cpu_usage

csv_file = "system_stats.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Device", "Temperature (C)", "CPU Usage (%)"])

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ws_temp, ws_cpu_usage = get_workstation_stats()
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, "Workstation", ws_temp, ws_cpu_usage])
    
    pi_devices = [
        {"ip": "pi_ip_address", "user": "pi_username", "password": "pi_password"}
    ]
    
    for pi in pi_devices:
        pi_temp, pi_cpu_usage = get_pi_stats(pi['ip'], pi['user'], pi['password'])
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, "Raspberry Pi", pi_temp, pi_cpu_usage])
    
    time.sleep(60)

