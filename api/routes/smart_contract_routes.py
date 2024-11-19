from flask import Blueprint, request, jsonify
from blockchain.smart_contracts.executor import Executor
from blockchain.smart_contracts.compiler import Compiler
from blockchain.smart_contracts.vm import VirtualMachine

smart_contract_routes = Blueprint('smart_contract_routes', __name__)

# Initialize the Compiler and VirtualMachine
compiler = Compiler()
vm = VirtualMachine(variables={})

# Initialize the Executor with the Compiler and VirtualMachine
executor = Executor(compiler, vm)

@smart_contract_routes.route('/deploy', methods=['POST'])
def deploy_contract():
    data = request.json
    try:
        contract_id = executor.deploy_contract(data['code'], data['owner'], data['name'])
        return jsonify({"message": "Contrato desplegado", "contract_id": contract_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@smart_contract_routes.route('/call/<contract_id>', methods=['POST'])
def call_contract(contract_id):
    data = request.json
    try:
        result = executor.run_contract(contract_id, data['function'], data['params'])
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400