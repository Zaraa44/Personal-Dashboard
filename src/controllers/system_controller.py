import psutil
from flask import Blueprint, jsonify

system_bp = Blueprint("system", __name__)

@system_bp.route("/status")
def status():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return jsonify({
        "cpu": cpu,
        "memory": {
            "used": round(memory.used / (1024**3), 2),
            "total": round(memory.total / (1024**3), 2),
            "percent": memory.percent
        },
        "disk": {
            "used": round(disk.used / (1024**3), 2),
            "total": round(disk.total / (1024**3), 2),
            "percent": disk.percent
        }
    })
