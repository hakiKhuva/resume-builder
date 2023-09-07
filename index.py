from app import create_app
import os

app = create_app({
    "SECRET_KEY": os.environ.get("SECRET_KEY", os.urandom(50))
})