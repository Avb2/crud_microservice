FROM python:3.12

WORKDIR /usr/local/auth

COPY auth/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY keys/ticket-priv-key.pem /app/keys/ticket-priv-key.pem
COPY keys/public.pem /app/keys/public.pem


RUN chmod 644 /app/keys/ticket-priv-key.pem
RUN chmod 644 /app/keys/public.pem

COPY auth/src ./src
EXPOSE 5000

RUN useradd app
USER app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]