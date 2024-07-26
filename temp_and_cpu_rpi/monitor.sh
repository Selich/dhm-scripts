#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <Raspberry Pi IP> <Username> <Password>"
    exit 1
fi

PI_IP="$1"
PI_USER="$2"
PI_PASS="$3"

# Function to get Raspberry Pi stats
get_pi_stats() {
  local ip="$1"
  local user="$2"
  local password="$3"

  temp=$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no $user@$ip 'vcgencmd measure_temp' | grep -oP '\d+\.\d+')
  cpu_usage=$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no $user@$ip 'top -bn1 | grep "Cpu(s)"' | grep -oP '\d+\.\d+(?=% id)' | awk '{print 100 - $1}')
  
  echo "$temp,$cpu_usage"
}

# Function to get workstation stats
get_workstation_stats() {
  temp=$(sensors | grep 'Core 0:' | awk '{print $3}' | grep -oP '\d+\.\d+')
  cpu_usage=$(top -bn1 | grep "Cpu(s)" | grep -oP '\d+\.\d+(?=% id)' | awk '{print 100 - $1}')
  
  echo "$temp,$cpu_usage"
}

# CSV file to save data
csv_file="system_stats_$PI_IP.csv"

# Create CSV file and write header if it doesn't exist
if [ ! -f $csv_file ]; then
  echo "Timestamp,Device,Temperature (C),CPU Usage (%)" > $csv_file
fi

while true; do
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  
  # Get workstation stats
  ws_stats=$(get_workstation_stats)
  echo "$timestamp,Workstation,$ws_stats" >> $csv_file
  
  # Get stats for the Raspberry Pi
  pi_stats=$(get_pi_stats "$PI_IP" "$PI_USER" "$PI_PASS")
  echo "$timestamp,Raspberry Pi,$pi_stats" >> $csv_file
  
  # Sleep for a defined interval before collecting data again
  sleep 60
done

