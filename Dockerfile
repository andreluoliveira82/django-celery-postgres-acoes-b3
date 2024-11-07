FROM python:3.12

WORKDIR /app

# Copie os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock /app/

# Instale o pip, pipx e Poetry, e adicione o diretório do pipx ao PATH
RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx install poetry

# Adicione o diretório do Poetry ao PATH globalmente
ENV PATH="/root/.local/bin:$PATH"

# Exporte as dependências para um arquivo requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Instale as dependências do projeto diretamente
RUN pip install -r requirements.txt

# Instale o Google Chrome em um único comando e limpe o cache
RUN apt-get update && \
    apt-get install -y wget && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm -f google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Crie um novo usuário e ajuste permissões
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app

# Mude para o novo usuário
USER appuser

# Copie o resto dos arquivos do projeto
COPY . /app

# Comando padrão para iniciar o contêiner (se necessário)
CMD ["bash"]
