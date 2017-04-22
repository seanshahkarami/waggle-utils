import re


def uptime():
    fields = open('/proc/uptime').readline().split()

    return {
        'uptime': float(fields[0]),
        'idle': float(fields[1]),
    }


def stat():
    results = {'cpu': []}

    for line in open('/proc/stat'):
        fields = line.split()

        if fields[0].startswith('cpu'):
            results['cpu'].append({
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
            results['btime'] = int(fields[1])

    return results


def meminfo():
    results = {}

    for line in open('/proc/meminfo'):
        match = re.search('(.*):\s*(\d+)\s*kB')

        if match is not None:
            results[match.group(1)] = int(match.group(2))

    return results


if __name__ == '__main__':
    from pprint import pprint
    pprint(uptime())
    pprint(stat())
    pprint(meminfo())
