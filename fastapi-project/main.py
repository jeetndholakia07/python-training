from fastapi import FastAPI, Request, HTTPException
from routers.company_router import router as company_router
from routers.employee_router import router as employee_router
from routers.auth_router import router as auth_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.include_router(company_router, prefix="/v1")
app.include_router(employee_router, prefix="/v1")
app.include_router(auth_router, prefix="/v1")

# Validation Exception Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "detail": exc.errors(),
        },
    )

# HTTP Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )

# Global Base Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc),
        },
    )