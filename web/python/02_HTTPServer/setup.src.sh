# >>> setup.src.sh >>>

# --- ENSURE WEB SERVER CONFIG IS PRESENT ---

# sourced from tmux
if [[ -n "${TMUX}" ]]; then
    if [[ -z "${WEB_SERVER_IP}" ]]; then
        echo "WEB_SERVER_IP is undefined" >&2
        exit 1
    fi

    if [[ -z "${WEB_SERVER_PORT}" ]]; then
        echo "WEB_SERVER_PORT is undefined" >&2
        exit 1
    fi

    if [[ -z "${WEB_SERVER_DIR}" ]]; then
        echo "WEB_SERVER_DIR is undefined" >&2
        exit 1
    fi

# not sourced from tmux
else
    # relative to the script sourcing
    source ../web.env ||
    {
        echo "Failed to source ../web.env" >&2;
        exit 1;
    }
fi

# <<< setup.src.sh <<<
