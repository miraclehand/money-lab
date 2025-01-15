#!/bin/bash

USER=`whoami`
WORKING_DIR="/home/$USER/Dev/MoneyLab"
SESSION_NAMES=("database" "celery_worker" "price_collector" "disclosure_collector")
WINDOW_NAME="MoneyLab"
COMMAND="./run.sh"
TMUX_CMD="/usr/bin/tmux"

start_tmux_session() {
    local session_name=$1
    local window_name=$2
    local command=$3

    echo -e "Tmux Run $session_name" | logger -t "$session_name"

    cd "$WORKING_DIR/$session_name" || { echo "디렉토리 변경 실패: $WORKING_DIR/$session_name"; exit 1; }

    sudo -u "$USER" $TMUX_CMD new-session -s "$session_name" -d -n "$window_name"
    sudo -u "$USER" $TMUX_CMD send-keys -t "$session_name:$window_name" "$command" Enter
}

for session in "${SESSION_NAMES[@]}"; do
    start_tmux_session "$session" "$WINDOW_NAME" "$COMMAND"
done
