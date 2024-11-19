# blockchain/smart_contracts/compiler.py
import re

class Compiler:
    def __init__(self):
        self.bytecode = []
        self.variables = {}

    def compile(self, code: str):
        self.bytecode = []
        self.variables = {}
        tokens = self.tokenize(code)
        self.parse(tokens)
        return self.bytecode

    def tokenize(self, code: str):
        token_specification = [
            ('NUMBER', r'\d+'),  # Integer
            ('ID', r'[A-Za-z_]\w*'),  # Identifiers
            ('CONTRACT', r'contract'),  # Contract keyword
            ('FUNCTION', r'function'),  # Function keyword
            ('OP', r'[+\-*/=<>]'),  # Arithmetic and comparison operators
            ('STRING', r'"[^"]*"'),  # String literals
            ('BRACE', r'[{}]'),  # Braces
            ('PAREN', r'[()]'),  # Parentheses
            ('COLON', r':'),  # Colon
            ('SEMICOLON', r';'),  # Semicolon
            ('NEWLINE', r'\n'),  # Line endings
            ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
            ('MISMATCH', r'.'),  # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_num = 1
        line_start = 0
        tokens = []
        mo = get_token(code)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(f"Unexpected character {value!r} on line {line_num}")
            else:
                tokens.append((kind, value))
            mo = get_token(code, mo.end())
        return tokens

    def parse(self, tokens):
        iterator = iter(tokens)
        in_contract = False
        contract_name = None

        for kind, value in iterator:
            if kind == 'CONTRACT':  # Contract Declaration
                in_contract = True
                contract_name = next(iterator)[1]  # Get the contract name
                opening_brace = next(iterator)  # Expect '{'
                if opening_brace[1] != '{':
                    raise RuntimeError(f"Expected '{{' after contract {contract_name}")
                self.bytecode.append(f"DEFINE CONTRACT {contract_name}")

            elif in_contract and kind == 'FUNCTION':  # Inside Contract: Function Definition
                self.parse_function(iterator)

            elif in_contract and kind == 'BRACE' and value == '}':  # End of Contract
                in_contract = False
                self.bytecode.append(f"END CONTRACT {contract_name}")

            elif in_contract and kind == 'ID':  # Inside Contract: Variable or Action
                if value not in self.variables:
                    raise RuntimeError(f"Undefined variable in contract: {value}")
                self.bytecode.append(f"LOAD {value}")

            elif not in_contract:  # Outside a Contract Block
                raise RuntimeError("Code outside a contract block is not allowed.")

    def parse_function(self, iterator):
        function_name = next(iterator)[1]  # Function name
        opening_paren = next(iterator)  # Expect '('
        if opening_paren[1] != '(':
            raise RuntimeError(f"Expected '(' after function name {function_name}")

        # Parse parameters
        parameters = []
        while True:
            token = next(iterator)
            if token[1] == ')':  # End of parameters
                break
            if token[0] == 'ID':  # Parameter identifiers
                parameters.append(token[1])

        opening_brace = next(iterator)  # Expect '{'
        if opening_brace[1] != '{':
            raise RuntimeError(f"Expected '{{' to start function body for {function_name}")

        # Parse function body
        body = []
        while True:
            token = next(iterator)
            if token[1] == '}':  # End of function
                break
            body.append(token)

        self.bytecode.append(f"DEFINE FUNCTION {function_name} WITH {parameters}")
        self.bytecode.append(f"FUNCTION BODY {body}")

    def declare_variable(self, iterator):
        try:
            # Expect: let TYPE NAME = VALUE;
            type_token = next(iterator)  # TYPE (e.g., "int")
            name_token = next(iterator)  # NAME (e.g., "a")
            eq_token = next(iterator)  # Equals ('=')
            value_token = next(iterator)  # VALUE (e.g., "5")
            semi_token = next(iterator)  # Semicolon (';')

            if eq_token[1] != '=' or semi_token[1] != ';':
                raise RuntimeError(f"Syntax error near variable declaration")

            var_type = type_token[1]
            var_name = name_token[1]
            var_value = value_token[1]

            # Force typing check (for future Rust-style compatibility)
            if not isinstance(var_value, int):  # Example for int type
                raise RuntimeError(f"Type mismatch for variable {var_name}")

            # Store variable in memory
            self.variables[var_name] = var_value
            self.bytecode.append(f'DEFINE {var_name} {var_value} {var_type}')

        except StopIteration:
            raise RuntimeError("Incomplete variable declaration")

