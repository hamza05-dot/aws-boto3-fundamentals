import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def create_table():
    try:
        new_table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "student_id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "student_id", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print("Creating table, please wait ...")
        new_table.wait_until_exists()
        print(f"Table '{TABLE_NAME}' is ACTIVE.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print("Table already exists.")
        else:
            raise


if __name__ == "__main__":
    create_table()
