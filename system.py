import re


def readfile(path):
    with open(path, 'r') as f:
        return f.read()


def uptime():
    fields = readfile('/proc/uptime').split()
    return {
        'uptime': float(fields[0]),
        'idle': float(fields[1]),
    }


def stat():
    stat = {'cpu': []}

    for line in open('/proc/stat'):
        fields = line.split()

        if fields[0].startswith('cpu'):
            stat['cpu'].append({
                'name': fields[0],
                'user': int(fields[1]),
                'nice': int(fields[2]),
                'system': int(fields[3]),
                'idle': int(fields[4]),
                'iowait': int(fields[5]),
                'softirq': int(fields[6]),
                'steal': int(fields[7]),
                'guest': int(fields[8]),
                'guest_nice': int(fields[9]),
            })
        elif fields[0].startswith('btime'):
            stat['boot_time'] = int(fields[1])

    return stat


print(stat())
