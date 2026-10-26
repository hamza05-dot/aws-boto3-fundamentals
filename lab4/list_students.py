import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def list_students():
    items = []
    scan_kwargs = {}

    while True:
        response = table.scan(**scan_kwargs)
        items.extend(response.get("Items", []))

        if "LastEvaluatedKey" not in response:
            break
        scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

    for item in sorted(items, key=lambda x: x["student_id"]):
        print(f"{item['student_id']:<12} {item.get('name', '-'):<24} "
              f"{item.get('program', '-')}")
    print(f"\n{len(items)} student(s)")


if __name__ == "__main__":
    list_students()
