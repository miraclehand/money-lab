#!/bin/bash

echo -e "Tmux Run database" | logger -t database

user=`whoami`

cd /home/$user/Dev/MoneyLab/database
sudo -u $user /usr/bin/tmux new-session -s "database" -d -n "MoneyLab"
sudo -u $user /usr/bin/tmux send-keys -t "database:MoneyLab" './run.sh' Enter

cd -

echo -e "Tmux Run price-collector" | logger -t price-collector

cd /home/$user/Dev/MoneyLab/price-collector
sudo -u $user /usr/bin/tmux new-session -s "price-collector" -d -n "MoneyLab"
sudo -u $user /usr/bin/tmux send-keys -t "price-collector:MoneyLab" './run.sh' Enter

cd -

echo -e "Tmux Run disclosure-collector" | logger -t disclosure-collector

cd /home/$user/Dev/MoneyLab/disclosure-collector
sudo -u $user /usr/bin/tmux new-session -s "disclosure-collector" -d -n "MoneyLab"
sudo -u $user /usr/bin/tmux send-keys -t "disclosure-collector:MoneyLab" './run.sh' Enter


