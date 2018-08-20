import functools
import hashlib
import json
MINING_REWARD = 10
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transaction': []
}
blockchain = [genesis_block]
open_transaction = []
owner = 'babak'
participants = {'babak'}  # this is a set


def hashed_block(block):
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()
    # return '-'.join([str(block[key]) for key in block])


# def get_balance(participant):
#     tx_sender = [[tx['amount'] for tx in block['transaction']
#                   if tx['sender'] == participant] for block in blockchain]  # this is nested list comperhension
#     open_tx_sender = [tx['amount']
#                       for tx in open_transaction if tx['sender'] == participant]

#     tx_sender.append(open_tx_sender)
#     amount_send = functools.reduce(
#         lambda tx_sum, tx_amount: tx_sum+sum(tx_amount) if len(tx_amount) > 0 else tx_sum+0, tx_sender, 0)
#     tx_recipient = [[tx['amount'] for tx in block['transaction']
#                      if tx['recipient'] == participant] for block in blockchain]  # this is nested list comperhension
#     amount_recieved = functools.reduce(
#         lambda tx_sum, tx_amount: tx_sum+(tx_amount) if len(tx_amount) > 0 else tx_sum+0, tx_recipient, 0)
#     return amount_recieved - amount_send
def get_balance(participant):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx['amount'] for tx in block['transaction']
                  if tx['sender'] == participant] for block in blockchain]
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx['amount']
                      for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx['amount'] for tx in block['transaction']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(
        tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # Return the total balance
    return amount_received - amount_sent


def get_last_blockchain_value():
    """ return the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """
    Append current value as well as last value to blockchain.

    arguments:
        :sender: the sender of coin
        :recipient: the recipient of the coin
        :amount: the amount of coins send with transaction
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    if verify_transaction(transaction):
        open_transaction.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed = hashed_block(last_block)
    print("hashed_block is {}".format(hashed))
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transaction[:]
    copied_transactions.append(reward_transaction)
    open_transaction.append(reward_transaction)
    block = {
        'previous_hash': hashed,
        'index': len(blockchain),
        'transaction': copied_transactions
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input("enter the recipient of transaction : ")
    tx_amount = float(input('your transaction amount please : '))
    return tx_recipient, tx_amount  # this is tuple


def get_user_choice():
    user_input = input("your choice! ")
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print("Outputing the block")
        print(block)
    else:
        print("-"*20)


def verify_chain():
    """ verify the blockchain return True if it is valid , otherwise return False """
    for(index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous_hash"] != hashed_block(blockchain[index-1]):
            return False
    return True


def verify_transactions():
    # is_valid = True
    # for tx in open_transaction:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid
    all([verify_transaction(tx) for tx in open_transaction])


waite_for_input = True
while waite_for_input:
    print("please choose!")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain value")
    print("4: Output participents")
    print("5: check transaction validity")
    print("h:Manuplate the chain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print("Added transaction")
        else:
            print('Transaction failed')
        print(open_transaction)
    elif user_choice == "2":
        if mine_block():
            open_transaction = []
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transaction are  valid")
        else:
            print("There are invakid transactions")
    elif user_choice == "q":
        waite_for_input = False
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transaction': [{'sender': 'babak', 'recipient': 'amir', 'amount': 100.0}]
            }
    else:
        print("Input was invalid , please choose from the list!")
    print("choice registerd! ")
    if not verify_chain():
        print_blockchain_elements()
        print("invalid blockchain")
        break
    print('balance of {} : {:6.2f}'.format('babak', get_balance('babak')))
else:
    print("User left")


print("Done!")
