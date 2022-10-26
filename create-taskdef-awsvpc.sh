aws --endpoint-url https://madison.us-west-2.amazonaws.com \
--region us-west-2 ecs-sc register-task-definition \
--cli-input-json file://task_def_awsvpc.json \
--debug