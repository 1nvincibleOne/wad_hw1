import asyncio
import random
import time
import uuid

from cachetools import TTLCache
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()

TTL = 3 * 60 * 60  # keep data for 3 hours
orders = TTLCache(maxsize=1_000_000, ttl=TTL)   # orderId -> {"cargoId", "price"}
cargos = TTLCache(maxsize=1_000_000, ttl=TTL)   # cargoId -> {"orderId", "step"}
STATUSES = ["NEW", "In Process", "In Process", "Delivered", "Done"]


@app.middleware("http")
async def fixed_response_time(request: Request, call_next):
    """Pad every response so it takes exactly 500 ms."""
    start = time.perf_counter()
    response = await call_next(request)
    await asyncio.sleep(max(0, 0.5 - (time.perf_counter() - start)))
    return response


@app.get("/api/orderId/{order_id}")
async def get_order(order_id: str):
    if order_id not in orders:
        cargo_id = str(uuid.uuid4())
        orders[order_id] = {"cargoId": cargo_id, "price": random.randint(100, 999)}
        cargos[cargo_id] = {"orderId": order_id, "step": 0}
    return {"orderId": order_id, **orders[order_id]}


@app.get("/api/cargo/{cargo_id}")
async def get_cargo(cargo_id: str):
    cargo = cargos.get(cargo_id)
    if cargo is None:
        raise HTTPException(404, "not found")
    status = STATUSES[cargo["step"] % len(STATUSES)]
    cargo["step"] += 1
    return {"cargoId": cargo_id, "orderId": cargo["orderId"], "status": status}


class Price(BaseModel):
    price: int


@app.put("/api/price/{order_id}")
async def set_price(order_id: str, body: Price):
    if order_id not in orders:
        raise HTTPException(404, "not found")
    orders[order_id]["price"] = body.price
    return {"orderId": order_id, "price": body.price}
