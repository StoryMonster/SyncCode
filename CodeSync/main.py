from sync_code_procedure import SyncCodeProcedure
import json
import argparse
import os


def get_configurations_from_config_file(config_file):
    with open(config_file, "r") as fd:
        return json.loads(fd.read())


def run_procedure(procedure_name, procedure_config):
    procudure = SyncCodeProcedure(procedure_name, procedure_config)
    procudure.start()
    procudure.stop()


def parse_args():
    parser = argparse.ArgumentParser(description="code sync tool based on ssh")
    parser.add_argument('--config-file', type=str, default="config.ini", help='specify the configuration file')
    parser.add_argument('--specify', type=str, default="", help='specify the sync object, default is to sync all')
    return parser.parse_args()


def is_root_dir(path):
    return ".git" in os.listdir(path)


def get_repository_root_path():
    import os, platform
    cwd = os.getcwd()
    spliter = "\\" if platform.system() == "Windows" else "/"
    nodes = cwd.split(spliter)
    while len(nodes) != 0:
        path = spliter.join(nodes)
        if is_root_dir(path): return path
        del nodes[-1]
    return ""


def get_procedure_name_for_sync_current_repository(configs):
    for proc_name in configs:
        if os.path.samefile(configs[proc_name]["source_workdir"], get_repository_root_path()):
            return proc_name
    return None


if __name__ == "__main__":
    args = parse_args()
    configs_for_procedures = get_configurations_from_config_file(args.config_file)
    procedure_name = args.specify or get_procedure_name_for_sync_current_repository(configs_for_procedures)
    if procedure_name is None:
        print("Your working directory is not configured")
        exit(-1)
    if procedure_name not in configs_for_procedures:
        print(f"Unknown procedure: {procedure_name}")
        exit(-1)
    run_procedure(procedure_name, configs_for_procedures[procedure_name])
