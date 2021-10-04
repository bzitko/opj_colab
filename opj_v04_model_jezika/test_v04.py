def testname(func):
    print()
    print(func.__name__.upper())
    print('-'*60)

def test(func, input, output = None):
    def reformat(data):
        maxlen = 80
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in data)
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k in list(data)[:3])
        return data

    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n=> %s\n%s= %s\n' % (success, func.__name__, reformat(input_copy), reformat(output), success_rel ,result))


def test_model(func, input, output):
    def reformat(data):
        maxlen = 80
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in data)
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k,v in data.items())
        return data
    def freq_model(model):
        freq = {}
        for count in model.values():
            freq[count] = freq.get(count, 0) + 1
        return freq

    model = func(*input)
    result = freq_model(model)
    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    #print('%s\t%s%s ==> %s == %s\n' % (success, func.__name__, reformat(input), reformat(output), (result)))
    print('%s\t%s%s \n=> %s\n%s= %s\n' % (success, func.__name__, reformat(input), reformat(output), success_rel ,result))
    return model
