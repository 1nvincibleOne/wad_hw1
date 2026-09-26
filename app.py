import asyncio
import os
import random
import time
import uuid

from cachetools import TTLCache
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

APP_NAME = os.getenv("APP_NAME", "Order / Cargo stub")
TTL = int(os.getenv("CACHE_TTL_SECONDS", str(3 * 60 * 60)))
RESPONSE_DELAY = int(os.getenv("RESPONSE_DELAY_MS", "500")) / 1000

app = FastAPI(title=APP_NAME)

orders = TTLCache(maxsize=1_000_000, ttl=TTL)   # orderId -> {"cargoId", "price"}
cargos = TTLCache(maxsize=1_000_000, ttl=TTL)   # cargoId -> {"orderId", "step"}
STATUSES = ["NEW", "In Process", "In Process", "Delivered", "Done"]


@app.middleware("http")
async def fixed_response_time(request: Request, call_next):
    """Pad every response so it takes at least RESPONSE_DELAY_MS."""
    start = time.perf_counter()
    response = await call_next(request)
    await asyncio.sleep(max(0, RESPONSE_DELAY - (time.perf_counter() - start)))
    return response


@app.get("/")
async def root():
    return {
        "app": APP_NAME,
        "cacheTtlSeconds": TTL,
        "responseDelayMs": int(RESPONSE_DELAY * 1000),
        "docs": "/docs",
    }


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
