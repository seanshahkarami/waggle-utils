units = {
    'kB': 1024,
}


def loadavg():
    with open('/proc/loadavg') as f:
        fields = f.readline().split()
        return {
            'loadavg1': float(fields[0]),
            'loadavg5': float(fields[1]),
            'loadavg10': float(fields[2]),
        }


def cpustats():
    stats = {}

    with open('/proc/stat') as f:
        for line in f:
            if line.startswith('cpu'):
                fields = line.split()
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

    with open('/proc/meminfo') as f:
        for line in f:
            fields = line.split(':')
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

    with open('/proc/mounts') as f:
        for line in f:
            fields = line.split()
            results[fields[1]] = {
                'dev': fields[0],
                'type': fields[2],
                'attr': fields[3],
            }

    return results


def uptime():
    with open('/proc/uptime') as f:
        fields = f.readline().split()
        return {
            'uptime': float(fields[0]),
            'idle': float(fields[1]),
        }
