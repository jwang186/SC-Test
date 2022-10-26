import boto3
import traceback
import sys
import csv
import time

def main():
  sc_ddb_table_name = "SC-ManifestsV3-xDSv3-0"
  taskSetArn="arn:aws:ecs:us-west-2:401418392244:task-set/test-sc-dualstack/ngo-service-awsvpc-default/ecs-svc/2791963755505496469"
  db_client = boto3.client('dynamodb', region_name='us-west-2')
  get_item_response = db_client.get_item(TableName=sc_ddb_table_name, Key={"Id": {'S': taskSetArn}})

  print(get_item_response)
  item = get_item_response["Item"]
  print(item)
if __name__ == "__main__":
  main()
