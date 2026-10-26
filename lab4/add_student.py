from decimal import Decimal
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def add_student():
    item = {
        "student_id": input("Student ID: ").strip(),
        "name":       input("Full name: ").strip(),
        "email":      input("Email: ").strip(),
        "program":    input("Program: ").strip(),
    }
    year = input("Year (number): ").strip()
    if year.isdigit():
        item["year"] = Decimal(year)

    try:
        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(student_id)",
        )
        print(f"Added student {item['student_id']}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("That student already exists. Use Update instead.")
        else:
            raise


if __name__ == "__main__":
    add_student()
