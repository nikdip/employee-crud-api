import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('employee_info')


def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    try:
        # METHOD (SAFE)
        http_method = event.get("httpMethod")

        if not http_method:
            http_method = (
                event.get("requestContext", {})
                .get("http", {})
                .get("method")
            )

        # PATH (SAFE)
        path = (
            event.get("rawPath")
            or event.get("path")
            or event.get("requestContext", {})
            .get("http", {})
            .get("path")
            or ""
        )

        print("METHOD =", http_method)
        print("PATH =", path)

        # REMOVE STAGE
        path = path.replace("/production", "")

        if not http_method:
            return {
                "statusCode": 400,
                "body": "No HTTP method received"
            }

        # ROUTES
        if http_method == "GET" and path == "/status":
            return build_response(200, "Service is operational")

        if http_method == "GET" and path == "/employees":
            return get_employees()

        if http_method == "GET" and path == "/employee":
            emp_id = event.get("queryStringParameters", {}).get("employeeid")
            return get_employee(emp_id)

        if http_method == "POST" and path == "/employee":
            body = json.loads(event.get("body") or "{}")
            return save_employee(body)

        if http_method == "PATCH" and path == "/employee":
            body = json.loads(event.get("body") or "{}")
            return modify_employee(
                body.get("employeeId"),
                body.get("updateKey"),
                body.get("updateValue")
            )

        if http_method == "DELETE" and path == "/employee":
            body = json.loads(event.get("body") or "{}")
            return delete_employee(body.get("employeeId"))

        return build_response(404, f"NOT FOUND: {http_method} {path}")

    except Exception as e:
        print("ERROR:", str(e))
        return build_response(500, str(e))



# DATABASE FUNCTIONS


def get_employee(emp_id):
    res = table.get_item(Key={"employeeid": emp_id})
    return build_response(200, res.get("Item"))


def get_employees():
    res = table.scan()
    return build_response(200, {"employees": res.get("Items", [])})


def save_employee(data):
    table.put_item(Item=data)
    return build_response(200, {"message": "saved", "item": data})


def modify_employee(emp_id, key, value):
    res = table.update_item(
        Key={"employeeid": emp_id},
        UpdateExpression=f"SET {key} = :v",
        ExpressionAttributeValues={":v": value},
        ReturnValues="UPDATED_NEW"
    )
    return build_response(200, res.get("Attributes"))


def delete_employee(emp_id):
    res = table.delete_item(
        Key={"employeeid": emp_id},
        ReturnValues="ALL_OLD"
    )
    return build_response(200, res.get("Attributes"))



# RESPONSE


def build_response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder)
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)