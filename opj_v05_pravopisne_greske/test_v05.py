def testname(func):
    print()
    print(func.__name__.upper())
    print('-'*60)

def test(func, input, output = None):
    def reformat(data):
        maxlen = 80
        maxdict = 5
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in data)
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k in sorted(data)[:maxdict])
        return data

    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n=> %s\n%s= %s\n' % (success, func.__name__, reformat(input_copy), reformat(output), success_rel ,reformat(result)))
