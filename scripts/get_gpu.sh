function exec_command()
{
    local vm_name=$1
    local remote_path=$2
    local args=$3
    if [ "$args" != "" ]
    then
        args=",$args"
    fi
    if ! virsh qemu-agent-command "$vm_name" '{"execute":"guest-exec","arguments" : {"path":"'"$remote_path"'"'"$args"'}}'
    then
        echo "guest-exec failed! remote_path = $remote_path" >&2
        return 1
    fi
}

function get_pid()
{
  result=$(echo "$1" | grep -Pio '(?<=pid":)[\d]+(?=})')
  if [[ "$result" ]]; then
                echo "$result"
                return 0
  else
          echo "$1"
          return 1
  fi
}

function read_output()
{
    if [[ $3 ]]; then
        local end=$(( $SECONDS + $3 ))
    fi
    while [[ ! $3 || $SECONDS -lt $end ]]; do
        local response=$(virsh qemu-agent-command "$1" '{"execute": "guest-exec-status", "arguments": { "pid": '"$2"'}}')
        local exited=$(echo "$response" | grep -Po '(?<=exited":)((true)|(false))')
        if [[ -z "$exited" ]]; then
            return 1
        fi
        if [ "$exited" == true ]; then
            echo "$response"
            return 0
        fi
        sleep 1
    done
    echo "Waiting for pid $2 on vm $1 timed out: $(( $SECONDS - $end + $3 ))" >&2
    return 1
}

function get_output()
{
    read_output "$1" $(get_pid "$2") $3 | grep -Po '(?<=out-data":").+?(?=")' | base64 -d
}
vm_name=$1
function get_gpu()
{
    local vm_name=$1
    local filter=$2
    args='"arg":["--query-gpu=gpu_name,pcie.link.gen.current,memory.total,temperature.gpu,utilization.gpu,utilization.memory,power.draw", "--format=csv,noheader,nounits"],"capture-output":true'
    res=$(exec_command "$vm_name" "C:/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe" "$args") && get_output "$vm_name" "$res" 5
}

get_gpu "$vm_name"
