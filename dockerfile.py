FROM python:3.8-slim

# Instalar dependências
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copiar os arquivos do código
COPY . /app/

# Expor a porta que o Flask vai rodar
EXPOSE 5000

# Rodar o aplicativo
CMD [""python"", ""app.py""]
