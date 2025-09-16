import time
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from src.model.Painted import Painted, CoordinatesOutOfRange, ColorsOutOfRange
from src.manager.Painteds import Painteds, YouDontHaveRights
from src.defined import SKETCH_RANGE

class App:
    _app = Flask(__name__)
    CORS(_app)
    @classmethod
    def run(cls, host:str="0.0.0.0", port:int=8080):
        cls._app.run(host, port)
    @_app.route("/paint", methods=["GET"])
    @staticmethod
    def _paint() -> Response:
        def gIFAS(a:str):
            return int(request.args.get(a))
        x, y, r, g, b = [gIFAS(a) for a in ["x", "y", "r", "g", "b"]]
        try:
            p = Painted(int(time.time()), x, y, r, g, b)
            Painteds.paint(request.remote_addr, p)
        except CoordinatesOutOfRange:
            return jsonify({"status": {"id":20, "description":"Coordinates are out of range."}}), 400
        except ColorsOutOfRange:
            return jsonify({"status": {"id":21, "description":"Colors are out of range."}}), 400
        except YouDontHaveRights:
            return jsonify({"status": {"id":21, "description":"You don't have rights."}}), 403
        return jsonify({"status": {"id":0, "description": "It's a success!"}})
    @_app.route("/getCompactSketch")
    @staticmethod
    def _getCompactSketch() -> Response:
        return jsonify({"status": {"id":0, "description": "It's a success!"}, "c":{f"{a[0]},{a[1]}":cs for a, cs in Painteds.getCompactSketch().items()}})
    @_app.route("/getRights")
    @staticmethod
    def _getRights() -> Response:
        return jsonify({"status": {"id":0, "description": "It's a success!"}, "c":Painteds.getRightCountByIp(request.remote_addr)})
    @_app.route("/getSketchRange")
    @staticmethod
    def _getSketchRange() -> Response:
        return jsonify({"status": {"id":0, "description": "It's a success!"}, "c":{"x":SKETCH_RANGE[0], "y":SKETCH_RANGE[1]}})