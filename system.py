import re
import os
import os.path


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


def mediainfo():
    blocks = [name for name in os.listdir('/sys/block') if name.startswith('mmcblk')]

    for block in blocks:
        path = os.path.join('/sys/block', block)

        filename = os.join(path, 'device/size')
        block_size = int(open(filename).readline()) * 512

        filename = os.join(path, 'device/type')
        block_media = open(filename).readline()

        partitions = [name for name in os.listdir(path) if name.startswith(block)]

        for partition in partitions:
            pass


def get_block_info(blockname):
    syspath = os.path.join('/sys/block', blockname)

    info = {}

    # units of size are 512 byte blocks
    filename = os.path.join(syspath, 'size')
    info['size'] = int(open(filename).readline()) * 512

    # type is either SD or MMC
    filename = os.path.join(syspath, 'device/type')

    text = open(filename).readline()

    if text.startswith('SD'):
        info['type'] = 'sd'
    elif text.startswith('MMC'):
        info['type'] = 'emmc'
    else:
        info['type'] = 'unknown'

    info['partitions'] = []

    for name in [name for name in os.listdir(syspath) if name.startswith(blockname)]:
        info['partitions'].append(get_partition_info(os.path.join(syspath, name)))

    for part in info['partitions']:
        part['ratio'] = part['size'] / info['size']

    return info


def get_partition_info(path):
    part = {}

    filename = os.path.join(path, 'partition')
    part['partition'] = int(open(filename).readline())

    # units of start are 512 byte blocks
    filename = os.path.join(path, 'start')
    part['start'] = int(open(filename).readline()) * 512

    # units of size are 512 byte blocks
    filename = os.path.join(path, 'size')
    part['size'] = int(open(filename).readline()) * 512

    return part


if __name__ == '__main__':
    from pprint import pprint
    pprint(uptime())
    pprint(stat())
    pprint(meminfo())

    for name in filter(lambda s: s.startswith('mmc'), os.listdir('/sys/block')):
        pprint(get_block_info(name))
