<p align="center">
  <img src="https://user-images.githubusercontent.com/63754409/138783487-b3e1c4e1-629c-4a0f-80d9-a5a6ff689910.png" />
</p>

# Projeto adoCão

Documentação [FastAPI](https://fastapi.tiangolo.com/).

## Instalação

Clone este repositório

  ``` shell
  git clone https://github.com/Louissilver/adocao_python.git
  cd caminho/do/diretorio/adocao_python
  ```
Se você ainda não possui o virtual environment do Python, instale com o comando abaixo
  ``` shell
  pip install virtualenv
  ```

Crie um ambiente virtual no diretório

  ``` shell
  python -m venv './adocao_python/'
  ```

* Em _Linux_, _macOS_ e outros _UNIXes_, ative o virtual environment:

  ``` shell
  source .\venv\Scripts\activate
  ```

* Para computadores rodando _Windows_, ative o virtual environment:

  ``` shell
  .\venv\Scripts\activate
  ```

## Dependências
  
Utilize o `pip` para baixar as dependências do projeto:

``` shell
pip install -r requirements.txt
```

## Banco de dados

A aplicação utiliza **MongoDB** e criará automaticamente o banco de dados, mas
para isso é necessário já possuir o MongoDB instalado. 

Para instalar, basta seguir o tutorial de instalação:
```https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/```

## Execução

Para executar o servidor use:

``` shell
uvicorn index:app --reload  
```

O servidor estará sendo executado na porta 8000

Para consultar a documentação da API, acesse http://localhost:8000/docs#/  e para interomper a execução pressione «Ctrl»+«C».
