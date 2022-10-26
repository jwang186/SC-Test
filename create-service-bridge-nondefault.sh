aws --endpoint-url https://madison.us-west-2.amazonaws.com \
--region us-west-2 ecs-sc create-service \
--cli-input-json file://test_service_bridge_nondefault.json \
--enable-execute-command \
--debug