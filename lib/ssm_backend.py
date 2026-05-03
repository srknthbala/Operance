import json
import time
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / "state" / "aws_state.json"

def _load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def _save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def send_command(instance_id):
    """
    Simulates AWS SSM SendCommand behavior.
    Fails if SSM is not yet registered.
    """
    state = _load_state()

    if instance_id not in state["instances"]:
        return {
            "Success": False,
            "Error": {
                "Code": "InvalidInstanceId",
                "Message": "Instance does not exist."
            }
        }

    # Simulate SSM registration delay (5 seconds after launch)
    instance = state["instances"][instance_id]
    time_since_launch = time.time() - instance["created_at"]

    if time_since_launch < 5:
        return {
            "Success": False,
            "Error": {
                "Code": "TargetNotConnected",
                "Message": "Instance is not connected to SSM."
            }
        }

    # Mark SSM as online
    state["ssm_status"][instance_id] = "online"
    _save_state(state)

    return {
        "Success": True,
        "CommandId": "cmd-1234567890"
    }