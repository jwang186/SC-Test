./create-cluster.sh
./run-instances.sh

sleep 60

./create-service-awsvpc-default.sh
./create-service-awsvpc-nondefault.sh
./create-service-bridge-default.sh
./create-service-bridge-nondefault.sh