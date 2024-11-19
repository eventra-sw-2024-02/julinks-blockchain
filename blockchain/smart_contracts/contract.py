# blockchain/smart_contracts/contract.py

class Contract:
    def __init__(self, bytecode: str, owner: str, name: str):
        self.bytecode = bytecode
        self.owner = owner
        self.name = name
        self.state = {}

    def set_state(self, key, value):
        self.state[key] = value

    def get_state(self, key):
        return self.state.get(key, None)

    def __repr__(self):
        return f"Contract({self.name}, Owner: {self.owner})"