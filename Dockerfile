FROM python:3.14-bookworm

WORKDIR /libguard

RUN apt-get update && apt-get install -y curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
    | sh -s -- -b /usr/local/bin
RUN pip install --upgrade pip && pip install uv --no-cache-dir

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]