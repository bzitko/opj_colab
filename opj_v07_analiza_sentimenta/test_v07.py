def testname(func):
    print()

    print(func.__name__.upper())
    print('#'*60)

def reformat(data):
        maxlen = 80
        maxdict = 10
        maxlist = 10
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            if len(data) > maxlist:
                temp = [reformat(el) for el in list(data)[:maxlist]] + ['...']
                return type(data)(temp)
            else:
                return type(data)(reformat(el) for el in list(data))
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k in sorted(data)[:maxdict])
        return data


def test(func, input, output = None):
    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n\t=> %s\n\t%s= %s\n' % (success, func.__name__, reformat(str(reformat(input_copy))), reformat(output), success_rel , reformat(result)))
    return result

def testclass(obj, method, input, outputs = {}):
    import copy
    input_copy = copy.deepcopy(input)
    method(*input)
    lines = []
    passed = True
    for attr in sorted(outputs):
        output = outputs[attr]

        if not hasattr(obj, attr):
            result = '???'
            passed = False
        else:
            result = getattr(obj, attr)
        passed = result == output
        success = 'OK' if result == output else 'X'
        success_rel = '=' if result == output else '!'
        lines.append('\t%s\t%s' % (success, attr))
        lines.append('\t=> %s\n\t%s= %s\n' % (reformat(output), success_rel , reformat(result)))
        #print('%s\t%s%s \n\t=> %s\n\t%s= %s\n' % (success, method.__name__, reformat(str(reformat(input_copy))), reformat(output), success_rel , reformat(result)))

    passed == 'OK' if passed else 'X'
    lines.insert(0, '%s\t%s%s' % (success, method.__name__, reformat(str(reformat(input_copy)))))
    for line in lines:
        print(line)
