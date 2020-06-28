FROM python:3.6.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5500
ENTRYPOINT ["python"]
CMD [ "main_board.py"]