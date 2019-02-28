import paramiko
import re


class SSHLink(object):
    def __init__(self, hostname, username, password, workspace=None, platform="linux"):
        self.client = paramiko.SSHClient()
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) is not None:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            self.client.load_system_host_keys()
        self.client.connect(hostname=hostname, username=username, password=password)
        self.sftp = self.client.open_sftp()
        self.platform = platform
        if workspace is not None:
            self.sftp.chdir(workspace)

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.sftp is not None:
            self.sftp.close()
            self.sftp = None
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command=""):
        _, out, err = self.client.exec_command(command)
        output = "".join(out.readlines())
        error = "".join(err.readlines())
        return output, error

    def post_file(self, local_file, remote_file):
        ## absolute path
        self.sftp.put(local_file, remote_file)

    def mkdir_on_target(self, path):
        path = path.rstrip("/")
        last_slash_index = path.rfind("/")
        folder_name = path[last_slash_index+1:]
        parent_path = path[:last_slash_index]
        files = self.sftp.listdir(parent_path)
        if folder_name not in files:
            self.sftp.mkdir(path)
