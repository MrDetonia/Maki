FROM python:3.5-alpine

# copy files
WORKDIR /maki
COPY ["requirements.txt", "*.py", "./"]

# install dependencies
RUN pip install -r requirements.txt

# start bot
CMD ["python", "./bot.py"]
