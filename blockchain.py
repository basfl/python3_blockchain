blockchain = []


def get_last_blockchain_value():
    """ return the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=[1]):
    """
    Append current value as well as last value to blockchain.

    arguments:
        :transction_amout: the amount that shoud be added
        :last_transaction: the last blockchain transaction
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    return float(input('your transaction amount please :'))


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
   # block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        print("block_index is {}".format(block_index))
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            print("blockchain[block_index][0] is {}".format(
                blockchain[block_index][0]))
            print(
                "blockchain[block_index - 1] is {}".format(blockchain[block_index - 1]))
            is_valid = True
        else:
            is_valid = False
            break
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1
    return is_valid


waite_for_input = True
while waite_for_input:
    print("please choose!")
    print("1: Add a new transaction value")
    print("2: Output the blockchain value")
    print("h:Manuplate the chain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "q":
        waite_for_input = False
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    else:
        print("Input was invalid , please choose from the list!")
    print("choice registerd! ")
    if not verify_chain():
        print_blockchain_elements()
        print("invalid blockchain")
        break
else:
    print("User left")


print("Done!")
