import boto3

myClient = boto3.client('s3')

myBuckets = myClient.list_buckets()['Buckets']

for bucket in myBuckets:
	print(bucket['Name'])