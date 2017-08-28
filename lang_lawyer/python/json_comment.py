import json

# No comments.

try:
    print(json.loads("""
{
  "key1": 1,
  // "key2": 2,
  "key3": "three"
}
"""))
except ValueError as e:
    print(e)
