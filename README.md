# Order / Cargo stub

A small FastAPI app that simulates an order/cargo tracking API. Data lives in an
in-memory TTL cache (3 hours by default), and every response is padded to a
fixed latency (500 ms by default).

## Build and run with Docker

Build the image:

    docker build -t order-stub .

Run the container (maps host port 8000 to container port 8000):

    docker run -d --name order-stub -p 8000:8000 order-stub

Open http://localhost:8000 (app info) or http://localhost:8000/docs (Swagger UI).

## Environment variables

| Variable            | Default              | Description                            |
|---------------------|----------------------|----------------------------------------|
| `APP_NAME`          | `Order / Cargo stub` | Name shown on `/` and in `/docs`       |
| `CACHE_TTL_SECONDS` | `10800`              | How long orders/cargos are kept        |
| `RESPONSE_DELAY_MS` | `500`                | Minimum response time of every request |


## Run without Docker

    pip install -r requirements.txt
    uvicorn app:app --host 0.0.0.0 --port 8000

## Endpoints

| Method | Path                     | Body              | Response                                  |
|--------|--------------------------|-------------------|-------------------------------------------|
| GET    | /                        | –                 | app name and current config               |
| GET    | /api/orderId/<orderId>   | –                 | {"orderId", "cargoId", "price"}           |
| GET    | /api/cargo/<cargoId>     | –                 | {"cargoId", "orderId", "status"}          |
| PUT    | /api/price/<orderId>     | {"price": 123}    | {"orderId", "price"}                      |
