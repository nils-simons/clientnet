def getSystemInfo():
    import platform
    this_system = platform.uname()
    infos = f"System: {this_system.system} {this_system.release}\nVersion: {this_system.version}\nNode Name: {this_system.node}\nMachine: {this_system.machine}\nProcessor: {this_system.processor}"
    return infos