data = dict()

def addToDictionary(key,val):
    data[key]=val
    return 'OK'
def getFrom(key):
    try:
        return data[key]
    except:
        return ''

def appendDictionary(key,val):
    data[key] = val
    return 'OK'

def sliceDictionary(key,val):
    value = data[key]
    data[key] = value[val]
    return 'OK'

def executeOperation(operation,key,val):
    function_launch = {
        'put': addToDictionary,
        'get': getFrom,
        'slice': appendDictionary,
        'append': sliceDictionary
    }

    return function_launch[operation](key, val)

def parseString(inp2):
    inp = str(inp2,'utf-8')[:-1]
    opKeyVal = inp.split('(')
    operation = opKeyVal[0]
    keyVal = opKeyVal[1].split(',')
    key = keyVal[0][1:-1]
    value = keyVal[1][1:-1]

    return  operation,key,value


inp = b"put('movie','star')"
operation,key,value = parseString(inp)
print(operation)
print(key)
print(value)
ret = executeOperation(operation,key,value)


print(ret)
print(data)
