from flask import render_template, request, Flask, redirect, url_for

from drone import drone
from cloud import cloud
from block import block
from cloud import cloudtxnlistbefore
from cloud import transactioncountbefore
from cloud import cloudtxnlistafter
from cloud import transactioncountafter

from blockchain import totaltransactioncount
from block import blocks
from block import transactions



from drone import droneDetailsList

from googleCloud import upload_files

# from time import time
import random
import winsound

initE = 100
threshold = 1/3
alltxn=[]
message=[]
nwtxn=[]





def broadcast(obj, network, CLOUD, I):
    if(isinstance(obj, block)):
        for D in network['drones']:
            D.insert(obj)
        network['lastBlock'] = obj

    elif(isinstance(obj, dict)):
        network['txns'].append(obj)
        CLOUD.send(obj)  # Each transaction is shared with cloud
        if(len(network['txns']) == 6):
            miner = random.choice(network['heads'])
            BLOC, unverified = miner.createBlock(network['txns'])
            network['txns'].clear()
            broadcast(BLOC, network, CLOUD, I)
            I.extend(unverified)


def updateCHeads():
    for d in cHeads:
        d.head = False
    cHeads.clear()
    for z in zones:

        p = 1 / len(zones[z])
        r = random.randint(1 / p)
        k = len(zones)

        nH = None
        pre = 0
        # I'm still not sure why we are doing,
        # for d in zones[z]:
        #     rE = d.rE
        #     T = p * rE * k / initE
        #     den = 1 - p * (r % (1 / p))
        #     PRE = T / den
        # PRE = rE-Econsumed-pathLoss
        # if (PRE > pre):
        #     pre = T
        #     nH = d
        ####-inner for-#####
        # nH.head = True
        cHeads.append(nH)
    ###-outer for-###
    print("New cluster Heads appointed.")


CLOUD = cloud()
# N=int(input("Enter no.of IoT drones:"))
N = 12
invalidTxns = []
dList = [drone(i % 4) for i in range(N)]
zones = {
    0: [],
    1: [],
    2: [],
    3: []
}
cHeads = []
for d in dList:
    zones[d.zone].append(d)
for eachZone in zones:
    node = random.choice(zones[eachZone])
    node.head = True
    cHeads.append(node)


network = {
    'drones': dList,
    'heads': cHeads,
    'lastBlock': None,
    'txns': []
}



winsound.Beep(600, 400)
# start=time()
for S in dList:
    msg = 'X'
    signature = S.getSignature(msg)
    oneTxnList = [{"Sender": S, "Message": msg, "Signature": signature}]
    miner = dList[0]
    BLOC = miner.genesisBlock(oneTxnList)
    broadcast(BLOC, network, CLOUD, invalidTxns)


#print("TIME FOR GENESIS BLOCKS:")
print("Starting Up...")

winsound.Beep(600, 800)


images = [
    ["test-00.jpg", "test-01.jpg"],
    ["test-10.jpg", "test-11.jpg"]
]
Intrude = True
newList = network['drones'].copy()
if(Intrude):
    newList.append(drone(-1))


# start=time()
for x in range(10):
    for y in range(10):
        garbage = random.choices(
            "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", k=20)
        msg = "".join(garbage)
        S = random.choice(newList)
        # result=detectImage(images[x][y])
        result = [{'percentage_probability': msg}]
        if(result):
            # winsound.Beep(600, 10)
            dir = random.random() * 360
            dir = "{:.2f}".format(dir)
            msg = str(x)+"|"+str(y)+"|"+dir+"|"
            msg += str(result[0]['percentage_probability'])
            signature = S.getSignature(msg)
            txn = {"Sender": S, "Message": msg, "Signature": signature}
            broadcast(txn, network, CLOUD, invalidTxns)
#            message.append({"X":str(x),"Y":str(y),"Direction":dir,"Probability":str(result[0]['percentage_probability'])})
            
            
            

# print("TOTAL TIME:",time()-start)
winsound.Beep(600, 700)

print("-"*90, "IDENTITY", "-"*90)
#for D in newList:
    #print("Drone.no:", D.num)
    #print("Drone-ID:", D.address)
    #for k, v in D.idProof.items():
        #print(k+":", v)
    #print()

print("-"*90, "DRONE DETAILS", "-"*90)
#for i in newList:
    #print(i)

print("-"*90, "BLOCKCHAIN", "-"*90)
#print(dList[0].chain)

print("-"*90, "IN CLOUD", "-"*90)
cloudtransactionlistbefore=CLOUD.getTransactionsbefore()



print("\n\nVerifying transactions in cloud.....")
CLOUD.verify(network['lastBlock'].mTree)
print("Verification done!\n\n")

print("-"*90, "IN CLOUD", "-"*90)
cloudtransactionlistafter=CLOUD.getTransactionsafter()
print("\n\n")

print("-"*90, "NETWORK", "-"*90)
for T in network['txns']:
    #print("Sender: ", T['Sender'].address[:60], end=",  ")
    #print("Message: ", T['Message'], end=",  ")
   #print("Signature: ", T['Signature'].hex()[:60])
    
    nwtxn.append(T)
    
print("\n\n")


#Printing all valid transactions
print("-"*90, "ALL TXNS", "-"*90)
for T in dList[0].chain.allTxns:
    #print("Sender: ", T['Sender'].address[:60], end=",  ")
    #print("Message: ", T['Message'], end=",  ")
    #print("Signature: ", T['Signature'].hex()[:60])
    
    alltxn.append(T)
    
    message.append(T['Message'].split('|'))



#Printing Residual Energies
#for d in dList:
    #print(d.rE)










#flask Section
app = Flask(__name__)

@app.route('/')
def home():
   return render_template("home.html")
    
@app.route('/allTransactions')
def allTransactions():
    return render_template("allTransactions.html",values=alltxn)
        
@app.route('/viewMessageDetails')
def viewMessageDetails():
    return render_template("viewMessageDetails.html",value=message)

@app.route('/viewNetworkTransactions')
def viewNetworkTransactions():
    return render_template("viewNetworkTransactions.html",value=nwtxn)

@app.route('/viewCloudTransactionsbefore')
def viewCloudTransactionsbefore():
    return render_template("viewCloudTransactionsbefore.html", txncount=transactioncountbefore, value=cloudtransactionlistbefore)

CLOUD.verify(network['lastBlock'].mTree)

@app.route('/viewCloudTransactionsafter')
def viewCloudTransactionsafter():
    
    text_file = open("C:/Flask/IntegrationProject/alert.txt", "w+")
    text_file.write("---Sender---"+"\t"+"---Message---"+"\t"+"---Signature---"+"\n\n")
    
    
    for T in cloudtransactionlistafter:
      
        message=T['Sender'].address+"\t\t"+T['Message']+"\t\t"+T['Signature'].hex()+"\n"
        text_file.write(message)
     
    
    
    upload_files()
    print("\n\nUploaded to Cloud\n\n")
    text_file.close()
    
    return render_template("viewCloudTransactionsafter.html", txncount=transactioncountafter, value=cloudtransactionlistafter)

@app.route('/viewDroneDetails')
def viewDroneDetails():
    return render_template("viewDroneDetails.html", value=droneDetailsList)

@app.route('/viewBlockchain')
def viewBlockchain():
    return render_template("viewBlockchain.html", txncount=totaltransactioncount, value=blocks, value2=transactions)

        



if __name__ == '__main__':
    app.run(debug=True);