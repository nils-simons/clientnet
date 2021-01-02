def getScreenshot():
    try:
        import pyautogui
        import ftplib
        from datetime import datetime
        import os
        import uuid
        import functions.get_config as get_config
    except:
        return "Cannot import all required modules."
    try:
        data_dir = 'data/'
        today = datetime.today()
        now = datetime.now()
        client_mac_adrs = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        client_mac_adrs = client_mac_adrs.replace(":", ".")
        screenshot_file_path = data_dir + today.strftime("%Y.%m.%d") + "-" + now.strftime("%Hh%M.%S") + "_" + client_mac_adrs + "_screenshot.png"
    except:
        return "Cannot create correct Filename."

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_file_path)
    except:
        return "Cannot take or save screenshot."
    try:
        ftp_session = ftplib.FTP(get_config.getWebConfig("ftp_server_addr"), get_config.getWebConfig("ftp_server_user"), get_config.getWebConfig("ftp_server_passwd"))
        img_file = open(screenshot_file_path,'rb')
        upld_screenshot_file_path = screenshot_file_path.replace(data_dir, "")
        ftp_session.storbinary('STOR /client_screenshots/' + upld_screenshot_file_path, img_file)
        img_file.close()
        ftp_session.quit()
    except:
        return "Cannot get Web config or Upload to FTP Server."
    try:
        os.remove(screenshot_file_path)
    except:
        pass
    return "Screenshot uploaded at: https://data.clientnet.ml/client_screenshots/" + upld_screenshot_file_path