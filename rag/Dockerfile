FROM python:3.11

WORKDIR /app

COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

EXPOSE 8888

#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
CMD ["uvicorn", "src.models_deployment:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
