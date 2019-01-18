#!/usr/bin/env python
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import json
import os
import subprocess
import sys
import time
import yaml


def remove_undercloud(instackenv_json, instackenv_json_output, uc_pm_addr):
    nodes = []
    with open(instackenv_json, "r") as rf:
        instackenv = json.load(rf)
        for node in instackenv["nodes"]:
            if uc_pm_addr in node["pm_addr"][0:node["pm_addr"].find(".")]:
                print "WARN :: Found Undercloud included in the instackenv"
                continue
            nodes.append(node)
    with open(instackenv_json_output, "w") as wf:
        data = {
            "nodes": nodes,
        }
        json.dump(data, wf, indent=4, sort_keys=True)


def main():
    start_time = time.time()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(
        description="Reads instackenv and validates the nodes ipmi access.",
        prog="instackenv-validate.py")
    parser.add_argument(
        "-i", "--instackenv", default="instackenv.json", help="Path to instackenv.json file.")
    parser.add_argument(
        "-o", "--output-instackenv", default="instackenv.valid.json",
        help="Outputs the validated instackenv.json.  Defaults to 'instackenv.valid.json'")
    parser.add_argument(
        "-f", "--output-invalid", default="invalid-nodes.yaml",
        help="Outputs the failed nodes.  Defaults to 'invalid-nodes.yaml'")
    parser.add_argument(
        "-u", "--undercloud-ipmi-addr", default=None,
        help="Undercloud pm_addr to remove mistakenly included underclouds in instackenv.")
    cliargs = parser.parse_args()

    print "INFO :: instackenv-validate.py reading in {}".format(cliargs.instackenv)
    print "INFO :: Script directory: {}".format(script_dir)

    if os.path.isfile(cliargs.instackenv):
        instackenv_json = cliargs.instackenv
    else:
        instackenv_json = os.path.join(script_dir, cliargs.instackenv)

    if not os.path.isfile(instackenv_json):
        print "ERROR :: Can not find {}".format(cliargs.instackenv)
        sys.exit(1)

    print "INFO :: Opening instackenv file: {}".format(instackenv_json)
    print "INFO :: Outputting valid instackenv file: {}".format(cliargs.output_instackenv)
    print "INFO :: Outputting invalid nodes yaml: {}".format(cliargs.output_invalid)

    # Remove UC from instackenv (if if is accidently included into the instackenv.json)
    if cliargs.undercloud_ipmi_addr:
        remove_undercloud(instackenv_json, cliargs.output_instackenv, cliargs.undercloud_ipmi_addr)

    # Open instackenv and validate
    baremetal_ips = []
    good_nodes = []
    failed_nodes = []
    errors = 0
    with open(cliargs.output_instackenv, "r") as of:
        instackenv = json.load(of)
        for node in instackenv["nodes"]:
            if "pm_addr" in node:
                if len(node["pm_addr"]) == 0:
                    # Unsure of what to do since we have no idea what is the failed node
                    print "ERROR :: pm_addr length 0 on node: {}".format(node)
                    errors += 1
                    continue
            else:
                # Unsure of what to do since we have no idea what is the failed node
                print "ERROR :: pm_addr missing on node: {}".format(node)
                errors += 1
                continue

            print "INFO :: Validating node {}".format(node["pm_addr"])

            if "pm_password" in node:
                if len(node["pm_password"]) == 0:
                    print "ERROR :: Password length 0 on node: {}".format(node["pm_addr"])
                    errors += 1
                    failed_nodes.append(node["pm_addr"])
                    continue
            else:
                print "ERROR :: Password does not exist: {}".format(node["pm_addr"])
                errors += 1
                failed_nodes.append(node["pm_addr"])
                continue

            if "pm_user" in node:
                if len(node["pm_user"]) == 0:
                    print "ERROR :: User 0 length on node: {}".format(node["pm_addr"])
                    errors += 1
                    failed_nodes.append(node["pm_addr"])
                    continue
            else:
                print "ERROR :: User does not exist for node: {}".format(node["pm_addr"])
                errors += 1
                failed_nodes.append(node["pm_addr"])
                continue

            if node["pm_type"] == "pxe_ipmitool":
                cmd = ("ipmitool -R 1 -I lanplus -H {} -U {} -P {} chassis "
                       "status".format(node["pm_addr"], node["pm_user"], node["pm_password"]))
                print "INFO :: Executing: {}".format(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     shell=True)
                (output, err) = p.communicate()
                p_status = p.wait()
                if p_status != 0:
                    print "ERROR :: ipmitool failed on {}".format(node["pm_addr"])
                    errors += 1
                    failed_nodes.append(node["pm_addr"])
                    continue
                baremetal_ips.append(node["pm_addr"])
            good_nodes.append(node)

    if not len(set(baremetal_ips)) == len(baremetal_ips):
        print "ERROR :: Baremetals IPs are not all unique."
        errors += 1

    with open(cliargs.output_instackenv, "w") as wf:
        data = {
            "nodes": good_nodes,
        }
        json.dump(data, wf, indent=4, sort_keys=True)

    print "Failed Nodes: {}".format(failed_nodes)
    with open(cliargs.output_invalid, "w") as failed_out_yaml:
        yaml.safe_dump(failed_nodes, failed_out_yaml, default_flow_style=False)

    print "INFO :: Took {} to validate instackenv file.".format(round(time.time() - start_time, 2))
    if errors == 0:
        print "INFO :: SUCCESS: found 0 errors"
        return 0
    else:
        print "INFO :: found {} errors".format(errors)
        return 1


if __name__ == "__main__":
    sys.exit(main())
