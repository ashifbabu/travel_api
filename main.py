from fastapi import FastAPI

from services.bus_service.bus_service import router as bus_router
from services.car_service.car_service import router as car_router
from services.event_service.event_service import router as event_router
from services.flight_service.api.routes import router as flight_router
from services.holiday_service.holiday_service import router as holiday_router
# from services.flight_service.flight_service import router as flight_router
from services.hotel_service.hotel_service import router as hotel_router
from services.insurance_service.insurance_service import \
    router as insurance_router
from services.train_service.train_service import router as train_router

app = FastAPI()

app.include_router(flight_router, prefix="/api/v1/flights")
app.include_router(hotel_router, prefix="/api/v1/hotels")
app.include_router(holiday_router, prefix="/api/v1/holidays")
app.include_router(car_router, prefix="/api/v1/cars")
app.include_router(bus_router, prefix="/api/v1/buses")
app.include_router(train_router, prefix="/api/v1/trains")
app.include_router(event_router, prefix="/api/v1/events")
app.include_router(insurance_router, prefix="/api/v1/insurance")


@app.get("/")
async def root():
    return {"message": "Welcome to the Travel API"}
