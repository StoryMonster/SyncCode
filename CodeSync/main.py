from sync_code_procedure import SyncCodeProcedure
import json
import argparse


def get_configurations_from_config_file(config_file):
    with open(config_file, "r") as fd:
        return json.loads(fd.read())


def parse_args():
    parser = argparse.ArgumentParser(description="code sync tool based on ssh")
    parser.add_argument('--config-file', type=str, default="config.ini", help='specify the configuration file')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    configs_for_procedures = get_configurations_from_config_file(args.config_file)
    for procedure_name in configs_for_procedures:
        config = configs_for_procedures[procedure_name]
        procudure = SyncCodeProcedure(procedure_name, config, None)
        procudure.start()
        procudure.stop()






