FROM python:3.9
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD ./Data ./Data
COPY ./app.py ./
COPY ./dataloader.py ./
COPY ./func.py ./
COPY ./bash.sh ./
EXPOSE 5000
CMD ["python","app.py"]