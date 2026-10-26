from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def query_demo():
    student_id = input("Student ID: ").strip()

    # Query: goes straight to one partition. Fast and cheap.
    response = table.query(
        KeyConditionExpression=Key("student_id").eq(student_id)
    )

    for item in response.get("Items", []):
        print(f"{item['student_id']:<12} {item.get('name', '-'):<24} "
              f"{item.get('program', '-')}")
    print(f"\n{len(response.get('Items', []))} item(s)")


if __name__ == "__main__":
    query_demo()
