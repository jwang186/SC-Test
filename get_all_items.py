import boto3
import traceback
import sys
import csv
import time
from botocore.paginate import TokenEncoder

def main():
  sc_ddb_table_name = "SC-ManifestsV3-xDSv3-0"

  db_client = boto3.client('dynamodb', region_name='us-west-2')
  db_paginator = db_client.get_paginator('scan')

  starting_token = None
  pagination_config = {
    "MaxItems": 100,  ## maximum number of items to return in this paginate
    "PageSize": 10,   ## in each page the number of items
  }
  count = 0
  encoder = TokenEncoder()
  ecs_taskset_arn_prefix = 'arn:aws:ecs:us-west-2:401418392244:task-set/test-sc-dualstack/go-service-awsvpc-default'
  failure_count = 0
  success_count = 0
  failure_record = {}

  while True:
    if starting_token:
      pagination_config['StartingToken'] = starting_token

    db_page_response = db_paginator.paginate(
        TableName=sc_ddb_table_name,
        Select='ALL_ATTRIBUTES',
        ReturnConsumedCapacity='NONE',
        ConsistentRead=True,
        PaginationConfig=pagination_config,
        FilterExpression='begins_with(Id, :id)',
        ExpressionAttributeValues={
          ':id': {'S': ecs_taskset_arn_prefix}
        })

    for page in db_page_response:
      if "LastEvaluatedKey" in page:
        starting_token = encoder.encode({"ExclusiveStartKey": page['LastEvaluatedKey']})
      else:
        starting_token = None

      for item in page['Items']:
        arn = item['Id']['S']
        print(item)
        print(arn)
        print(item['Content']['B'])

        count = count + 1
        if count%10 == 0:
          time.sleep(0.2)

    if not starting_token:
      print("Scanned all items in DDB ")
      break

  print("Summary")
  print("Success count: " + str(success_count))
  print("Failure count: " + str(failure_count))
  print("Total count: " + str(count))

  with open("failure_record.csv", 'w') as output:
    cw = csv.writer(output)
    for key in failure_record.keys():
      cw.writerow([key, failure_record[key]])

if __name__ == "__main__":
  main()