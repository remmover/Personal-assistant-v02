
FROM python:3.11.3

WORKDIR .

COPY . .
# Встановимо залежності всередині контейнера
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main



# Запустимо наш застосунок всередині контейнера
CMD ["python", "./personal_assistant/main.py"]