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

function upload_file()
{
        local vm_name=$1
        local local_path=$2
        local remote_path=$3

        /bin/bash /usr/local/bin/upload_file.sh "$vm_name" "$remote_path" "$local_path"
}

function run_powershell_script()
{
        local vm_name=$1
        local local_path=$2
        local remote_path=$3
        local args=$4
        args='"arg":["-ExecutionPolicy", "ByPass", "-File", "'$remote_path'", '$args'], "capture-output": true'
        upload_file "$vm_name" "$local_path" "$remote_path" \
                && exec_command "$vm_name" "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe" "$args"
}

function ps_script_log()
{
        local vm_name=$1
        local log_path=$2
        /bin/bash $scriptdir/download_file.sh "$vm_name" "$log_path" | sed -n '/SerializationVersion/,/Windows PowerShell transcript end/{//b;p}'
}

function agent_run_script()
{
        local ps_script=$1
        local args=$2
        local timeout=$3
        local pid=$(run_powershell_script "$name" "$resource_path/$ps_script" "$working_dir/$ps_script" "$args")
        local exitcode=$(get_exitcode "$name" "$pid" $timeout)
        #if [ "$exitcode" != "" ] && [ exitcode -gt 0 ]; then
        #       ps_script_log "$name" "$working_dir/$ps_script.log"
        #fi
        echo "$exitcode"
        [ "$exitcode" == 0 ]
}

vm_name=$1

run_powershell_script "$vm_name" /scripts/pkmsvc/PKM_PrepareDisk.ps1 "c:/temp/PKM_PrepareDisk.ps1" '"arg"'
