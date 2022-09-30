FROM ubuntu
RUN apt-get update -y
RUN apt install python3 -y
RUN apt install python3-pip -y
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD ./Data ./Data
COPY ./app.py ./
COPY ./dataloader.py ./
COPY ./func.py ./
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--reload"]