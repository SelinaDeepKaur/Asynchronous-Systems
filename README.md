# Asynchronous-Systems
Byzantine Chain Replication

PLATFORM : 
Python version : 3.6.3
DistAlgo : 1.0.9
Hosts : Laptops without VM
OS : MAC/Windows
Platform for multiple hosts : Olympus and Clients - Windows, Replicas - MAC



INSTRUCTIONS : 
We have included 5 scenarios of test cases in separate folders.
1. Place ByzantineFaultTolerantProtocol.da file inside each folder
2. Each folder already has csv file needed to test the scenario
3. Open cmd in folder location and give the following commands

To run on single host:
OLYMPUS
python -m da -n olympus -f --logdir ./ --logfilename olympus.log --logfilelevel info ByzantineFaultTolerantProtocol.da

REPLICA
python -m da -n Replica0 -D -f --logdir ./ --logfilename replica0.log --logfilelevel info --message-buffer-size 6400000 ByzantineFaultTolerantProtocol.da
python -m da -n Replica1 -D -f --logdir ./ --logfilename replica1.log --logfilelevel info --message-buffer-size 6400000 ByzantineFaultTolerantProtocol.da
python -m da -n Replica2 -D -f --logdir ./ --logfilename replica2.log --logfilelevel info --message-buffer-size 6400000 ByzantineFaultTolerantProtocol.da

CLIENT
python -m da -n Client0 -D -f --logdir ./ --logfilename client0.log --logfilelevel info ByzantineFaultTolerantProtocol.da
python -m da -n Client1 -D -f --logdir ./ --logfilename client1.log --logfilelevel info ByzantineFaultTolerantProtocol.da
python -m da -n Client2 -D -f --logdir ./ --logfilename client2.log --logfilelevel info .daByzantineFaultTolerantProtocol

To run on multi host:
REPLICA
python -m da -H 172.24.21.17 -R 172.24.18.144 -n Replica0 -D -f --logdir ./ --logfilename replica0.log --logfilelevel info --message-buffer-size 6400000 ByzantineFaultTolerantProtocol.da
python -m da -H 172.24.21.17 -R 172.24.18.144 -n Replica1 -D -f --logdir ./ --logfilename replica1.log --logfilelevel info --message-buffer-size 6400000 ByzantineFaultTolerantProtocol.da
python -m da -H 172.24.21.17 -R 172.24.18.144 -n Replica2 -D -f --logdir ./ --logfilename replica2.log --logfilelevel info --message-buffer-size 6400000 ByzantineFaultTolerantProtocol.da

CLIENT
python -m da -H 172.24.18.144 -n Client0 -D -f --logdir ./ --logfilename client0.log --logfilelevel info ByzantineFaultTolerantProtocol.da
python -m da -H 172.24.18.144 -n Client1 -D -f --logdir ./ --logfilename client1.log --logfilelevel info ByzantineFaultTolerantProtocol.da
python -m da -H 172.24.18.144 -n Client2 -D -f --logdir ./ --logfilename client2.log --logfilelevel info ByzantineFaultTolerantProtocol.da

OLYMPUS
python -m da -H 172.24.18.144 -n olympus -f --logdir ./ --logfilename olympus.log --logfilelevel info ByzantineFaultTolerantProtocol.da

Here, I’m running 3 replicas on host - 172.24.21.17 (giving 172.24.18.144 as peer node)
olympus and 3 clients on another host - 172.24.18.144 (giving 172.24.21.17 as peer node)



WORKLOAD GENERATION :
We have written this function ‘generatePseudoRandomRequests’ which generates the Pseudo Random workload for us. Based on the noOfRequests it picks up the specified number of requests from a set of requests stored in ‘listofRequest’ variable.

def generatePseudoRandomRequests(rSeed,noOfRequests):
        output("--------------- Generating Pseudo Random Requests for Client --------------",level=20)
        listofRequest = ["put('movie','star')","append('movie',' wars')","get('movie')","put('jedi','luke    skywalker')","slice('jedi','0:4')","get('jedi')"]
        random.seed(rSeed)
        requests = random.sample(listofRequest,k=noOfRequests)        
        return requests

For seed value = 233 and no of requests = 5, as specified in the sample config file given to us.
The code picks up the same set of 5 requests from the list of requests everytime we set the seed value to 233 before retrieving those 5 requests into the ‘requests’ variable.
The  we return the requests stored in the ‘request’ variable to the client. It then sequentially sends those requests to replicas.



CONTRIBUTIONS :
CLIENT
Ask Olympus whether configuration changed (periodically or as needed) - Selina
Check that dictionary contains expected content at end of test case

OLYMPUS
Upon reconfiguration-request, send wedge requests - Selina
Validate wedged messages - Dinesh
Compute initial running state (incl. replica catch-up) - Dinesh
Create keys and create and setup processes for new replicas - Selina

REPLICA
Head: send reconfiguration-request if timeout waiting for result shuttle - Dinesh & Selina
Non-head: send reconfiguration-request if timeout waiting for result shuttle after forwarding request to head 
Detect provable misbehavior and send reconfiguration-request - Dinesh
Head: periodically initiate checkpoint, send checkpoint shuttle - Dinesh
Non-head: add signed checkpoint proof, send updated checkpoint shuttle - Dinesh
Handle completed checkpoint shuttle: validate completed checkpoint proof, delete history prefix, forward completed checkpoint proof - Dinesh
Handle catch-up message, execute operations, send caught-up message - Selina
Fault-injection: additional triggers for phase 3 - Selina 
Fault-injection: additional failures for phase 3 - Selina

MULTI-HOST EXECUTION 
Processes are spread across multiple hosts - Selina

CONFIGURATION FILES 
Support configuration files specified in project.txt - Dinesh

LOGS 
Detailed and readable logs - Dinesh

DOCUMENTATION 
README and testing.txt - Selina

MAIN FILES : our main file ping.da in ./src/ contains all the code for olympus client and replica



CODE SIZE :
(1a) Algorithm (LOC) :1785
       Other (LOC) :654
       Total (LOC) :2334	
(1b) We used CLOC (https://github.com/AlDanial/cloc) to count the number of blanks lines.
       Then we used the find feature of sublime to calculate the number of comments (lines beginning with #) in it.
        To calculate other functionalities: - We searched for keyword ‘output’ the total of which was 430.
        To calculate fault injections: - We searched for keyword fstatus,getAction, to calculate fault-triggers:- 105+ we searched for key word if fstatus != ‘not found’ to calculate fault actions:- 119 bringing total to 224
(2) Algorithm code (LOC):1785
     Other functionality interleaved with it (LOC) : 529

LANGUAGE FEATURE USAGE :
Numbers of list comprehensions : 27
Dictionary comprehensions : 34
Set comprehensions : 0 
Aggregations : 0
Quantifications :8



