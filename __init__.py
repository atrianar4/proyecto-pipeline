from flask import Flask

app = Flask(__name__)

from app import app
from app import database
from app import mcr_pipeline
from app import sm