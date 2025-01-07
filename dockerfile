FROM python:3.12-slim
WORKDIR /currencyback
COPY . /currencyback
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["fastapi", "main:app","0.0.0.0","--port","8000"]
