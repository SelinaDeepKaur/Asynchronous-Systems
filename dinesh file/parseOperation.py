data = dict()

def addToDictionary(key,val):
    try:
        print(key)
        data[key]=val
        return 'OK'
    except:
        return 'Fail'

def getFrom(key,val):
    try:
        return data[key]
    except:
        return ''

def appendDictionary(key,val):
    try:
        valueExsist = data[key]
        data[key] = val
        return 'OK'
    except:
        return 'fail'

def sliceDictionary(key,val):
    try:
        print('key',key)
        print(data)
        value = data[key]
        indices = val.split(':')
        print(value)
        data[key] = value[int(indices[0]):int(indices[1])]
        return 'OK'
    except:
        return 'fail'

def executeOperation(operation,key,val):
    function_launch = {
        'put': addToDictionary,
        'get': getFrom,
        'append': appendDictionary,
        'slice': sliceDictionary
    }

    return function_launch[operation](key, val)

def parseString(inp2):
    inp = str(inp2,'utf-8')[:-1]
    opKeyVal = inp.split('(')
    operation = opKeyVal[0]
    print('operation')
    keyVal = opKeyVal[1].split(',')
    key = keyVal[0][1:-1]
    value = keyVal[1][1:-1]

    return  operation,key,value


def doOperation(inp):
    operation,key,value = parseString(inp)
    print(operation)
    print(key)
    print(value)
    ret = executeOperation(operation,key,value)
    print(ret)


#put('jedi,'luke skywalker); slice('jedi','0:4'); get('jedi')
inp = b"put('jedi','luke skywalker')"
doOperation(inp)
print(data)
inp = b"slice('jedi','3:10')"
doOperation(inp)
print(data)
inp = b"get('jedi')"
doOperation(inp)


print(data)



