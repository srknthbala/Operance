EC2 Launch Validation – Integration Test Investigation
Team: EC2 Launch Validation
Priority: P2
Status: Open

Summary:

* The integration test `test_instance_launch_and_ssm_ready` in `tests/integration/test_ec2_launch.py` has begun failing in CI.
* This test validates EC2 instance launch and post-launch verification using AWS Systems Manager (SSM).
* Initial investigation suggests the integration test may not correctly handle instance readiness before executing the SSM verification step.

-------------------------------------------------------------------------------------

Observed Behavior:

* RunInstances → Success
* Instance state → running
* SSM SendCommand → Failed
* Error: TargetNotConnected

CI Failure:

"AssertionError: SSM command should succeed after readiness."

-------------------------------------------------------------------------------------

Expected Test Behavior

The test should:

[] Launch an EC2 instance using a valid configuration
[] Wait for the instance to reach running state
[] Verify the instance is reachable via SSM
[] Execute a verification command through SSM
[] Assert successful command execution
[] Terminate the instance after validation
[] Ensure no residual resources remain

-------------------------------------------------------------------------------------

Assignment:

Investigate the failing integration test and restore stability.

* Backend simulation code is functioning correctly and should not be modified.
* The failure originates from the integration test located in `tests/integration/test_ec2_launch.py`.
* Review the test workflow and ensure it properly waits for instance readiness before verifying SSM command execution.
* Use `./run_ci.sh` from the repository root to execute the CI integration test locally while investigating the failure.

-------------------------------------------------------------------------------------

Success Criteria

[] Root cause identified
[] Integration test logic corrected
[] Test passes consistently across multiple runs
[] No flakiness introduced
[] All resources properly cleaned up