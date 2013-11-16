#!/usr/bin/env python

import re

def neg32bit(n):
    return ((1<<32) - n - 1) & ((1<<32) - 1)

def _verify_mask(mask):
    notmask = neg32bit(mask)
    if (notmask & (notmask + 1)) != 0:
        raise ValueError, "resulting mask is malformed (not like 1..10..0)"

def _ip_by_bytes(nums):
    return nums[0]<<24 | nums[1] << 16 | nums[2] << 8 | nums[3]

def _ip_to_bytes(ip):
    return (ip >> 24) & 0xFF, (ip >> 16) & 0xFF, (ip >> 8) & 0xFF, ip & 0xFF

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
    num = get_mask_bits(mask)
    tupl = (num,) + _ip_to_bytes(mask) + (1<<(32-num),)
    print "Mask with %d bits: %d.%d.%d.%d - %d addresses" % tupl

def print_net_info(ip, mask):
    print "(net) %d.%d.%d.%d < e.g. %d.%d.%d.%d (ip) < %d.%d.%d.%d (bcast)" % (
        _ip_to_bytes(ip & mask)
        + _ip_to_bytes(ip)
        + _ip_to_bytes(ip | neg32bit(mask)))

def go():
    try:
        while True:
            orig = raw_input()
            query = orig.replace('IPv4', '') # strip something
            nums = map(int, re.findall('\d+', query))
            # print 'Processing', repr(orig)
            if len(nums) == 1:
                # just checking mask
                if nums[0] < 0 or nums[0] > 32:
                    print "Error: number not understood:", nums[0]
                    continue
                print_mask_info(get_mask_by_bits(nums[0]))
            elif len(nums) == 4 and 'IPv4' in orig:
                # windows ipconfig, read next line for mask
                query2 = raw_input()
                # print 'Processing more:', query2
                mnums = map(int, re.findall('\d+', query2))
                mask = _ip_by_bytes(mnums)
                ip = _ip_by_bytes(nums)
                print_mask_info(mask)
                print_net_info(ip, mask)
            elif len(nums) in (4, 8, 12):
                # just netmask, or ifconfig, or IP + mask (see spoj)
                mask = _ip_by_bytes(nums[-4:])
                print_mask_info(mask)
                if len(nums) in (8, 12):
                    ip = _ip_by_bytes(nums[:4])
                    print_net_info(ip, mask)
            elif len(nums) == 0:
                continue
            else:
                print "Wrong number of numbers in line:", len(nums)
    except EOFError:
        pass

if __name__ == '__main__':
    go()
