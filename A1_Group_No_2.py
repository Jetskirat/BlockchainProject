# Note : Generated QR code will be saved as an image in the same directory as the code file

import hashlib
import datetime
import random
import time
import qrcode
from colorama import Fore

'''Initial declarations'''

distributer_list = []
client_list = []
blockchain = []
transaction_list = []
m_id = 0
d_id = 0
c_id = 0



'''Contructing a function to calculate the merkle tree from input hashes'''

def merkle_parent_level(hashes):
    if len(hashes)%2 == 1:
        hashes.append(hashes[-1])
    
    parent_level = []

    for i in range(0, len(hashes), 2):
        parent_lvl = hashlib.sha256((hashes[i]+hashes[i+1]).encode()).hexdigest()
        parent_level.append(parent_lvl)
    
    return parent_level


def merkle_root(hashes):

    c_lvl = hashes

    while len(c_lvl) > 1:
        c_lvl = merkle_parent_level(c_lvl)

    return c_lvl[0]





'''Defining a class for transactions'''

class transaction:
    
    def __init__(self, m_id, d_id, c_id):
        self.m_id = m_id
        self.d_id = d_id
        self.c_id = c_id
        self.prod_id = 0
        self.amount = 0
        self.timestamp = []
        self.dis_dispatched = False
        self.client_recieved = False
        self.complete = False
        self.elapsed_time = 0
        self.mined = False





'''Defining a class for blocks in the blockchain'''

class block:

    def __init__(self, previous_block_hash, transaction_lists):
        self.previous_block_hash = previous_block_hash
        self.transaction_lists = transaction_lists
        self.timestamp = 0

        tran_string = ''
        for i in range(2):
            tran_string += str(transaction_lists[i].m_id)
            tran_string += ' '
            tran_string += str(transaction_lists[i].d_id)
            tran_string += ' '
            tran_string += str(transaction_lists[i].c_id)
            tran_string += ' '
            tran_string += str(transaction_lists[i].prod_id)
            tran_string += ' '
            tran_string += str(transaction_lists[i].timestamp[0])
            tran_string += ' '
            tran_string += str(transaction_lists[i].timestamp[1])
            tran_string += ' '
            tran_string += str(transaction_lists[i].timestamp[2])
            tran_string += '\n'


        self.block_data = tran_string + '-' + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.merkle_root = merkle_root(tran_string)



'''Defining a class for distributers and clients'''

class distributer:

    def __init__(self, id, deposit):
        self.id = id
        self.busy = False
        self.key = 0
        self.deposit = deposit

class client:

    def __init__(self, id, key, deposit):
        self.id = id
        self.considered = False
        self.key = key
        self.deposit = deposit
        self.recieved = 0



'''Main body'''

print(Fore.WHITE + "Welcome to the Supply Chain managment system.\n")

m_id = int(input(Fore.WHITE + 'Enter the Manufacturer ID to start the process : '))

while 1:

    choice = int(input(Fore.WHITE + """\n\nEnter the number for which input to execute:\n
            1)Enter into the list of distributers.\n
            2)Make a new product request as a client.\n
            3)Dispatch the product as Distributer.\n
            4)Collect the product as Client.\n
            5)Track the transaction by QR code\n
            6)Mine a new block.\n
            7)Raise a complaint as Distributor.\n
            8)Raise a complaint as Client.\n
        """))


    if choice == 1:

        d_id = int(input('\nEnter Distributer ID : '))

        count = 0
        for last_temp in distributer_list:
            if d_id == last_temp.id:
                print("\nDistributor already exists.")
                count += 1
                break
        
        if count > 0:
            continue

        distributer_list.append(distributer(d_id, 1000))

        print("\nMaking a security deposit of Rs 1000 in the system.")
        time.sleep(1)

    elif choice == 2:

        time.sleep(1)

        # Checking if there availabe distributers  
        if distributer_list == []:
            print("\nPlease enter a distributer first.")
            continue
        
        free_count = 0
        for dis in distributer_list:
            if dis.busy == False:
                free_count += 1
            
        if free_count == 0:
            print("\nNo distributer is available at the moment, please try again later.")
            continue
        
        c_id = int(input('\nEnter Client ID : '))
        client_key = random.randint(1000, 9999)
        client_list.append(client(c_id, client_key, 1000))

        print("\nMaking a security deposit of Rs 1000 in the system.")

        time.sleep(1)

        print(Fore.CYAN + "\nThe product key for the client is %2d." % (client_key))

        # Choosing a random available distributer from the distributer list
        dis_temp = []
        for dis in distributer_list:
            if dis.busy == False and dis.deposit > 0:
                dis_temp.append(dis)
                
        selected_distributor = random.choice(dis_temp)
        
        dis_key = random.randint(1000,9999)

        time.sleep(1)

        print("\nThe product key for the distributer is %2d." % (dis_key))


        for dis2 in distributer_list:
            if dis2.id == selected_distributor.id:
                dis2.busy = True
                dis2.key = dis_key

        
        # Generating a unique ID for the product
        product_id = random.randint(0,50)


        # Initiating a transaction

        initial_transaction = transaction(m_id, selected_distributor.id, c_id)

        initial_transaction.timestamp.append(datetime.datetime.now().timestamp())

        initial_transaction.prod_id = product_id

        transaction_list.append(initial_transaction)

        time.sleep(1)
        
        print('\nProduct dispatched to Distributer %2d for Client %2d under the product ID %2d.' % (selected_distributor.id,c_id, product_id))

        time.sleep(1)

    elif choice == 3:
        
        distributer_id = int(input("\nEnter the Distributer ID : "))
        prod_idd = int(input("\nEnter the ID of the product to be recieved : "))

        tempdis = 0
        for temp_tran in transaction_list:
            if temp_tran.prod_id != prod_idd:
                tempdis += 1

        if tempdis == len(transaction_list):
            print("\nProduct ID not found.")
            continue


        dis_count = 0

        for dis3 in distributer_list:
            if dis3.id == distributer_id:

                dis_key2 = int(input("\nEnter the product key for the distribution : "))
                
                if dis_key2 == dis3.key:
                    time.sleep(1)

                    print("\nDispatching the product...")

                    for tran in transaction_list:
                        if tran.d_id == dis3.id and tran.prod_id == prod_idd:
                            tran.timestamp.append(datetime.datetime.now().timestamp())
                            tran.dis_dispatched = True
                            break

                    dis3.key = 0
                    dis3.busy = False    

                    time.sleep(1)

                    print("\nProduct dispatched successfully.")
                    time.sleep(1)
                    break
                
                else:
                    print("\nWrong product key!")

            dis_count += 1

        if dis_count == len(distributer_list):
            print("\nInvalid Distributor ID.")

    elif choice == 4:
        
        client_id = int(input("\nEnter the client ID : "))
        prod_id = int(input("\nEnter the ID of the product to be recieved : "))

        time.sleep(1)

        tempcl = 0
        for temp_tran1 in transaction_list:
            if temp_tran1.prod_id != prod_id:
                tempcl += 1

        if tempcl == len(transaction_list):
            print("\nProduct ID not found.")
            continue

        client_count = 0

        for client3 in client_list:
            if client_id == client3.id:

                if client3.recieved == prod_id:
                    print("\nProduct already recieved.")
                    break

                client_key2 = int(input("\nEnter the product key to recieve the product : "))

                if client_key2 == client3.key:
                
                    for tran in transaction_list:
                        if tran.c_id == client_id and tran.prod_id == prod_id:
                            if tran.dis_dispatched == False:
                                print("\nProduct not dispatched by the distributer.")
                                break

                            else:
                                tran.timestamp.append(datetime.datetime.now().timestamp())
                                tran.client_recieved = True
                                tran.complete = True
                                client3.recieved = prod_id
                                break
                    
                        

                    client3.key = 0

                    time.sleep(1)

                    print("\nProduct successfully recieved by the client.")
                    time.sleep(1)
                    break

                else:
                    print("\nWrong product key!")
        
            client_count += 1

        if client_count == len(client_list):
            print("\nInvalid Client ID.")

    elif choice == 5:
        client_id_qr = int(input("\nEnter the client ID : "))
        prod_id2_qr = int(input("\nEnter the ID of the product to be tracked : "))

        time.sleep(1)

        client_count2 = 0

        for client4 in client_list:
            if client_id_qr == client4.id:
                for tran_qr in transaction_list:
                    if tran_qr.c_id == client_id_qr and prod_id2_qr == tran_qr.prod_id:
                        
                        time_dis = "N.A" if tran_qr.dis_dispatched == False else datetime.datetime.fromtimestamp(tran_qr.timestamp[1])
                        time_rec = "N.A" if tran_qr.client_recieved == False else datetime.datetime.fromtimestamp(tran_qr.timestamp[2])

                        if(tran_qr.dis_dispatched == True):
                            disstatus = 'Dispatched by the distributer'
                        else:
                            disstatus = 'Not dispatched by the distributer'
                        
                        if(tran_qr.client_recieved == True):
                            clstatus = 'Received by the client'
                        else:
                            clstatus = 'Not received by the client'
                        
                        
                        string = "\nProduct status : " + disstatus + "/" + clstatus + "\nProduct dispatched by distributer:"+str(time_dis)+"\nProduct received by Client:"+str(time_rec)

                        time.sleep(1)
                        print("\nGenerating QR Code.")

                        img = qrcode.make(string)
                        img.save("qrCode.png")
                        break
            
            else:
                client_count2 += 1

        if client_count2 == len(client_list):
            print("\nInvalid Client ID.")

    elif choice == 6:
        # We have been assigned PoET as our consensus algorithm, we implement it using the random library. 
        
        # We log 2 completed transactions per block, so mining function would only working if no of completed transactions in the list is greater than 2.
        
        completed_transactions = []

        time.sleep(1)

        for tran_tran in transaction_list:
            if tran_tran.complete == True and tran_tran.mined == False:
                completed_transactions.append(tran_tran)

        if len(completed_transactions) < 2:
            print("\nNot enough transactions to mine a block.")
            continue

        
        
        # Now we assign waiting time(in seconds) to all the nodes i.e completed transactions.

        for tran_tran2 in completed_transactions:
            tran_tran2.elasped_time = random.randint(5,3600)

        
        for tran_tran3 in completed_transactions:
            print("\nTransaction product ID : %2d\nWait time : %2d sec" % (tran_tran3.prod_id, tran_tran3.elasped_time))
            time.sleep(1)


        # Now select the 2 nodes with the least wait time

        min_time1 = completed_transactions[0].elasped_time
        transaction1 = completed_transactions[0]
        
        for k in completed_transactions:
            if min_time1 > k.elapsed_time:
                min_time1 = k.elapsed_time
                transaction1 = k

        # so we get the transaction with the least wait time.


        # now we do the same to get the second transaction

        min_time2 = completed_transactions[0].elasped_time
        transaction2= completed_transactions[0]

        for l in completed_transactions:
            if l.elapsed_time == min_time1:
                continue
            if min_time2 < l.elapsed_time:
                min_time2 = l.elapsed_time
                transaction_list = l

        mine_tran = [transaction1, transaction2]

        print("\nMining the block...")

        if blockchain == []:
            blockg = block('0', mine_tran)
            blockg.timestamp = datetime.datetime.now().timestamp()
            blockchain.append(blockg)

        else:
            len_bc = len(blockchain)

            block1 = block(blockchain[len_bc-1].block_hash, mine_tran)
            block1.timestamp = datetime.datetime.now().timestamp()
            blockchain.append(block1)


        # printing the blockchain

        for block_ in blockchain:
            time.sleep(1)

            print(Fore.GREEN + "\nCurrent block hash : " + block_.block_hash + "\nMerkle Root : " + block_.merkle_root + "\nTimestamp : " + str(block_.timestamp) +"\nPrevious block hash : " + block_.previous_block_hash)
        

        # Marking mined transactions as mined

        for tran_tran4 in transaction_list:
            if tran_tran4.prod_id == transaction1.prod_id or tran_tran2.prod_id == transaction2.prod_id:
                tran_tran4.mined = True
 
    elif choice == 7:

        dis_prob= int(input("\nEnter the Distributer ID : "))
        cl_prob = int(input("\nEnter the accused client ID : "))
        prod_prob = int(input("\nEnter the ID of the product in the talks : "))

        time.sleep(1)

        for tran_prob in transaction_list:
            if tran_prob.c_id == cl_prob and tran_prob.prod_id == prod_prob and tran_prob.d_id == dis_prob:
                if tran_prob.client_recived == True:
                    print("\nProduct was successfully recieved by the client, a deduction of RS 100 will be made for misconduct of the policy.")

                    for client_prob in client_list:
                        if client_prob.id == cl_prob:
                            client_prob.deposit -= 100
                        
                else:
                    print("\nProduct was never received by the client.")

                    time.sleep(1)

                    if tran_prob.dis_dipatched == False:
                        print("\nProduct was never dispatched from the distributer side, a deduction of RS 100 will be made for misconduct of the policy.")
                        for dist_prob in distributer_list:
                            if dist_prob.id == dis_prob:
                                dist_prob.deposit -= 100
            
            else:
                print("\nOne of the entered field is wrong, Try again.")
     
    elif choice == 8:

        cl_prob2 = int(input("\nEnter the Client ID : "))
        dis_prob2= int(input("\nEnter the accused distributer ID : "))
        prod_prob2 = int(input("\nEnter the ID of the product in the talks : "))

        time.sleep(1)

        for tran_prob2 in transaction_list:
            if tran_prob2.c_id == cl_prob2 and tran_prob2.prod_id == prod_prob2 and tran_prob2.d_id == dis_prob2:
                if tran_prob2.dis_dispatched == False:
                    print("\nProduct was never dispatched from the distributer side, a deduction of RS 100 will be made for misconduct of the policy.")

                    for dist_prob2 in distributer_list:
                        if dist_prob2.id == dis_prob2:
                            dist_prob2.deposit -= 100
                        
                else:
                    print("\nProduct was dispatched by the client.")

                    time.sleep(1)

                    if tran_prob2.client == True:
                        print("\nProduct was successfully recieved by the client, a deduction of RS 100 will be made for misconduct of the policy.")
                        for client_prob2 in client_list:
                            if client_prob2.id == cl_prob2:
                                client_prob2.deposit -= 100
            
            else:
                print("\nOne of the entered field is wrong, Try again.")

                

