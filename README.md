# deploy-microcloud

Ansible files to deploy a Tripleo Undercloud and Overcloud on the Microcloud System.

Completes:
* Tripleo Undercloud Install
* Node Introspection
* Node pinning based on overcloud deployment scenario
* Overcloud deployment based on scenario
* Browbeat Deployment
* Opens "Install" tmux session and deploys each scenario tmux script

Usage:

```
$ cp hosts hosts.local
$ # Add Microcloud to hosts.local
$ cp vars/main.yaml vars/main.local.yaml
$ # Edit vars/main.local.yml to adjust deployment parameters
$ ansible-playbook -i hosts.local deploy.yaml
```
