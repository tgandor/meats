from hashlib import md5
tri_quote = lambda x: 3 * chr(34) + x + 3 * chr(34)
s = """from hashlib import md5
tri_quote = lambda x: 3 * chr(34) + x + 3 * chr(34)
s = X
print(md5(s.replace('X', tri_quote(s), 1)+chr(10)).hexdigest())"""
print(md5(s.replace('X', tri_quote(s), 1)+chr(10)).hexdigest())
