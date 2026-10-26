from boto3.dynamodb.conditions import Attr
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def search_students():
    term = input("Program contains: ").strip()

    # Scan + filter: reads the whole table, returns the matches
    response = table.scan(
        FilterExpression=Attr("program").contains(term)
    )

    for item in response.get("Items", []):
        print(f"{item['student_id']:<12} {item.get('name', '-'):<24} "
              f"{item.get('program', '-')}")
    print(f"\n{len(response.get('Items', []))} match(es)")


if __name__ == "__main__":
    search_students()
