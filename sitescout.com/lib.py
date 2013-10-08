import tablib


def raw_input_json(question, jsons):
    print
    print question
    print '=' * 60

    k = jsons.keys()

    k = sorted(k)
    struct = zip(range(1, len(k) + 1), k)

    for ind, val in struct:
        print "%s\t%s" % (ind, val)

    print
    print 'Pick your number (enter to ignore): '
    c = raw_input('>> ')
    if c.strip() == '':
        return None

    choice = int(c)

    mykey = struct[choice - 1][1]

    print ''
    return jsons[mykey]


def save2xls(result, filename):
    data = tablib.Dataset([], headers=result['data'][0].keys())
    for element in result['data']:
        data.append(element.values())
    open(filename, 'wb').write(data.xls)


if __name__ == '__main__':
    # testing
    from data import country
    r = raw_input_json('no question!', country)
    print 'result', r
