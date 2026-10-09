import resource

soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print(f"before: soft={soft}, hard={hard}")

resource.setrlimit(resource.RLIMIT_NOFILE, (65535, hard))

soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print(f"after: soft={soft}, hard={hard}")

