FROM python:3.14-bookworm

WORKDIR /libguard

RUN pip install --upgrade pip && pip install uv --no-cache-dir

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]