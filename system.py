import re


uptime_fields = ['uptime', 'idle']


def uptime():
    fields = open('/proc/uptime').readline().split()
    return dict(zip(uptime_fields, map(float, fields)))


stat_cpu_fields = ['user', 'nice', 'system', 'idle', 'iowait', 'softirq', 'steal', 'guest', 'guest_nice']


def stat():
    results = {'cpu': {}}

    for line in open('/proc/stat'):
        fields = line.split()

        if fields[0].startswith('cpu'):
            name, *cpu_fields = fields
            results['cpu'][name] = dict(zip(stat_cpu_fields, map(int, cpu_fields)))
        elif fields[0].startswith('btime'):
            results['btime'] = int(fields[1])

    return results


def meminfo():
    results = {}

    for line in open('/proc/meminfo'):
        match = re.search('(.*):\s*(\d+)\s*kB', line)

        if match is not None:
            results[match.group(1)] = int(match.group(2))

    return results


if __name__ == '__main__':
    from pprint import pprint
    pprint(uptime())
    pprint(stat())
    pprint(meminfo())
