import os
import os.path
import re


units = {
    'kB': 1024,
    'mB': 1024**2,
    'gB': 1024**3,
}


def readtext(*path):
    with open(os.path.join(*path)) as f:
        return f.readline().strip()


def readint(*path):
    with open(os.path.join(*path)) as f:
        return int(f.readline())


def readlines(*path):
    with open(os.path.join(*path)) as f:
        for line in f:
            yield line.rstrip()


def readfields(sep, *path):
    with open(os.path.join(*path)) as f:
        for line in f:
            yield re.split(sep, line)


def loadavg():
    fields = readtext('/proc/loadavg').split()

    return {
        'loadavg1': float(fields[0]),
        'loadavg5': float(fields[1]),
        'loadavg10': float(fields[2]),
    }


def cpustats():
    stats = {}

    for fields in readfields('\s+', '/proc/stat'):
        if fields[0].startswith('cpu'):
            stats[fields[0]] = {
                'user': int(fields[1]),
                'nice': int(fields[2]),
                'system': int(fields[3]),
                'idle': int(fields[4]),
                'iowait': int(fields[5]),
                'softirq': int(fields[6]),
            }

    return stats


def meminfo():
    stats = {}

    for fields in readfields('\s*:\s*', '/proc/meminfo'):
        key = fields[0].strip()
        rhs = fields[1].split()

        if len(rhs) == 1:
            value = int(rhs[0])
        elif len(rhs) == 2:
            value = int(rhs[0]) * units[rhs[1]]

        stats[key] = value

    return stats


def mounts():
    results = {}

    for line in readlines('/proc/mounts'):
        fields = line.split()

        results[fields[1]] = {
            'dev': fields[0],
            'type': fields[2],
            'attr': fields[3],
        }

    return results


def uptime():
    fields = readtext('/proc/uptime').split()

    return {
        'uptime': float(fields[0]),
        'idle': float(fields[1]),
    }


def listblocks():
    return os.listdir('/sys/block')


def blockinfo(block):
    blockpath = os.path.join('/sys/block', block)

    blockinfo = {}

    sector_size = readint(blockpath, 'queue/hw_sector_size')
    blockinfo['size'] = readint(blockpath, 'size') * sector_size
    blockinfo['type'] = readtext(blockpath, 'device/type')

    blockinfo['partitions'] = {}

    for part in [part for part in os.listdir(blockpath) if part.startswith(block)]:
        partpath = os.path.join(blockpath, part)

        partinfo = {}

        partinfo['start'] = readint(partpath, 'start') * sector_size
        partinfo['size'] = readint(partpath, 'size') * sector_size
        partinfo['ratio'] = partinfo['size'] / blockinfo['size']

        number = readint(partpath, 'partition')
        blockinfo['partitions'][number] = partinfo

    return blockinfo


def devices():
    devices = []

    for device in os.listdir('/sys/bus/usb/devices'):
        path = os.path.join('/sys/bus/usb/devices', device)

        try:
            devices.append({
                'manufacturer': readtext(path, 'manufacturer'),
                'product': readtext(path, 'product'),
                'version': readtext(path, 'version'),
                'idProduct': readtext(path, 'idProduct'),
                'idVendor': readtext(path, 'idVendor'),
            })
        except FileNotFoundError:
            continue

    return devices
