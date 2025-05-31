
# Projeto de Geração de Texto com GPT-2

## Descrição

Este projeto implementa um serviço de geração de texto utilizando o modelo pré-treinado GPT-2 da biblioteca Hugging Face Transformers. Ele oferece duas formas principais de implantação: uma API web construída com Flask e containerizada com Docker, e uma função serverless para AWS Lambda. O objetivo é fornecer uma interface acessível para interagir com o modelo GPT-2, enviando um *prompt* (texto inicial) e recebendo uma continuação gerada pelo modelo.

O "código importado" central neste projeto é o modelo `GPT2LMHeadModel` e seu respectivo `GPT2Tokenizer`, que são utilizados para realizar a tarefa de modelagem de linguagem e geração de texto. Este projeto contextualiza o uso desses componentes, envolvendo-os em serviços práticos e implantáveis.

## Funcionalidades Principais

* **Geração de Texto:** Utiliza o modelo GPT-2 para gerar texto com base em um *prompt* fornecido pelo usuário.
* **API Web com Flask:** Oferece um endpoint `/generate` (via POST) para interação com o modelo através de requisições HTTP.
* **Containerização com Docker:** Permite fácil empacotamento e implantação da API Flask em ambientes que suportam Docker.
* **Implantação Serverless com AWS Lambda:** Fornece um handler para implantar a funcionalidade de geração de texto como uma função AWS Lambda.

## Tecnologias Utilizadas

* Python 3.8+
* Flask (para a API web)
* Hugging Face Transformers (para o modelo GPT-2)
* Docker (para containerização)
* AWS Lambda e Boto3 (para a implantação serverless)
* JSON (para comunicação de dados)

## Estrutura do Projeto

* `python-trained-model.py`: Contém a aplicação Flask que serve o modelo GPT-2 através de uma API. Este arquivo é referenciado como `app.py` no Dockerfile.
* `dockerfile` (ou `Dockerfile`): Arquivo de definição para construir a imagem Docker da aplicação Flask. (Observação: o arquivo fornecido chama-se `dockerfile.py`, mas seu conteúdo é de um Dockerfile padrão).
* `aws-deployment.py`: Contém o código do handler para a função AWS Lambda, permitindo a geração de texto em um ambiente serverless.
* `requirements.txt`: Deve listar as dependências Python do projeto.

## Pré-requisitos

* Python 3.8 ou superior
* Docker instalado (para a opção de implantação com Docker)
* Conta AWS e AWS CLI configurados (para a opção de implantação com AWS Lambda)
* Um arquivo `requirements.txt` com as dependências (veja seção abaixo).

## `requirements.txt`

Crie um arquivo `requirements.txt` na raiz do projeto com o seguinte conteúdo (as versões podem precisar de ajuste):

```txt
flask
transformers
torch
boto3
```

## Instalação e Uso

Existem duas formas principais de executar este projeto:

### Opção 1: Usando Docker (API Flask)

1.  **Certifique-se de que o arquivo `python-trained-model.py` seja nomeado como `app.py` na raiz do projeto, ou ajuste o `CMD` no `Dockerfile` para `CMD ["python", "python-trained-model.py"]`.**
2.  **Construa a imagem Docker:**
    Navegue até o diretório raiz do projeto (onde o `Dockerfile` e `requirements.txt` estão localizados) e execute:
    ```bash
    docker build -t gpt2-text-generator .
    ```
3.  **Execute o container Docker:**
    ```bash
    docker run -p 5000:5000 gpt2-text-generator
    ```
    A API estará acessível em `http://localhost:5000`.

4.  **Use a API:**
    Envie uma requisição POST para `http://localhost:5000/generate` com um corpo JSON contendo o *prompt*.
    Exemplo usando `curl`:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"prompt": "Olá, mundo! Como você está hoje?"}' \
         http://localhost:5000/generate
    ```
    A resposta será um JSON com o texto gerado:
    ```json
    {
      "response": "Olá, mundo! Como você está hoje? Eu estou bem, obrigado por perguntar."
    }
    ```

### Opção 2: Implantação com AWS Lambda

1.  **Preparação do Pacote de Implantação:**
    * O script `aws-deployment.py` contém o `lambda_handler`.
    * Você precisará empacotar este script junto com suas dependências (listadas no `requirements.txt`) e o modelo GPT-2.
    * **Atenção:** Modelos como o GPT-2 podem ser grandes. Para o AWS Lambda, pode ser necessário:
        * Usar camadas Lambda para as dependências.
        * Carregar o modelo de um bucket S3 dentro da função Lambda ou usar o Amazon EFS para Lambda se o tamanho do pacote de implantação exceder os limites.

2.  **Criação da Função Lambda:**
    * Acesse o console da AWS ou use a AWS CLI/SAM/CloudFormation para criar uma nova função Lambda.
    * Configure o runtime para Python (ex: Python 3.8).
    * Faça o upload do pacote de implantação.
    * Defina o handler como `aws-deployment.lambda_handler` (assumindo que o arquivo se chama `aws-deployment.py`).
    * Ajuste as configurações de memória e tempo limite conforme necessário (a inferência de modelos de linguagem pode ser intensiva).

3.  **Teste a Função Lambda:**
    Configure um evento de teste no console Lambda com o seguinte formato JSON:
    ```json
    {
      "prompt": "Era uma vez, em uma terra distante"
    }
    ```
    A resposta da Lambda incluirá o texto gerado.

## Contexto da Importação e Adaptação

* **Origem do Código Principal (Modelo):** O modelo de linguagem `GPT2LMHeadModel` e o `GPT2Tokenizer` são componentes da biblioteca `transformers` da Hugging Face.
* **Adaptações Realizadas:**
    * O modelo GPT-2 pré-treinado é carregado e utilizado para gerar texto.
    * Uma API Flask foi desenvolvida (`python-trained-model.py`) para expor a funcionalidade de geração de texto através de um endpoint HTTP.
    * Um `Dockerfile` foi criado para facilitar a containerização e implantação da API Flask.
    * Um handler para AWS Lambda (`aws-deployment.py`) foi implementado para permitir a implantação serverless da funcionalidade.

## Licença

Este projeto utiliza componentes de terceiros:

* **Hugging Face Transformers:** Licenciado sob Apache License 2.0. É importante estar ciente dos termos de uso do modelo GPT-2 e da biblioteca.

O código específico deste projeto (wrappers Flask, Dockerfile, handler Lambda) pode ser licenciado conforme sua necessidade (ex: MIT, Apache 2.0, ou mantido como proprietário). Adicione sua declaração de licença aqui.

Exemplo:
```
## Licença do Projeto Atual
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
```

## Como Contribuir

Se este é um projeto pessoal, esta seção pode não ser necessária. Caso contrário:

1.  Faça um Fork do projeto.
2.  Crie uma Branch para sua Feature (`git checkout -b feature/NovaFuncionalidade`).
3.  Faça o Commit de suas mudanças (`git commit -m 'Adiciona NovaFuncionalidade'`).
4.  Faça o Push para a Branch (`git push origin feature/NovaFuncionalidade`).
5.  Abra um Pull Request.

## Autores e Agradecimentos

* **Autor do Projeto:** Jefferson Firmino Mendes/ On My Own
* **Agradecimentos:** À equipe da Hugging Face pelo desenvolvimento da biblioteca `transformers` e disponibilização do modelo GPT-2.

