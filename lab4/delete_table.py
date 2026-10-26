import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "hamza_Students"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def delete_table():
    confirm = input(f"Type the table name '{TABLE_NAME}' to confirm deletion: ").strip()

    if confirm != TABLE_NAME:
        print("Confirmation failed. Deletion canceled.")
        return

    try:
        table.delete()
        print("Deleting table, please wait ...")
        table.wait_until_not_exists()
        print(f"Table '{TABLE_NAME}' deleted.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print("Table does not exist.")
        else:
            raise


if __name__ == "__main__":
    delete_table()
