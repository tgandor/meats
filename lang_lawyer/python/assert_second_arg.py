
def eval_true():
    print('True assertion evaluated')
    return 'Not evaluated'

def eval_false():
    print('False assertion evaluated')
    return 'Exception value which will be printed'

assert True, eval_true()
assert False, eval_false()

