FROM python:3.5-alpine
WORKDIR /maki
COPY ["requirements.txt", "*.py", "./"]
RUN pip install -r requirements.txt
CMD ["python", "./bot.py"]
