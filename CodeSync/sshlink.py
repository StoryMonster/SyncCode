import paramiko


class SSHLink(object):
    def __init__(self, hostname, username, password, logger):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname, username=username, password=password)

    def __exit__(self, *args):
        self.close()

    def close(self):
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
        sftp = self.client.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()


if __name__ == "__main__":
    link = SSHLink("hzlinb19", "dochen", "1028Sun20", None)
    output, error = link.execute("ls")
    print("output:\n" + output)
    print("error:\n" + error)
    link.post_file("D:\\Cygwin\\home\\dochen\\CodeSync\\CodeSync\\sync_code_procedure.py", "/home/dochen/sync_code_procedure.py")