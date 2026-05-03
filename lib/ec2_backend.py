import json
import time
import uuid
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / "state" / "aws_state.json"


def _load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def _save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def launch_instance(config=None):
    """
    Simulates EC2 RunInstances.
    Creates an instance in 'pending' state.
    """
    state = _load_state()

    instance_id = f"i-{uuid.uuid4().hex[:12]}"

    state["instances"][instance_id] = {
        "state": "pending",
        "created_at": time.time()
    }

    # When instance is created, SSM is not yet registered
    state["ssm_status"][instance_id] = "not_registered"

    _save_state(state)

    return instance_id


def get_instance_state(instance_id):
    """
    Returns current instance state.
    Automatically transitions pending → running after 3 seconds.
    """
    state = _load_state()

    instance = state["instances"].get(instance_id)
    if not instance:
        raise Exception("InstanceNotFound")

    # Simulate async transition
    if instance["state"] == "pending":
        if time.time() - instance["created_at"] > 3:
            instance["state"] = "running"
            _save_state(state)

    return instance["state"]


def terminate_instance(instance_id):
    """
    Simulates EC2 TerminateInstances.
    """
    state = _load_state()

    if instance_id in state["instances"]:
        del state["instances"][instance_id]

    if instance_id in state["ssm_status"]:
        del state["ssm_status"][instance_id]

    _save_state(state)

    return True
