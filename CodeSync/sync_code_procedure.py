from sshlink import SSHLink
import os
import subprocess
import collections
import re
from utils import convert_to_unix_eol
import platform

"""
ChangedFile: The modified file under workspace
    relative_path: file name and path
    action: D(delete), A(add), M(modify)
"""
ChangedFile = collections.namedtuple("ChangedFile", ["relative_path", "action"])


class SyncCodeProcedure(object):
    def __init__(self, name, context):
        self.context = context
        assert self._context_precheck()
        self.name = name
        self.source_workdir = context["source_workdir"]
        self.target_workdir = context["target_workdir"]
        self.username = context["username"]
        self.hostname = context["hostname"]
        self.password = context["password"]
        self.sshlink = SSHLink(self.hostname, self.username, self.password)
        self.changed_files = []


    def __exit__(self, *args):
        self.stop()


    def stop(self):
        if self.sshlink is not None:
            self.sshlink.close()
            self.sshlink = None


    def start(self):
        self._get_all_changed_files()
        self._apply_changes_to_target()

    
    def _get_all_changed_files(self):
        cwd = os.getcwd()
        os.chdir(self.source_workdir)
        output = os.popen("git status --short --ignore-submodules").readlines()
        os.chdir(cwd)
        regex = re.compile(r"\s*(\S+)\s+(\S+)\s*")
        for line in output:
            matched = regex.match(line)
            if not matched: continue
            if matched.group(1) in ("A", "D", "M"):
                self.changed_files.append(ChangedFile(matched.group(2), matched.group(1)))
            elif matched.group(1) == "??":
                relative_path = matched.group(2)
                if self._is_user_code_file(relative_path):
                    self.changed_files.append(ChangedFile(relative_path, "A"))

    
    def _apply_changes_to_target(self):
        self.sshlink.execute(f"pushd {self.target_workdir} && git reset --hard HEAD && popd")
        print("reset target to HEAD")
        for changed_file_with_relativ_path, action in self.changed_files:
            if action in ["A", "M"]:
                if platform.uname().system == "Windows":
                    convert_to_unix_eol(os.path.join(self.source_workdir, changed_file_with_relativ_path))
                self._post_file_to_target(changed_file_with_relativ_path)
            else:
                self._remove_file_on_target(changed_file_with_relativ_path)


    def _post_file_to_target(self, file_with_relative_path):
        self.sshlink.post_file(self.source_workdir + "/" + file_with_relative_path, self.target_workdir + "/" + file_with_relative_path)
        print(f"send {file_with_relative_path} to {self.hostname}")


    def _remove_file_on_target(self, file_with_relative_path):
        file_path = self.target_workdir + "/" + file_with_relative_path
        self.sshlink.execute(f"rm {file_path} -rf")
        print(f"remove {file_path} on {self.hostname}")


    def _is_user_code_file(self, file_name):
        return re.match(r".*(\.cpp|\.hpp|\.py|\.mt|\.ttcn3)$", file_name)


    def _context_precheck(self):
        neccessary_fields = ["username", "password", "hostname", "source_workdir", "target_workdir"]
        for field in neccessary_fields:
            if field not in self.context:
                print(f"{field} not found in configuration of {self.name}")
                return False
        return True
