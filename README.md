# Julinks Blockchain Project

Este proyecto implementa una blockchain con soporte para contratos inteligentes, NFTs y billeteras. Utiliza Flask y Flask-SocketIO para la API y la comunicación en tiempo real.

## Requisitos

- Python 3.12
- pip

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/julinks-blockchain.git
    cd julinks-blockchain
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Uso

1. Inicia el servidor:
    ```sh
    python main.py
    ```

2. Abre tu navegador y ve a `http://localhost:5000` para ver la interfaz de la blockchain.

## Endpoints de la API

### Crear una billetera

```sh
curl -X POST http://localhost:5000/api/wallet/create
```

### Obtener el balance de una billetera

```sh
curl -X GET http://localhost:5000/api/wallet/balance/<address>
```

### Crear un NFT

```sh
curl -X POST http://localhost:5000/api/nft/create -H "Content-Type: application/json" -d '{"name": "Mi NFT", "creator": "direccion_del_creador", "metadata": {"image": "enlace_a_la_imagen", "description": "descripcion_del_nft"}}'
```

### Listar un NFT para la venta

```sh
curl -X POST http://localhost:5000/api/nft/list -H "Content-Type: application/json" -d '{"nft_id": "id_del_nft", "price": 100}'
```

### Comprar un NFT

```sh
curl -X POST http://localhost:5000/api/nft/buy -H "Content-Type: application/json" -d '{"nft_id": "id_del_nft", "buyer": "direccion_del_comprador"}'
```

### Desplegar un contrato inteligente

```sh
curl -X POST http://localhost:5000/api/contract/deploy -H "Content-Type: application/json" -d '{"code": "codigo_del_contrato", "owner": "direccion_del_dueno", "name": "nombre_del_contrato"}'
```

### Llamar a un contrato inteligente

```sh
curl -X POST http://localhost:5000/api/contract/call/<contract_id> -H "Content-Type: application/json" -d '{"function": "nombre_de_la_funcion", "params": {"param1": "valor1"}}'
```

### Obtener los bloques de la blockchain

```sh
curl -X GET http://localhost:5000/api/blockchain/blocks
```

### Añadir una transacción

```sh
curl -X POST http://localhost:5000/api/blockchain/transaction -H "Content-Type: application/json" -d '{"sender": "direccion_del_remitente", "recipient": "direccion_del_destinatario", "amount": 10}'
```

### Minar un nuevo bloque

```sh
curl -X GET http://localhost:5000/api/blockchain/mine
```
