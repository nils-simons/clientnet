def remoteShell(cmd):
    import os
    path_cmd_partitioned = cmd.partition("/workdir/")
    workdir = path_cmd_partitioned[2]
    # if workdir == "undifined":
    #     pass
    # else:
    #     # workdir = workdir.replace("\\", "\\\\")
    #     os.chdir(workdir)
    only_command = path_cmd_partitioned[0].replace("/cmd/", "").replace(path_cmd_partitioned[1], "").replace(path_cmd_partitioned[2], "")
    
    if "cd " in only_command:
        cd_path = only_command.replace("cd ", "")
        # cd_path = cd_path.replace("\\", "\\\\")
        os.chdir(cd_path)
        return os.getcwd() + "__docknext__Directory changed!"
    ret = os.getcwd() + "__docknext__" + only_command
    return ret