import hashlib

def proof_of_work(block, difficulty: int) -> (str, int):
    """
    Implementa un algoritmo básico de Proof of Work.
    El reto consiste en encontrar un hash que comience con un número de ceros especificado por 'difficulty'.
    """
    nonce = 0
    target = '0' * difficulty  # Definimos el número de ceros que debe tener el hash.

    while True:
        block.nonce = nonce
        block_hash = block.calculate_hash()

        if block_hash.startswith(target):
            print(f"PoW resuelto con nonce: {nonce}")
            return block_hash, nonce  # Retornamos el hash y el nonce que cumple con la dificultad
        nonce += 1
        # Para no quedar en un bucle infinito innecesario en la simulación
        if nonce > 1000000:
            break
    return None, None