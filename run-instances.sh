aws ec2 run-instances --region us-west-2 --image-id ami-073b57ab4842bb222 \
--count 1 --instance-type m5.4xlarge --key-name sc-test \
--security-group-ids sg-09ca18e5159506fc3 --subnet-id subnet-075b5028bb72e9190 \
--user-data file://userdata.txt --iam-instance-profile Name=ecsInstanceRole \
--associate-public-ip-address
# ami-0c220d6feb6e68ec8