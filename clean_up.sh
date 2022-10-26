aws --endpoint-url https://madison.us-west-2.amazonaws.com ecs-sc list-clusters > all_gamma_clusters.json
 
cat all_gamma_clusters.json | jq -r ".clusterArns[]" > cluster_arns
 
for cluster in `cat cluster_arns`;
do
 echo "Trying to delete $cluster ......";
 aws --endpoint-url https://madison.us-west-2.amazonaws.com ecs-sc list-tasks \
    --cluster $cluster | \
  jq -r ' .taskArns[] | [.] | @tsv ' | \
    while IFS=$'\t' read -r taskArn; do
      aws --endpoint-url https://madison.us-west-2.amazonaws.com ecs-sc stop-task \
        --cluster $cluster \
        --task $taskArn
    done
 
 aws --endpoint-url https://madison.us-west-2.amazonaws.com ecs-sc list-services \
   --cluster $cluster | \
 jq -r ' .serviceArns[] | [.] | @tsv ' | \
   while IFS=$'\t' read -r serviceArn; do
     aws --endpoint-url https://madison.us-west-2.amazonaws.com ecs-sc delete-service \
       --cluster $cluster \
       --service $serviceArn \
       --force
   done
 aws --endpoint-url https://madison.us-west-2.amazonaws.com ecs-sc delete-cluster --cluster $cluster;
 
 if [ $? == "0" ]; then
   echo "Delete $cluster successfully"
 else
   echo "Fail to delete $cluster"
 fi
done