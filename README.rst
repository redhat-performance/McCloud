mccloud
=================

Ansible files to deploy a Tripleo Undercloud and Overcloud on the
Microcloud Hardware and ScaleLab Hardware.

Completes:

* Tripleo Undercloud install
* Overcloud deployment based on scenario
* Node failure tolerance (incorrect ipmi, nonresponsive ipmi, clean wait/failed)
* Node introspection
* Node pinning based on overcloud deployment scenario
* 10 deployment scenarios supported(See Matrix Below) across 4 major versions of OpenStack
* Opens “Install” tmux session and deploy scenario tmux scripts included
* Browbeat Deployment
* Rally, PerfKit, Shaker and Browbeat workloads pre-installed
* Browbeat Tooling (collectd install, Spectre/MeltDown microcode+security setting)
* Private external networking setup
* Runs Browbeat scenario post install
* Artifacts and timings for tasks
* Options can be toggled off for vanilla overcloud if needed
* Handles instackenv/ipmi invalid hardware


Initial Deployment Usage:

* Assumes pre-provisioned Baremetal machine for Undercloud (Waits until machine is ready if kicked )

::

    $ cp hosts hosts.local
    $ # Add Undercloud host to hosts.local
    $ cp vars/main.yaml vars/main.local.yaml
    $ # Edit vars/main.local.yml to adjust deployment parameters
    $ ansible-playbook -i hosts.local deploy.yaml

Redeployment Usage:

* Assumes Undercloud machine was already built once using deploy.yaml playbook

::

    $ # Edit vars/main.local.yml to adjust deployment parameters
    $ ansible-playbook -i hosts.local redeploy.yaml

* Redeploy was only tested on small # of machines (Microcloud - 7 overcloud nodes)

ScaleLab Hardware - SLC1, SLC2
------------------------------

=  =================================================  ======  =====  ====  ======
Deployments vs OpenStack Versions
---------------------------------------------------------------------------------
#  deployment scenario                                Newton  Ocata  Pike  Queens
=  =================================================  ======  =====  ====  ======
0  1 Controller / X Computes                          Yes     Yes    Yes   Yes
1  3 Controllers / X Computes                         Yes     Yes    Yes   Yes
=  =================================================  ======  =====  ====  ======

Microcloud Hardware
-------------------

=  =================================================  ======  =====  ====  ======
Deployments vs OpenStack Versions
---------------------------------------------------------------------------------
#  deployment scenario                                Newton  Ocata  Pike  Queens
=  =================================================  ======  =====  ====  ======
0  1 Controller / X Computes                          Yes     Yes    Yes   Yes
1  3 Controllers / X Computes                         Yes     Yes    Yes   Yes
2  1 Controller / 3 CephStorage Nodes / X Computes    Yes     Yes    Yes   No
3  3 Controllers / 3 CephStorage Nodes / X Compute    Yes     Yes    Yes   No
4  1 Controller / 3 ObjectStorage Nodes / X Computes  Yes     Yes    Yes   No
5  1 Controller / 3 BlockStorage Nodes / X Computes   Yes     Yes    Yes   No
6  1 Controller / 1 Networker / X Computes            No      No     Yes   No
7  3 Controllers / 1 Networker / X Computes           No      No     Yes   No
8  1 Controller / X ComputeHCIs                       No      No     Yes   No
9  3 Controllers / X ComputeHCIs                      No      No     Yes   No
=  =================================================  ======  =====  ====  ======
