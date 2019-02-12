from sshlink import SSHLink
import os
from utils import convert_to_unix_eol, procedure_context_precheck
import queue
import platform


class SyncNonGitCodeProcedure(object):
    def __init__(self, name, context):
        assert procedure_context_precheck(name, context)
        self.context = context
        self.name = name
        self.source_workdir = context["source_workdir"]
        self.target_workdir = context["target_workdir"]
        self.username = context["username"]
        self.hostname = context["hostname"]
        self.password = context["password"]
        self.ingore_list = context["ignore"]
        self.sshlink = SSHLink(self.hostname, self.username, self.password, workspace=self.target_workdir)
        self.files = []


    def __exit__(self, *args):
        self.stop()


    def stop(self):
        if self.sshlink is not None:
            self.sshlink.close()
            self.sshlink = None


    def start(self):
        self._apply_files_to_target()


    def _is_ignored_file(self, filename):
        return False


    def _apply_files_to_target(self):
        self.sshlink.execute(f"pushd {self.target_workdir} && rm * -rf && popd")
        print("Clean target directory")
        cwd = os.getcwd()
        os.chdir(self.source_workdir)
        folders_queue = queue.Queue()
        folders_queue.put(".")
        while not folders_queue.empty():
            folder = folders_queue.get()
            for file in os.listdir(folder):
                path = folder + "/" + file
                if os.path.isdir(path):
                    self.sshlink.mkdir_on_target(path)
                    print(f"create folder {path} on target")
                    folders_queue.put(path)
                elif os.path.isfile(path):
                    self.sshlink.post_file(self.source_workdir + "/" + path, self.target_workdir + "/" + path)
                    print(f"send {path} to {self.hostname}")
        os.chdir(cwd)

        