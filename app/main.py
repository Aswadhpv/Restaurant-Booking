from fastapi import FastAPI
from app.routers import table_router, reservation_router

app = FastAPI(title="Restaurant Table Booking API")

# Include the routers directly.
app.include_router(table_router)
app.include_router(reservation_router)
