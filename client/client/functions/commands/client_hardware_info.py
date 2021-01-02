def getHardwareInfo():
    import psutil
    import platform
    from datetime import datetime

    f = open("data/hardware_info.txt", "a")

    def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    f.write("="*40 + "System Information" + "="*40)
    uname = platform.uname()
    f.write(f"\nSystem: {uname.system}")
    f.write(f"\nNode Name: {uname.node}")
    f.write(f"\nRelease: {uname.release}")
    f.write(f"\nVersion: {uname.version}")
    f.write(f"\nMachine: {uname.machine}")
    f.write(f"\nProcessor: {uname.processor}")

    # Boot Time
    f.write("\n" + "="*40 + "Boot Time" + "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    f.write(f"\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

    # let's f.write CPU information
    f.write("\n" + "="*40 + "CPU Info" + "="*40)
    # number of cores
    f.write("\nPhysical cores:" + str(psutil.cpu_count(logical=False)))
    f.write("\nTotal cores:" + str(psutil.cpu_count(logical=True)))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    f.write(f"\nMax Frequency: {cpufreq.max:.2f}Mhz")
    f.write(f"\nMin Frequency: {cpufreq.min:.2f}Mhz")
    f.write(f"\nCurrent Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    f.write("\nCPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        f.write(f"\nCore {i}: {percentage}%")
    f.write(f"\nTotal CPU Usage: {psutil.cpu_percent()}%")

    # Memory Information
    f.write("\n" + "="*40 + "Memory Information" + "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    f.write(f"\nTotal: {get_size(svmem.total)}")
    f.write(f"\nAvailable: {get_size(svmem.available)}")
    f.write(f"\nUsed: {get_size(svmem.used)}")
    f.write(f"\nPercentage: {svmem.percent}%")
    f.write("\n" + "="*20 + "SWAP" + "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    f.write(f"\nTotal: {get_size(swap.total)}")
    f.write(f"\nFree: {get_size(swap.free)}")
    f.write(f"\nUsed: {get_size(swap.used)}")
    f.write(f"\nPercentage: {swap.percent}%")

    # Disk Information
    f.write("\n" + "="*40 + "Disk Information" + "="*40)
    f.write("\nPartitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        f.write(f"\n=== Device: {partition.device} ===")
        f.write(f"\n  Mountpoint: {partition.mountpoint}")
        f.write(f"\n  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        f.write(f"\n  Total Size: {get_size(partition_usage.total)}")
        f.write(f"\n  Used: {get_size(partition_usage.used)}")
        f.write(f"\n  Free: {get_size(partition_usage.free)}")
        f.write(f"\n  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    f.write(f"\nTotal read: {get_size(disk_io.read_bytes)}")
    f.write(f"\nTotal write: {get_size(disk_io.write_bytes)}")

    # Network information
    f.write("\n" + "="*40 + "Network Information" + "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            f.write(f"\n=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                f.write(f"\n  IP Address: {address.address}")
                f.write(f"\n  Netmask: {address.netmask}")
                f.write(f"\n  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                f.write(f"\n  MAC Address: {address.address}")
                f.write(f"\n  Netmask: {address.netmask}")
                f.write(f"\n  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    f.write(f"\nTotal Bytes Sent: {get_size(net_io.bytes_sent)}")
    f.write(f"\nTotal Bytes Received: {get_size(net_io.bytes_recv)}")


    # GPU information
    import GPUtil
    from tabulate import tabulate
    f.write("\n" + "="*40 + "GPU Details" + "="*40 + "\n")
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        # get the GPU id
        gpu_id = gpu.id
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load*100}%"
        # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature, gpu_uuid
        ))

    f.write(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory", "temperature", "uuid")))


    f.close()