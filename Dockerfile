FROM tensorflow/tensorflow:2.3.0-gpu

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 8080
CMD [ "python3", "-m" , "flask", "run", "--port=8080", "--host=0.0.0.0"]
