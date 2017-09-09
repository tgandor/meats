#!/usr/bin/env python

import re
import sys

state = {'output': False}

def neg32bit(n):
    return ((1<<32) - n - 1) & ((1<<32) - 1)


def _verify_mask(mask):
    notmask = neg32bit(mask)
    if (notmask & (notmask + 1)) != 0:
        raise ValueError("resulting mask is malformed (not like 1..10..0):" + _format_ip(mask) + " = " + bin(mask))


def _ip_by_bytes(nums):
    return nums[0]<<24 | nums[1] << 16 | nums[2] << 8 | nums[3]


def _ip_to_bytes(ip):
    return (ip >> 24) & 0xFF, (ip >> 16) & 0xFF, (ip >> 8) & 0xFF, ip & 0xFF


def _format_ip(num_ip):
    return '%d.%d.%d.%d' % _ip_to_bytes(num_ip)


def get_mask_by_bytes(nums):
    mask = _ip_by_bytes(nums)
    _verify_mask(mask)
    return mask


def get_mask_by_bits(bits):
    bitsleft = 32 - bits
    return neg32bit((1 << bitsleft) - 1)


def get_mask_bits(mask):
    _verify_mask(mask)
    return bin(mask).count('1') # Python popcnt


def print_mask_info(mask):
    _hr()
    num = get_mask_bits(mask)
    tupl = (num,) + _ip_to_bytes(mask) + (1<<(32-num),)
    print("Mask with %d bits: %d.%d.%d.%d - %d addresses" % tupl)
    state['output'] = True


def print_net_info(ip, mask):
    print("(net) %d.%d.%d.%d < e.g. %d.%d.%d.%d (ip) < %d.%d.%d.%d (bcast)" % (
        _ip_to_bytes(ip & mask)
        + _ip_to_bytes(ip)
        + _ip_to_bytes(ip | neg32bit(mask))))
    state['output'] = True


def _hr():
    print('-' * 40)


def go():
    while True:
        orig = sys.stdin.readline()
        if not orig:
            break
        query = orig.replace('IPv4', '') # strip something
        nums = list(map(int, re.findall('\d+', query)))
        # print 'Processing', repr(orig)
        if len(nums) == 1:
            # just checking mask
            if nums[0] < 0 or nums[0] > 32:
                print("Error: number not understood: " + str(nums[0]))
                continue
            print_mask_info(get_mask_by_bits(nums[0]))
        elif len(nums) == 4 and 'IPv4' in orig:
            # windows ipconfig, read next line for mask
            query2 = sys.stdin.readline()
            if not query2:
                break
            # print 'Processing more:', query2
            mnums = [int(x) for x in re.findall('\d+', query2)]
            mask = _ip_by_bytes(mnums)
            ip = _ip_by_bytes(nums)
            print_mask_info(mask)
            print_net_info(ip, mask)
        elif len(nums) in (4, 8, 12):
            # just netmask, or ifconfig, or IP + mask (see spoj)
            mask = _ip_by_bytes(nums[-4:])
            try:
                _verify_mask(mask)
            except ValueError:
                continue
            print_mask_info(mask)
            if len(nums) in (8, 12):
                ip = _ip_by_bytes(nums[:4])
                print_net_info(ip, mask)
    if state['output']:
        _hr()

if __name__ == '__main__':
    go()
