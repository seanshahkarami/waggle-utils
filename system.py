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


def get_mmc_info(path):
    mmc = {}

    # units of size are 512 byte blocks
    filename = os.path.join(path, 'size')
    mmc['size'] = int(open(filename).readline()) * 512

    # type is either SD or MMC
    filename = os.path.join(path, 'device/type')
    mmc['type'] = open(filename).readline().lower()

    mmc['partitions'] = []

    for name in [name for name in os.listdir(path) if name.startswith('mmc')]:
        mmc['partitions'].append(get_partition_info(os.path.join(path, name)))

    for part in mmc['partitions']:
        part['ratio'] = part['size'] / mmc['size']

    return mmc


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

    pprint(get_mmc_info('/sys/block/mmcblk0'))
    pprint(get_mmc_info('/sys/block/mmcblk1'))
