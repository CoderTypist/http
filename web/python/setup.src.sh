# >>> setup.src.sh >>>

# --- ENSURE WEB SERVER CONFIG IS PRESENT ---

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
else
    source ../conf.src.sh ||
    {
        echo "Failed to source ../conf.src.sh" >&2;
        exit 1;
    }
fi

# <<< setup.src.sh <<<
