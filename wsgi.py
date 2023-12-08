import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8082,
        reload=True,
        timeout_keep_alive=120,
    )