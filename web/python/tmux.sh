#!/bin/bash

main()
{
    local pane_tcpdump=0
    local pane_client=1
    local pane_server=2

    # export password
    if [[ -z "${PASSWORD}" ]]; then
        echo "PASSWORD is undefined" >&2
        exit 1
    fi
    export PASSWORD ||
    {
        echo "Failed to export PASSWORD" >&2;
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
	
    # source bashrc
    local bashrc="/home/${USER}/.bashrc"
    tmux select-pane -t $pane_tcpdump && tmux send-keys "source ${bashrc}" C-m \
        && tmux select-pane -t $pane_client && tmux send-keys "source ${bashrc}" C-m \
        && tmux select-pane -t $pane_server && tmux send-keys "source ${bashrc}" C-m ||
    {
        tmux kill-session;
        echo "Failed to source ${bashrc}";
        exit 1;
    }

    # run tcpdump
    echo "PASSWORD: $PASSWORD"
    tmux select-pane -t $pane_tcpdump -- \
        && tmux send-keys "sudo tcpdump -i lo -X" C-m \
        && tmux send-keys "${PASSWORD}" C-m ||
    {
        tmux kill-session;
        echo "Failed to start tcpdump" >&2;
        exit 1;
    }

    # run http server
    tmux select-pane -t $pane_server -- \
        && tmux send-keys "cd ./server/docker/" C-m \
        && tmux send-keys "./.docker-compose-up.sh" C-m ||
    {
        tmux kill-session;
        echo "Failed to start web server" >&2;
        exit 1;
    }
    sleep 1

    # select client pane
    tmux select-pane -t $pane_client -- \
        && tmux send-keys "cd client" C-m \
        && tmux send-keys "ls" C-m ||
    {
        tmux kill-session;
        echo "Failed to list client scripts" >&2;
        exit 1;
    }

    # attach
    tmux -2 attach-session ||
    {
        tmux kill-session;
        echo "Failed to attach to tmux session" >&2;
        exit 1;
    }
}

set -a
source web.env ||
{
    echo "Failed to source web.env" >&2;
    exit 1;
}
set +a

main "$@"

