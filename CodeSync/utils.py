import os
import queue

def convert_to_unix_eol(file_name):
    with open(file_name, "r+", newline="\n") as fd:
        lines = fd.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip("\r\n")
        fd.seek(0, 0)
        fd.truncate(0)
        fd.writelines("\n".join(lines))
        fd.write("\n")


def procedure_context_precheck(procedure_name, context):
    neccessary_fields = ["username", "password", "hostname", "source_workdir", "target_workdir", "ignore"]
    for field in neccessary_fields:
        if field not in context:
            print(f"{field} not found in configuration of {procedure_name}")
            return False
    return True