# -*- generated by 1.0.9 -*-
import da
PatternExpr_351 = da.pat.TuplePattern([da.pat.ConstantPattern('requestConfiguration')])
PatternExpr_356 = da.pat.FreePattern('p')
PatternExpr_792 = da.pat.TuplePattern([da.pat.FreePattern('Configuration')])
PatternExpr_797 = da.pat.FreePattern('p')
PatternExpr_867 = da.pat.TuplePattern([da.pat.FreePattern('result'), da.pat.FreePattern('resultShuttle')])
PatternExpr_916 = da.pat.TuplePattern([da.pat.FreePattern('result'), da.pat.FreePattern('reqID'), da.pat.FreePattern('resultShuttle')])
PatternExpr_925 = da.pat.FreePattern('tail')
PatternExpr_1193 = da.pat.TuplePattern([da.pat.ConstantPattern('initial'), da.pat.FreePattern('clientId'), da.pat.FreePattern('requestID'), da.pat.FreePattern('signedRequestStatement')])
PatternExpr_1204 = da.pat.FreePattern('c')
PatternExpr_1354 = da.pat.TuplePattern([da.pat.FreePattern('clientId'), da.pat.FreePattern('requestID'), da.pat.FreePattern('shuttle'), da.pat.FreePattern('typeOfRequest'), da.pat.FreePattern('replicaType')])
PatternExpr_1367 = da.pat.FreePattern('previousReplica')
PatternExpr_1613 = da.pat.TuplePattern([da.pat.ConstantPattern('retransmission'), da.pat.FreePattern('clientId'), da.pat.FreePattern('requestID'), da.pat.FreePattern('signedRequestStatement')])
PatternExpr_1624 = da.pat.FreePattern('c')
PatternExpr_1631 = da.pat.TuplePattern([da.pat.FreePattern('result'), da.pat.FreePattern('resultShuttle')])
PatternExpr_1638 = da.pat.FreePattern('nextReplica')
_config_object = {}
import sys
import nacl.utils
from random import *
import nacl.encoding
import nacl.signing

def readConfigFile():
    config = dict()
    with open('config.csv', 'r') as f:
        for line in f:
            if (not (line[0] == '#')):
                (key, sep, val) = line.partition('=')
                if (not (len(sep) == 0)):
                    val = val.strip()
                    config[key.strip()] = (int(val) if str.isdecimal(val) else val)
    return config

def signTheStatement(signing_key, message):
    return signing_key.sign(message)
    self.output('-------------Signed the message---------------------------')

def decodeVerifyKey(verify_key_hex):
    return nacl.signing.VerifyKey(verify_key_hex, encoder=nacl.encoding.HexEncoder)

def verifyTheStatement(verify_key, signed):
    return verify_key.verify(signed)

class Olympus(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_0', PatternExpr_351, sources=[PatternExpr_356], destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_350])])

    def setup(self, **rest_2213):
        super().setup(**rest_2213)
        self.output('---------------ENTERING Olymus:setup ---------------------')
        self.output(self._id)
        self._state.terminate = False
        self._state.client_signing_keys = dict()
        self._state.client_verify_keys_hex = dict()
        self._state.replica_signing_keys = dict()
        self._state.replica_verify_keys_hex = dict()
        self.initialSetup()

    def run(self):
        super()._label('_st_label_344', block=False)
        _st_label_344 = 0
        while (_st_label_344 == 0):
            _st_label_344 += 1
            if self._state.terminate:
                _st_label_344 += 1
            else:
                super()._label('_st_label_344', block=True)
                _st_label_344 -= 1
        self.output('terminating')

    def readGlobalConfigFile(self):
        self.output('---------------ENTERING Olymus:readGlobalConfigFile ---------------------')
        globalConfiggg = readConfigFile()
        self.output('----EXIT-----')

    def initialSetup(self):
        self.output('---------------ENTERING Olymus:initialSetup ---------------------')
        self._state.globalConfig = readConfigFile()
        noOfClients = self._state.globalConfig['num_client']
        noOfReplicas = ((2 * self._state.globalConfig['t']) + 1)
        (self._state.client_signing_keys, self._state.client_verify_keys_hex) = self.createKeys(noOfClients)
        self._state.clients = self.createClientProcesses(self._state.client_signing_keys)
        (self._state.replica_signing_keys, self._state.replica_verify_keys_hex) = self.createKeys(noOfReplicas)
        self._state.replicas = self.createReplicaProcesses(self._state.replica_signing_keys, self._state.clients, self._state.replica_verify_keys_hex)

    def createKeys(self, number):
        self.output('---------------ENTERING Olymus:createKeys ---------------------')
        signing_keys = dict()
        verify_keys_hex = dict()
        for i in range(number):
            signing_key = nacl.signing.SigningKey.generate()
            verify_key = signing_key.verify_key
            verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)
            signing_keys[i] = signing_key
            verify_keys_hex[i] = verify_key_hex
        return (signing_keys, verify_keys_hex)

    def createClientProcesses(self, client_signing_keys):
        tempClients = []
        self.output('---------------ENTERING CLIENT CREATE PROCESS---------------------')
        noOfClients = self._state.globalConfig['num_client']
        hosts = self._state.globalConfig['hosts'].split(';')
        client_hosts = self._state.globalConfig['client_hosts'].split(';')
        for i in range(noOfClients):
            processAtNode = ('Client' + str(i))
            client = self.new(Client, at=processAtNode)
            self._setup(client, (self._id, i, client_signing_keys[i]))
            self._start(client)
            tempClients.insert(i, (client, self._state.client_verify_keys_hex[i]))
        return tempClients

    def createReplicaProcesses(self, replica_signing_keys, clients, replica_verify_keys_hex):
        self.output('---------------ENTERING REPLICA CREATE PROCESS---------------------')
        tempReplicas = dict()
        noOfReplicas = ((2 * self._state.globalConfig['t']) + 1)
        hosts = self._state.globalConfig['hosts'].split(';')
        replica_hosts = self._state.globalConfig['replica_hosts'].split(';')
        for i in range(noOfReplicas):
            processAtNode = ('Replica' + str(i))
            replica = self.new(Replica, at=processAtNode)
            tempReplicas[i] = (replica, replica_verify_keys_hex[i])
        for i in range(noOfReplicas):
            self._setup(tempReplicas[i][0], (self._id, i, 'ACTIVE', replica_signing_keys[i], clients, tempReplicas))
            self._start(tempReplicas[i][0])
        return tempReplicas

    def createConfiguration(self):
        pass

    def setupProcesses(self):
        self.output('---------------ENTERING setupProcesses ---------------------')
        for i in range(noOfClients):
            self._setup(client[i], args=(self._id,))

    def startProcesses(self):
        self.output('---------------ENTERING startProcesses ---------------------')
        for i in range(noOfClients):
            self._start(client[i])

    def _Olympus_handler_350(self, p):
        self.output('---------------ENTERING olympus:receieve:requestConfiguration---------------------')
        self.output(p)
        Configuration = self._state.replicas
        self.send((Configuration,), to=p)
    _Olympus_handler_350._labels = None
    _Olympus_handler_350._notlabels = None

class Client(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._ClientReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_792, sources=[PatternExpr_797], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_791]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_867, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_916, sources=[PatternExpr_925], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_915])])

    def setup(self, p, clientID, client_signing_key, **rest_2213):
        super().setup(p=p, clientID=clientID, client_signing_key=client_signing_key, **rest_2213)
        self._state.p = p
        self._state.clientID = clientID
        self._state.client_signing_key = client_signing_key
        self._state.terminate = False
        self._state.replicas = dict()
        self._state.TIMEOUT = 0
        self._state.globalConfig = dict()
        self._state.noOfReplicas = 0

    def run(self):
        self.output('---------------ENTERING client:run---------------------')
        self.send(('requestConfiguration',), to=self._state.p)
        self._state.globalConfig = readConfigFile()
        self._state.TIMEOUT = self._state.globalConfig['client_timeout']
        self._state.noOfReplicas = ((2 * self._state.globalConfig['t']) + 1)
        super()._label('_st_label_787', block=False)
        _st_label_787 = 0
        while (_st_label_787 == 0):
            _st_label_787 += 1
            if self._state.terminate:
                _st_label_787 += 1
            else:
                super()._label('_st_label_787', block=True)
                _st_label_787 -= 1

    def getOperations(self):
        return self._state.globalConfig[(('workload[' + str(self._state.clientID)) + ']')]

    def sendRequest(self, requestID, operation, receiver, typeOfRequest):
        self.output(operation)
        requestStatement = bytes(str(operation.strip()), 'utf8')
        self.output(requestStatement)
        signedRequestStatement = signTheStatement(self._state.client_signing_key, requestStatement)
        if (typeOfRequest == 'initial'):
            self.send((typeOfRequest, self._state.clientID, requestID, signedRequestStatement), to=receiver[0])
        elif (typeOfRequest == 'retransmission'):
            for replicaNo in range(self._state.noOfReplicas):
                self.send((typeOfRequest, self._state.clientID, requestID, signedRequestStatement), to=receiver[replicaNo][0])
        self.output(signedRequestStatement)

    def returnRandomNumber(self):
        return randint(1, 10000)

    def verifyResultProofs(self, tempResultProof):
        self.output('-----------------------verifyResultProofs---------------------------')
        numOfRP = len(tempResultProof)
        i = 0
        verified = ''
        while (i < numOfRP):
            temp_verify_key = decodeVerifyKey(self._state.replicas[i][1])
            tempSignedRP = tempResultProof[i]
            try:
                verified = verifyTheStatement(temp_verify_key, tempSignedRP)
                verified = 'True'
            except:
                verified = 'False'
            i += 1
        return verified

    def _Client_handler_791(self, Configuration, p):
        self.output('---------------ENTERING client:receive:Configuration---------------------')
        self._state.replicas = Configuration
        self.output(len(Configuration))
        for x in range(len(Configuration)):
            print('Replica:', Configuration[x])
        operations = self.getOperations().split(';')
        self.output(operations)
        for i in range(len(operations)):
            self.output('------SENDING REQUESTS LOOP----------------')
            requestID = self.returnRandomNumber()
            self.output('requestID: ', requestID)
            self.output('------SENDING REQUESTS LOOP----------------')
            self.sendRequest(requestID, operations[i], Configuration[0], 'initial')
            super()._label('_st_label_864', block=False)
            result = resultShuttle = None

            def ExistentialOpExpr_865():
                nonlocal result, resultShuttle
                for (_, _, (result, resultShuttle)) in self._ClientReceivedEvent_1:
                    if (int(resultShuttle[0]) == requestID):
                        return True
                return False
            _st_label_864 = 0
            self._timer_start()
            while (_st_label_864 == 0):
                _st_label_864 += 1
                if ExistentialOpExpr_865():
                    self.output('received result')
                    continue
                    _st_label_864 += 1
                elif self._timer_expired:
                    self.output('Send Retransmission Request.')
                    self.sendRequest(requestID, operations[i], Configuration, 'retransmission')
                    continue
                    _st_label_864 += 1
                else:
                    super()._label('_st_label_864', block=True, timeout=self._state.TIMEOUT)
                    _st_label_864 -= 1
            else:
                if (_st_label_864 != 2):
                    continue
            if (_st_label_864 != 2):
                break
        self.send(('Received Configuration',), to=p)
    _Client_handler_791._labels = None
    _Client_handler_791._notlabels = None

    def _Client_handler_915(self, result, reqID, resultShuttle, tail):
        self.output('-------------------- Received Result Shuttle from Tail-------------------------')
        resultVerified = self.verifyResultProofs(resultShuttle[2])
        self.output(resultVerified)
        self.output(resultShuttle)
    _Client_handler_915._labels = None
    _Client_handler_915._notlabels = None

class Replica(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_0', PatternExpr_1193, sources=[PatternExpr_1204], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_1192]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_1', PatternExpr_1354, sources=[PatternExpr_1367], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_1353]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_2', PatternExpr_1613, sources=[PatternExpr_1624], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_1612]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_3', PatternExpr_1631, sources=[PatternExpr_1638], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_1630])])

    def setup(self, p, i, Mode, replica_signing_key, clients, replicas, **rest_2213):
        super().setup(p=p, i=i, Mode=Mode, replica_signing_key=replica_signing_key, clients=clients, replicas=replicas, **rest_2213)
        self._state.p = p
        self._state.i = i
        self._state.Mode = Mode
        self._state.replica_signing_key = replica_signing_key
        self._state.clients = clients
        self._state.replicas = replicas
        self._state.terminate = False
        self._state.data = dict()
        self._state.replicaHistory = dict()
        self._state.resultCache = dict()
        self._state.slot = 0
        self._state.globalConfig = dict()
        self._state.noOfReplicas = 0

    def run(self):
        self.output('---------------------ENTERING Replica:run-----------------------')
        self.output(self._state.p)
        self.output('------------------printing replicas with their public keys------------')
        self._state.globalConfig = readConfigFile()
        self._state.noOfReplicas = ((2 * self._state.globalConfig['t']) + 1)
        super()._label('_st_label_1186', block=False)
        _st_label_1186 = 0
        while (_st_label_1186 == 0):
            _st_label_1186 += 1
            if self._state.terminate:
                _st_label_1186 += 1
            else:
                super()._label('_st_label_1186', block=True)
                _st_label_1186 -= 1
        self.output('--------------------Something------------------------')

    def assignSlot(self, s, o):
        self._state.replicaHistory[s] = ('order', o)
        self.output('---------------inside assignslot----')
        self.output(self._state.replicaHistory[s])

    def createStatements(self, s, o, r):
        self.output('-----------------------createStatements---------------------------')
        orderStatement = bytes(str(((("'order';" + str(s)) + ';') + o.decode('utf-8'))), 'utf8')
        self.output(orderStatement)
        signedOrderStatement = signTheStatement(self._state.replica_signing_key, orderStatement)
        hashedR = self.hashResult(r)
        resultStatement = bytes(((("'result';" + str(s)) + ';') + hashedR), 'utf8')
        signedResultStatement = signTheStatement(self._state.replica_signing_key, resultStatement)
        return (signedOrderStatement, signedResultStatement)

    def verifyOrderProofs(self, tempOrderProof):
        self.output('-----------------------verifyOrderProofs---------------------------')
        numOfOP = len(tempOrderProof)
        self._state.i = 0
        verified = ''
        while (self._state.i < numOfOP):
            temp_verify_key = decodeVerifyKey(self._state.replicas[self._state.i][1])
            tempSignedOP = tempOrderProof[self._state.i]
            try:
                verified = verifyTheStatement(temp_verify_key, tempSignedOP)
            except:
                verified = 'False'
            self._state.i += 1
        return verified

    def verifyResultProofs(self, tempResultProof):
        self.output('-----------------------verifyResultProofs---------------------------')
        numOfRP = len(tempResultProof)
        tempi = 0
        verified = ''
        while (tempi < numOfRP):
            temp_verify_key = decodeVerifyKey(self._state.replicas[tempi][1])
            tempSignedRP = tempResultProof[tempi]
            try:
                verified = verifyTheStatement(temp_verify_key, tempSignedRP)
                verified = 'True'
            except:
                verified = 'False'
            tempi += 1
        return verified

    def checkSlotInHistory(self, slot, operation):
        inHistory = 'false'
        self.output('----------------checkSlotInHistory---------------------')
        self.output('slot', slot)
        try:
            op = self._state.replicaHistory[slot][0]
            self.output('op', op)
            if (operation == op):
                inHistory = 'validOperation'
            elif (not (operation == op)):
                inHistory = 'invalidOperation'
        except:
            pass
        return inHistory

    def checkForHoles(self, slot):
        holes = False
        if (slot == 0):
            return holes
        try:
            op = self._state.replicaHistory[(slot - 1)]
        except:
            holes = True
        return holes

    def unionOrderProofs(self, orderProof, signedOS):
        self.output('-----------------------unionOrderProofs---------------------------')
        return orderProof.append(signedOS)

    def unionResultProofs(self, resultProof, signedRS):
        self.output('-----------------------unionResultProofs---------------------------')
        return resultProof.append(signedRS)

    def appendToReplicaHistory(self, s, o, orderProof):
        self._state.replicaHistory[s] = (o.decode('utf-8'), orderProof)

    def appendToResultCache(self, resultSh):
        self._state.resultCache[resultSh[0]] = (resultSh[1], resultSh[2])

    def getResultFromResultCache(self, requestID):
        try:
            tempResult = self._state.resultCache[requestID]
            return (requestID, tempResult[0], tempResult[1])
        except KeyError:
            return 'NoResult'

    def hashResult(self, r):
        return r

    def parseTheUnsignedStatement(self, unSignedRequestStatement):
        self.output('-----------------------parseTheUnsignedStatement---------------------------')
        inp = str(unSignedRequestStatement, 'utf-8')[:(- 1)]
        self.output(inp)
        opKeyVal = inp.split('(')
        operation = opKeyVal[0]
        keyVal = opKeyVal[1].split(',')
        key = keyVal[0][1:(- 1)]
        value = ''
        if (not (operation == 'get')):
            value = keyVal[1][1:(- 1)]
        return (operation, key, value.strip())

    def addToDictionary(self, key, val):
        self.output('-----------------------addToDictionary---------------------------')
        self._state.data[key] = val
        return 'OK'

    def getFrom(self, key, val):
        self.output('-----------------------getFrom---------------------------')
        try:
            return self._state.data[key]
        except:
            return ''

    def appendDictionary(self, key, val):
        self.output('-----------------------appendDictionary---------------------------')
        self._state.data[key] = val
        return 'OK'

    def sliceDictionary(self, key, val):
        self.output('-----------------------sliceDictionary---------------------------')
        value = self._state.data[key]
        self._state.data[key] = value[val]
        return 'OK'

    def executeOperation(self, operation, key, val):
        self.output('-----------------------executeOperation---------------------------')
        function_launch = {'put': self.addToDictionary, 'get': self.getFrom, 'append': self.appendDictionary, 'slice': self.sliceDictionary}
        return function_launch[operation](key, val)

    def _Replica_handler_1192(self, clientId, requestID, signedRequestStatement, c):
        self.output('---------------------ENTERING Replica:receive:signedRequestStatement-----------------------')
        self.output('---------------The signed statement with clientID---------------------')
        self.output(signedRequestStatement)
        orderProof = list()
        resultProof = list()
        temp_verify_key = decodeVerifyKey(self._state.clients[clientId][1])
        unSignedRequestStatement = ''
        operation = ''
        if (self._state.Mode == 'ACTIVE'):
            self.output('------------clientId------------:', clientId)
            self.output('-----------------------unsigning signedRequestStatement---------------------------')
            verified = ''
            try:
                verified = verifyTheStatement(temp_verify_key, signedRequestStatement)
            except:
                verified = 'Not verified'
            self.output(verified)
            (operation, key, value) = self.parseTheUnsignedStatement(verified)
            result = self.executeOperation(operation, key, value)
            self.output(result)
            (signedOrderStatement, signedResultStatement) = self.createStatements(self._state.slot, verified, result)
            self.output('------------------------Signed Order Statement for union-----------------')
            self.output(signedOrderStatement)
            orderProof.append(signedOrderStatement)
            resultProof.append(signedResultStatement)
            shuttle = (orderProof, resultProof)
            self.appendToReplicaHistory(self._state.slot, verified, orderProof)
            self._state.slot += 1
            self.output(shuttle)
            self.output(self._state.data)
        else:
            self.output('Replica is not active')
        self.output('---------------sending shuttle to next replica-------------')
        self.send((clientId, requestID, shuttle, 'initial', 'nonhead'), to=self._state.replicas[(self._state.i + 1)][0])
        self.output('----------------- I ended ----------------------')
    _Replica_handler_1192._labels = None
    _Replica_handler_1192._notlabels = None

    def _Replica_handler_1353(self, clientId, requestID, shuttle, typeOfRequest, replicaType, previousReplica):
        self.output('---------------The  shuttle from previous replica--------------------')
        if ((self._state.i < self._state.noOfReplicas) and (self._state.Mode == 'ACTIVE')):
            tempOrderProof = shuttle[0]
            tempResultProof = shuttle[1]
            self.output('----------------OUTPUT TOTAL ORDER PROOFS------------')
            self.output(tempOrderProof)
            verified = self.verifyOrderProofs(tempOrderProof)
            resultsVerified = self.verifyResultProofs(tempResultProof)
            if ((not (verified == 'False')) or (not (resultsVerified == 'False'))):
                tempOrderStatement = verified.decode('utf-8').split(';')
                self.output(tempOrderStatement)
                tempSlot = tempOrderStatement[1]
                tempSignedStatement = tempOrderStatement[2]
                self.output(tempSlot)
                self.output(tempSignedStatement)
                inHistory = self.checkSlotInHistory(int(tempSlot), tempSignedStatement)
                self.output(inHistory)
                holes = self.checkForHoles(int(self._state.slot))
                self.output(holes)
                if ((inHistory == 'false') and (holes == False)):
                    (operation, key, value) = self.parseTheUnsignedStatement(bytes(tempSignedStatement, 'utf-8'))
                    result = self.executeOperation(operation, key, value)
                    self.output('------------DATA DICTIONARY----------')
                    self.output('Data', self._state.data)
                    (tempSignedOrderStatement, tempSignedResultStatement) = self.createStatements(tempSlot, bytes(tempSignedStatement, 'utf-8'), result)
                    self.output('Signed Order Statement', tempSignedOrderStatement)
                    tempOrderProof.append(tempSignedOrderStatement)
                    tempResultProof.append(tempSignedResultStatement)
                    self.appendToReplicaHistory(self._state.slot, verified, tempOrderProof)
                    shuttle = (tempOrderProof, tempResultProof)
                    if (not (self._state.i == (self._state.noOfReplicas - 1))):
                        self.output(self._state.replicas[(self._state.i + 1)])
                        self.send((clientId, requestID, shuttle, 'initial', 'nonhead'), to=self._state.replicas[(self._state.i + 1)][0])
                    elif (self._state.i == (self._state.noOfReplicas - 1)):
                        resultShuttle = (requestID, result, tempResultProof)
                        self.appendToResultCache(resultShuttle)
                        self.send(('result', resultShuttle), to=self._state.clients[clientId][0])
                        self.send(('result', resultShuttle), to=self._state.replicas[(self._state.i - 1)][0])
                    else:
                        self.output('------------------------JUST CHILL------------------------')
        self.output('-------------------- I ended -------------------------')
    _Replica_handler_1353._labels = None
    _Replica_handler_1353._notlabels = None

    def _Replica_handler_1612(self, clientId, requestID, signedRequestStatement, c):
        self.output('---------------------ENTERING Replica:receive:retransmission-----------------------')
    _Replica_handler_1612._labels = None
    _Replica_handler_1612._notlabels = None

    def _Replica_handler_1630(self, result, resultShuttle, nextReplica):
        self.output('-------------------- Received Result Shuttle from Next Replica -------------------------', level=20)
        self.output(result)
        resultVerification = self.verifyResultProofs(resultShuttle[2])
        if (resultVerification == 'True'):
            self.appendToResultCache(resultShuttle)
        else:
            self.output('--------------------- Proof of Misbehaviour---------------', level=40)
        self.output(resultVerification)
        if (not (self._state.i == 0)):
            self.send(('result', resultShuttle), to=self._state.replicas[(self._state.i - 1)][0])
    _Replica_handler_1630._labels = None
    _Replica_handler_1630._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])

    def run(self):
        self.output('---------------ENTERING main---------------------')
        olympus = self.new(Olympus, args=())
        self._start(olympus)
