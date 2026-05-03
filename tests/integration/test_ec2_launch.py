import time

from lib.ec2_backend import launch_instance, get_instance_state, terminate_instance
from lib.ssm_backend import send_command


def wait_for_instance_running(instance_id, timeout=10):
    """
    Waits until instance state becomes 'running'.
    """
    start = time.time()

    while time.time() - start < timeout:
        state = get_instance_state(instance_id)
        if state == "running":
            return True
        time.sleep(1)

    raise TimeoutError("Instance did not reach running state in time.")


def wait_for_ssm_ready(instance_id, timeout=15):
    """
    Waits until SSM command succeeds.
    """
    start = time.time()

    while time.time() - start < timeout:
        response = send_command(instance_id)

        if response.get("Success"):
            return response

        time.sleep(1)

    raise TimeoutError("SSM did not become ready in time.")


def test_instance_launch_and_ssm_ready():
    """
    Integration test:
    - Launch EC2 instance
    - Wait for running state
    - Send SSM command
    - Expect success
    - Terminate instance
    """

    instance_id = launch_instance(config={})

    try:
        wait_for_instance_running(instance_id)
        response = send_command(instance_id)
        assert response["Success"], "SSM command should succeed after readiness."

    finally:
        terminate_instance(instance_id)