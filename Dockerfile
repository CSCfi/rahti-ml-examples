FROM tensorflow/tensorflow:2.7.0-gpu

ENV HOME=/app
WORKDIR $HOME
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN chgrp -R 0 $HOME && \
    chmod -R g=u $HOME

EXPOSE 8080
CMD [ "uvicorn", "asgi:app", "--port=8080", "--host=0.0.0.0"]