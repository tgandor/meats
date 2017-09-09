from __future__ import print_function

nums = "1 2 3"

# Py2:

nums1 = map(int, nums.split())        # 8 characters saved, + 2 per additional letter in for variable
nums2 = [int(x) for x in nums.split()]

print('Py2 way:', nums1, nums2, nums1 == nums2)

# Py3:

nums1 = list(map(int, nums.split()))  # surprise: list(map) wins by 2 characters still!
nums2 = [int(x) for x in nums.split()]

print('Py3 way:', nums1, nums2, nums1 == nums2)

