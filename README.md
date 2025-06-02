# API TaskFlow

## Configurações do Projeto

Instale o Python 3.12 (https://www.python.org/downloads/release/python-3120/)

Configure seu ambiente de desenvolvimento:

- **Linux / MAC**:

```plaintext
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

- **Windows**:

```plaintext
python -m venv venv && venv\Scripts\activate.bat && pip install -r requirements.txt
```

Na raiz do projeto, crie o arquivo .env contendo as variáveis listadas no arquivo .env.example.

Para inicializar o projeto, dentro de seu ambiente virtual, utilize o comando:

```plaintext
python main.py
```

Após a inicialização, a API ficará exposta no endereço localhost:8000.

Em localhost:8000/docs você terá acesso à documentação dos endpoints da API via Swagger.
