import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def get_student():
    student_id = input("Student ID: ").strip()
    response = table.get_item(Key={"student_id": student_id})

    if "Item" not in response:
        print(f"No student with ID {student_id}")
        return

    for key, value in response["Item"].items():
        print(f"  {key:<14}: {value}")


if __name__ == "__main__":
    get_student()
