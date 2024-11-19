# blockchain/smart_contracts/executor.py
from blockchain.smart_contracts.compiler import Compiler
from blockchain.smart_contracts.vm import VirtualMachine

class Executor:
    def __init__(self, compiler: Compiler, vm: VirtualMachine):
        self.compiler = compiler
        self.vm = vm

    def deploy_contract(self, code: str, owner: str, name: str):
        """
        Deploys the smart contract.
        """
        bytecode = self.compiler.compile(code)  # Compile the contract code
        contract = {"name": name, "bytecode": bytecode, "owner": owner}
        return contract

    def run_contract(self, contract):
        """
        Executes the smart contract using the virtual machine.
        """
        self.vm.execute(contract["bytecode"])
