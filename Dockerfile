FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 13022
ENV PYTHONPATH="$PYTHONPATH:/app"
CMD python ./src/controller.py cloud