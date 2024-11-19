from datetime import datetime
from blockchain.consensus.proof_of_work import proof_of_work
from blockchain.core.block import Block
from blockchain.core.transaction import Transaction
from blockchain.smart_contracts.executor import Executor
from blockchain.smart_contracts.compiler import Compiler
from blockchain.smart_contracts.vm import VirtualMachine


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Define the difficulty of Proof of Work (4 zeros)
        self.pending_transactions = []
        self.mining_reward = 50
        compiler = Compiler()

        # Initialize the VirtualMachine with an empty 'variables' dictionary
        vm = VirtualMachine(variables={})

        self.executor = Executor(compiler, vm)
        self.contracts = {}

    def create_genesis_block(self) -> Block:
        """
        Creates the first block of the chain (genesis block).
        """
        return Block(0, str(datetime.now()), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        """
        Gets the latest block of the chain.
        """
        return self.chain[-1]

    def add_block(self, new_block: Block):
        """
        Adds a new block to the chain after validating with Proof of Work.
        """
        new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash
        new_block.hash, new_block.nonce = proof_of_work(new_block, self.difficulty)  # Perform PoW to validate the block
        self.chain.append(new_block)
        print("Block added:", new_block)

    def is_chain_valid(self) -> bool:
        """
        Verifies the validity of the chain (using block hashes).
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify the hash of the current block
            if current_block.hash != current_block.calculate_hash():
                print(f"Hash error in block {i}")
                return False

            # Verify the integrity of the link between blocks
            if current_block.previous_hash != previous_block.hash:
                print(f"Link error between blocks {i - 1} and {i}")
                return False

        return True

    def deploy_contract(self, code: str, owner: str, name: str):
        """
        Deploys a new smart contract.
        """
        contract = self.executor.deploy_contract(code, owner, name)
        self.contracts[name] = contract
        print(f"Contract {name} deployed by {owner}")

    def execute_contract(self, name: str):
        """
        Executes a deployed smart contract.
        """
        contract = self.contracts.get(name)
        if contract:
            self.executor.run_contract(contract)
        else:
            print(f"Contract {name} not found")

    def add_transaction(self, sender: str, recipient: str, amount: float):
        """
        Adds a new transaction to the list of pending transactions.
        """
        transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        """
        Mines all pending transactions and adds them to a new block.
        """
        if not self.pending_transactions:
            print("No transactions to mine")
            return

        new_block = Block(
            index=len(self.chain),
            timestamp=str(datetime.now()),
            data=[tx.to_dict() for tx in self.pending_transactions],
            previous_hash=self.get_latest_block().hash
        )
        self.add_block(new_block)
        self.pending_transactions = []
        print("All pending transactions have been mined")