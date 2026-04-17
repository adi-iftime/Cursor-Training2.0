from fastapi import FastAPI

app = FastAPI()

USERS = [
    {"id": 1, "name": "Alice Example", "email": "alice@example.com"},
    {"id": 2, "name": "Bob Example", "email": "bob@example.com"},
]


@app.get("/users")
def list_users():
    return USERS


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
