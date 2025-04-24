#!/bin/bash

main()
{
    local pane_tcpdump=0
    local pane_client=1
    local pane_server=2

    local web_server_ip="127.0.0.1"
    local web_server_port=8888
    local web_server_dir="/home/$USER/serve"

    # ensure directory to serve exists
    if [[ ! -d "${web_server_dir}" ]]; then
        echo "No such directory: ${web_server_dir}"
        exit 1
    fi

    # export password
    if [[ -z "${PASSWORD}" ]]; then
        echo "PASSWORD is undefined"
        exit 1
    fi
    export PASSWORD ||
    {
        echo "Failed to export PASSWORD";
        exit 1;
    }

    # new session
    tmux new-session -d ||
    {
        echo "Failed to create tmux session" >&2;
        exit 1;
    }

    # create panes
    tmux split-window -v && tmux split-window -h ||
    {
        tmux kill-session;
        echo "Failed to split window" >&2;
        exit 1;
    }

    # run tcpdump
    echo "PASSWORD: $PASSWORD"
    tmux select-pane -t $pane_tcpdump -- && tmux send-keys "sudo tcpdump -i lo -X" C-m && tmux send-keys "${PASSWORD}" C-m ||
    {
        tmux kill-session;
        echo "Failed to start tcpdump";
        exit 1;
    }

    # run http server
    tmux select-pane -t $pane_server -- \
    && tmux send-keys "python3 -m http.server -d ${web_server_dir} -b ${web_server_ip} ${web_server_port}" C-m ||
    {
        tmux kill-session;
        echo "Failed to start web server";
        exit 1;
    }
    sleep 1

    # make http requests with curl
    tmux select-pane -t $pane_client -- \
    && tmux send-keys "curl --trace - http://${web_server_ip}:${web_server_port}/line.txt" C-m \
    && tmux send-keys "curl --trace - http://${web_server_ip}:${web_server_port}/lines.txt" C-m \
    && tmux send-keys "curl --trace - http://${web_server_ip}:${web_server_port}/nonexistent.txt" C-m ||
    {
        tmux kill-session;
        echo "Failed to make HTTP requests";
        exit 1;
    }

    # attach
    tmux -2 attach-session ||
    {
        tmux kill-session;
        echo "Failed to attach to tmux session";
        exit 1;
    }
}

main "$@"
