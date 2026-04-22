import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="ValidateExpenseLogicApp")
@app.route(route="ValidateExpenseLogicApp", methods=["POST"])
def validate_expense_logic_app(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        
        amount = req_body.get("amount", 0)
        category = req_body.get("category", "")
        
        # Business logic
        valid_categories = ["travel", "meals", "supplies", "equipment", "software", "other"]
        is_valid = category in valid_categories and amount > 0
        
        return func.HttpResponse(
            body=json.dumps({
                "isValid": is_valid,
                "isAutoApprovable": amount < 100
            }),
            mimetype="application/json",
            status_code=200
        )
    except Exception:
        return func.HttpResponse("Invalid Request", status_code=400)