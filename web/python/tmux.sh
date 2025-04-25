#!/bin/bash

source conf.src.sh ||
{
    echo "Failed to source conf.src.sh" >&2;
    exit 1;
}

main()
{
    local pane_tcpdump=0
    local pane_client=1
    local pane_server=2

    # ensure directory to serve exists
    if [[ ! -d "${WEB_SERVER_DIR}" ]]; then
        echo "No such directory: ${WEB_SERVER_DIR}" >&2
        exit 1
    fi

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
	
	# export web server info
	export WEB_SERVER_IP ||
	{
		echo "Failed to export WEB_SERVER_IP" >&2;
		exit 1;
	}
	export WEB_SERVER_PORT ||
	{
		echo "Failed to export WEB_SERVER_PORT">&2;
		exit 1;
	}
	export WEB_SERVER_DIR ||
	{
		echo "Failed to export WEB_SERVER_DIR">&2;
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
    tmux select-pane -t $pane_tcpdump -- && tmux send-keys "sudo tcpdump -i lo -X" C-m && tmux send-keys "${PASSWORD}" C-m ||
    {
        tmux kill-session;
        echo "Failed to start tcpdump" >&2;
        exit 1;
    }

    # run http server
    tmux select-pane -t $pane_server -- \
    && tmux send-keys "./start_server.sh" C-m ||
    {
        tmux kill-session;
        echo "Failed to start web server" >&2;
        exit 1;
    }
    sleep 1

	# select client pane
	tmux select-pane -t $pane_client ||
	{
		tmux kill-session;
		echo "Failed to select client pane" >&2;
		exit ;
	}

    # attach
    tmux -2 attach-session ||
    {
        tmux kill-session;
        echo "Failed to attach to tmux session" >&2;
        exit 1;
    }
}

main "$@"

