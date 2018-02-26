deploy-microcloud
=================

Ansible files to deploy a Tripleo Undercloud and Overcloud on the
Microcloud System.

Completes:

* Tripleo Undercloud Install
* Node Introspection
* Node pinning based on overcloud deployment scenario
* Overcloud deployment based on scenario
* Browbeat Deployment
* Opens “Install” tmux session and deploys each scenario tmux script
* Shaker / Browbeat Workloads pre-installed
* 8 deployment scenarios supported across 3 different major versions of OpenStack

Initial Deployment Usage:

::

    $ cp hosts hosts.local
    $ # Add Microcloud to hosts.local
    $ cp vars/main.yaml vars/main.local.yaml
    $ # Edit vars/main.local.yml to adjust deployment parameters
    $ ansible-playbook -i hosts.local deploy.yaml

Redeployment Usage:

::

    $ # Edit vars/main.local.yml to adjust deployment parameters
    $ ansible-playbook -i hosts.local redeploy.yaml

=  =================================================  ======  =====  ====  ======
Deployments vs OpenStack Versions
---------------------------------------------------------------------------------
#  deployment scenario                                Newton  Ocata  Pike  Queens
=  =================================================  ======  =====  ====  ======
0  1 Controller / 6 Computes                          Yes     Yes    Yes   No
1  3 Controllers / 4 Computes                         Yes     Yes    Yes   No
2  1 Controller / 3 CephStorage Nodes / 3 Computes    Yes     Yes    Yes   No
3  3 Controllers / 3 CephStorage Nodes / 1 Compute    Yes     Yes    Yes   No
4  1 Controller / 3 ObjectStorage Nodes / 3 Computes  Yes     Yes    Yes   No
5  1 Controller / 3 BlockStorage Nodes / 3 Computes   Yes     Yes    Yes   No
6  1 Controller / 1 Networker / 5 Computes            No      No     Yes   No
7  3 Controllers / 1 Networker / 3 Computes           No      No     Yes   No
=  =================================================  ======  =====  ====  ======
