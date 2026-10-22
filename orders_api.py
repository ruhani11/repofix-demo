"""A small order-submission API."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI(title="Order Service", version="0.1.0")


class OrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: str = Field(min_length=1, max_length=80)
    quantity: int = Field(strict=True)


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderRequest) -> dict[str, str | int]:
    if order.quantity <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be a positive integer.",
        )

    return {
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "accepted",
    }
