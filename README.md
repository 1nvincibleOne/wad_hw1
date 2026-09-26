# Order / Cargo stub

## Run

    pip install -r requirements.txt
    uvicorn app:app --host 0.0.0.0 --port 8000

or with Docker:

    docker build -t stub . && docker run -p 8000:8000 stub

## Endpoints

| Method | Path                     | Body              | Response                                  |
|--------|--------------------------|-------------------|-------------------------------------------|
| GET    | /api/orderId/<orderId>   | –                 | {"orderId", "cargoId", "price"}           |
| GET    | /api/cargo/<cargoId>     | –                 | {"cargoId", "orderId", "status"}          |
| PUT    | /api/price/<orderId>     | {"price": 123}    | {"orderId", "price"}                      |


