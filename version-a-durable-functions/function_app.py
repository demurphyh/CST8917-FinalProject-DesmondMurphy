import azure.functions as func
import azure.durable_functions as df
import datetime

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="start_approval", methods=["POST"]) # <--- MUST HAVE THIS
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    payload = req.get_json()
    instance_id = await client.start_new("expense_approval_orchestrator", None, payload)
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def expense_approval_orchestrator(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    amount = input_data.get("amount")

    # 1. Validation Activity
    is_valid = yield context.call_activity("validate_expense", input_data)
    if not is_valid:
        return "Rejected: Validation Failed"

    # 2. Check for Auto-Approval
    if amount < 100:
        yield context.call_activity("send_notification", {"status": "Approved", "msg": "Auto-approved"})
        return "Auto-Approved"

    # 3. Human Interaction Pattern
    timeout_task = context.create_timer(context.current_utc_datetime + datetime.timedelta(seconds=30))
    approval_task = context.wait_for_external_event("ManagerApproval")

    winner = yield context.task_any([approval_task, timeout_task])

    if winner == approval_task:
        status = approval_task.result
    else:
        status = "Escalated"

    yield context.call_activity("send_notification", {"status": status})
    return status

@app.activity_trigger(input_name="inputData")
def validate_expense(inputData: dict):
    # Logic: Reject missing fields or invalid category
    valid_categories = ["travel", "meals", "supplies", "equipment", "software", "other"]
    required = ["employeeName", "employeeEmail", "amount", "category"]
    
    if not all(k in inputData for k in required):
        return False
    if inputData.get("category") not in valid_categories:
        return False
    return True

@app.activity_trigger(input_name="details")
def send_notification(details: dict):
    # In a real app, you'd use SendGrid here. For the lab, printing is fine.
    print(f"NOTIFICATION SENT: {details.get('status')}")
    return f"Notification sent for {details.get('status')}"


@app.function_name(name="manager_approval_endpoint")
@app.route(route="approve/{instanceId}")
@app.durable_client_input(client_name="client")
async def manager_approval_endpoint(req: func.HttpRequest, client: df.DurableOrchestrationClient) -> func.HttpResponse:
    # Manual extraction if the automatic binding fails
    instance_id = req.route_params.get('instanceId')
    action = req.params.get('action')
    
    await client.raise_event(instance_id, "ManagerApproval", action)
    return func.HttpResponse(f"Event sent to {instance_id}")