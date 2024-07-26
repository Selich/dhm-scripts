#!/bin/bash

get_pi_stats() {
  local ip="$1"
  local user="$2"
  local password="$3"

  temp=$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no $user@$ip 'vcgencmd measure_temp' | grep -oP '\d+\.\d+')
  cpu_usage=$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no $user@$ip 'top -bn1 | grep "Cpu(s)"' | grep -oP '\d+\.\d+(?=% id)' | awk '{print 100 - $1}')
  
  echo "$temp,$cpu_usage"
}

get_workstation_stats() {
  temp=$(sensors | grep 'Core 0:' | awk '{print $3}' | grep -oP '\d+\.\d+')
  cpu_usage=$(top -bn1 | grep "Cpu(s)" | grep -oP '\d+\.\d+(?=% id)' | awk '{print 100 - $1}')
  
  echo "$temp,$cpu_usage"
}

csv_file="system_stats.csv"

if [ ! -f $csv_file ]; then
  echo "Timestamp,Device,Temperature (C),CPU Usage (%)" > $csv_file
fi

pi_devices=(
  "pi_ip_address pi_username pi_password"
)

while true; do
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  
  ws_stats=$(get_workstation_stats)
  echo "$timestamp,Workstation,$ws_stats" >> $csv_file
  
  for pi in "${pi_devices[@]}"; do
    IFS=' ' read -r -a pi_info <<< "$pi"
    pi_stats=$(get_pi_stats "${pi_info[0]}" "${pi_info[1]}" "${pi_info[2]}")
    echo "$timestamp,Raspberry Pi,$pi_stats" >> $csv_file
  done
  
  sleep 60
done

