import json
import pickle
import time

from flask import Flask

from .state import State

app = Flask(__name__)


@app.route("/")
def main():
    return "up", 200


@app.route("/api/status")
def get_status():
    try:
        state: State = pickle.load(open("state.pickle", "rb"))
    except:
        state = State()
    return {"doors": state.door_status, "last_updated": state.last_updated}


@app.route("/api/open/<int:door>")
def open_door(door: str):
    state: State = pickle.load(open("state.pickle", "rb"))
    if state.to_open is not None:
        return {"error": "Door already opening"}, 400
    try:
        state.to_open = int(door)
        pickle.dump(state, open("state.pickle", "wb"))
        return {"doorId": door}, 200
    except ValueError:
        return {"error": "Invalid door number"}, 400


@app.route("/post/<string:arr>")
def test_(arr: str):
    try:
        list_ = json.loads(arr)
    except:
        return {"error": "Invalid JSON"}, 400
    try:
        state = pickle.load(open("state.pickle", "rb"))
    except:
        state = State()
    state.door_status = list_
    door = state.to_open
    state.to_open = None
    state.last_updated = time.time() * 1000
    pickle.dump(state, open("state.pickle", "wb"))

    return str(door) if door is not None else "null", 200
