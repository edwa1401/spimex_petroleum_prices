FROM python:3.10-alpine

WORKDIR /spimex_petroleum_prices

RUN apk update && apk add --no-cash --virtual bash git gcc g++

RUN python -m pip install --upgrade pip

COPY requirements.txt /spimex_petroleum_prices/

RUN python -m pip install -r requirements.txt

COPY . /spimex_petroleum_prices

CMD ["uvicorn", "webapp.__main__:app", "--host", "0.0.0.0", "--port", "80"]