FROM python:3
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
CMD ["pytest"]