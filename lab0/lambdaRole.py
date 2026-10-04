import boto3
import io
import zipfile
sts      = boto3.client("sts")
lambda_client = boto3.client("lambda")
account  = sts.get_caller_identity()["Account"]
role_arn = f"arn:aws:iam::{account}:role/LabRole"
name = "lab0-function"
package = io.BytesIO()

with zipfile.ZipFile(package, "w") as z:
    z.writestr(
        "lambda_function.py",
        """
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Hello from Lambda!"
    }
"""
    )

package_bytes = package.getvalue()


response = lambda_client.create_function(
    FunctionName=name,
    Runtime="python3.13",
    Role=role_arn,
    Handler="lambda_function.lambda_handler",
    Code={"ZipFile": package_bytes},
)

print(response["FunctionArn"])
