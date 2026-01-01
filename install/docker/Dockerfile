FROM fedora:40

RUN dnf -y update && \
    dnf -y install python3 python3-pip grpcurl && \
    dnf -y clean all

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN if [ -f /app/requirements.txt ]; then \
      pip3 install --no-cache-dir -r /app/requirements.txt; \
    else \
      pip3 install --no-cache-dir fastapi uvicorn aiosqlite asyncpg jinja2 pydantic-settings; \
    fi

COPY . /app

EXPOSE 9090

CMD ["python3", "main.py"]