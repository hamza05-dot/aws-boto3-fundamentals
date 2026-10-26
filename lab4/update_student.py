from decimal import Decimal
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def update_student():
    student_id = input("Student ID: ").strip()
    field      = input("Field (name/email/program/year): ").strip()
    value      = input("New value: ").strip()

    if field in ("year", "grade"):
        value = Decimal(value)

    try:
        response = table.update_item(
            Key={"student_id": student_id},
            UpdateExpression="SET #field = :value",
            ExpressionAttributeNames={"#field": field},
            ExpressionAttributeValues={":value": value},
            ConditionExpression="attribute_exists(student_id)",
            ReturnValues="ALL_NEW",
        )
        print("Updated:", response["Attributes"])
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(f"No student with ID {student_id}")
        else:
            raise


if __name__ == "__main__":
    update_student()
