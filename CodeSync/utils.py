

def convert_to_unix_eol(file_name):
    with open(file_name, "r+", newline="\n") as fd:
        lines = fd.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip("\r\n")
        fd.seek(0, 0)
        fd.truncate(0)
        fd.writelines("\n".join(lines))
        fd.write("\n")
