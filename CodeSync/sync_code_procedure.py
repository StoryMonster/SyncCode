from sshlink import SSHLink
import os
import subprocess


class SyncCodeProcedure(object):
    diff_file = "a.diff"

    def __init__(self, name, context, logger):
        self.name = name
        self.context = context
        self._context_precheck()
        self.source_workdir = context["source_workdir"]
        self.target_workdir = context["target_workdir"]
        self.username = context["username"]
        self.hostname = context["hostname"]
        self.password = context["password"]
        self.logger = logger
        self.sshlink = SSHLink(self.hostname, self.username, self.password, self.logger)

    def __exit__(self, *args):
        self.stop()

    def stop(self):
        if self.sshlink is not None:
            self.sshlink.close()
            self.sshlink = None

    def start(self):
        self._generate_diff_file()
        self._post_diff_file()
        self._apply_diff_file()

    def _generate_diff_file(self):
        cwd = os.getcwd()
        workdir = os.chdir(self.source_workdir)
        generate_diff_file_command = ["git", "diff", ">", self.source_workdir + "/" + self.diff_file]
        #returncode = subprocess.run([]).returncode
        os.system("git diff > %s" % self.source_workdir + "/" + self.diff_file)
        os.chdir(cwd)

    def _post_diff_file(self):
        self.sshlink.post_file(self.source_workdir + "/" + self.diff_file, self.target_workdir + "/" + self.diff_file)

    def _apply_diff_file(self):
        output, err = self.sshlink.execute("pushd %s && git reset --hard HEAD && git apply %s && popd" % (self.target_workdir, self.diff_file))

    def _context_precheck(self):
        neccessary_fields = ["username", "password", "hostname", "source_workdir", "target_workdir"]
        for field in neccessary_fields:
            if field not in self.context:
                print(f"{field} not found in configuration of {self.name}")
                return False
        return True
