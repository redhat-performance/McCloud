#!/usr/bin/env bash
# tmux setup for use with Browbeat - 1 Controller / 6 Computes
SESSION='browbeat'
ssh_config_home='/home/stack/browbeat/ansible'
compute_name='overcloud-compute'

tmux -2 new-session -d -s $SESSION -n 'undercloud-root'

# Stack user window (sourced stackrc)
tmux new-window -t $SESSION:1 -n 'undercloud-stack'
tmux send-keys "su - stack" C-m
tmux send-keys ". stackrc" C-m

# Stack user window (sourced overcloudrc)
tmux new-window -t $SESSION:2 -n 'undercloud-overcloud'
tmux send-keys "su - stack" C-m
tmux send-keys ". overcloudrc" C-m

# Single Pane Browbeat
tmux new-window -t $SESSIION:3 -n 'browbeat'
tmux send-keys "su - stack" C-m
tmux send-keys "cd browbeat; . .browbeat-venv/bin/activate" C-m
tmux split-window -v
tmux select-pane -t 1
tmux send-keys "su - stack" C-m
tmux send-keys "cd browbeat/log" C-m
tmux send-keys "touch debug.log; tailf debug.log" C-m
tmux select-pane -t 0

# Single Pane Controller
tmux new-window -t $SESSIION:4 -n 'controller'
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config overcloud-controller-0" C-m
tmux send-keys "sudo su -" C-m
tmux select-pane -t 0

# Single Pane Computes
tmux new-window -t $SESSIION:5 -n 'Computes0-3'
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config ${compute_name}-0" C-m
tmux send-keys "sudo su -" C-m
tmux split-window -v
tmux select-pane -t 0
tmux split-window -h
tmux select-pane -t 1
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config ${compute_name}-1" C-m
tmux send-keys "sudo su -" C-m
tmux select-pane -t 2
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config ${compute_name}-2" C-m
tmux send-keys "sudo su -" C-m
tmux split-window -h
tmux select-pane -t 3
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config ${compute_name}-3" C-m
tmux send-keys "sudo su -" C-m
tmux select-pane -t 0

# Single Pane Computes4-5
tmux new-window -t $SESSIION:6 -n 'computes4-5'
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config ${compute_name}-4" C-m
tmux send-keys "sudo su -" C-m
tmux split-window -v
tmux select-pane -t 1
tmux send-keys "su - stack" C-m
tmux send-keys "cd ${ssh_config_home}" C-m
tmux send-keys "ssh -F ssh-config ${compute_name}-5" C-m
tmux send-keys "sudo su -" C-m
tmux select-pane -t 0

tmux select-window -t $SESSION:2

tmux -2 attach-session -t $SESSION
