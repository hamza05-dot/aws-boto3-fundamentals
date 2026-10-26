import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def delete_student():
    student_id = input("Student ID: ").strip()

    try:
        response = table.delete_item(
            Key={"student_id": student_id},
            ConditionExpression="attribute_exists(student_id)",
            ReturnValues="ALL_OLD",
        )
        print(f"Deleted {response.get('Attributes', {}).get('name', student_id)}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(f"No student with ID {student_id}")
        else:
            raise


if __name__ == "__main__":
    delete_student()
