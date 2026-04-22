# Desmond Murphy - 040946131 - CST8917 - Final Assignment - April 21

## Version A Summary

- Description: Version A is a code-first implementation that utilizes the Asynchronous HTTP Pattern for function chaining and the Human Interaction Pattern to accept or reject expense requests.

- Design Decisions
  - Used a stateful Orchestrator to manage the workflow cycle
  - Used an external HTTP trigger for manager callbacks
  - Using `yield context.wait_for_external_event("ManagerApproval")` as an  event driven wait state
- Challenges
  - Minimal challenges with the code-first approach
  - I had some issues configuring and running the function that I needed to resolve

## Version B Sumary

- Description: Version B uses a low-code/no-code solution through Azure Logic Apps to recreate the workflow of Version A.

- Design Decisions
  - Asynchronous callbacks
  - Native wait state
  - Escalation Path
  - Workflow involves many connectors including:
    - Service Bus Connectors, sending emails, function calls and conditions
- Challenges:
  - I had a lot of trouble configuring logic apps and setting it up and in the end it wasn't working completely
  - I wasnt able to locally test the run

## Comparison Analysis

### Development Experience

- Personally, I found the development experience for Version A much easier. I think it might be because I have development experience, but I find it easier and more enjoyable to develop with Python and troubleshoot by looking at logs and error messages. On the other hand, I could see how somebody might enjoy using logic apps to emulate the same workflow, especially if they don't have development experience, but for me, I found it very frustrating to set up connectors and properties within them.

### Testability

- Again I found it easier to test in scenario A throuh http calls. The only slight annoyance from this testing was having to grab the Instance ID from each specific request and add it to the variable before being able to run the manager decisions which add a bit of friction to testing. Testing with logic apps just involve manually passing JSON messages into the service bus queue and is harder to automate. Using a durable function we can test locally on our system and save costs whereas with the logic apps setup everything needs to be set up in the cloud and doesn't have true local testing like with a durable function.

### Error Handling

- In scenario A with the durable function pattern it gives you the ability to handle errors just like any standard code development, usinf ty/except blocks or using retry methods native to durable functions. This gives you more control over how errors are handled. As for the logic app workflow in scenario B, some connectors have built in retry settings that can be changed, i'm not aware of other ways to handle errors but im sure it has other built in error handling but I wasn't able to figure it out. I prefer controlling the error handling and debugging via code first approaches.

### Human Interaction Pattern

- Handling the Human Interaction pattern is an area where I think logic apps have an advantage over the code-first durable function approach. Using the Send Approval Email To Manager connector to handle manager interaction with the request is much more intuitive than handling the approval process through two separate HTTP calls that require the instance ID to be passed to them. I'm sure that with a code-first approach, it could be set up to send emails to managers about their decisions, but it would be a lot harder to implement.

### Observability

- The observability that is provided through logic apps with the Visual Run History is probably superior to searching through Application Insights and error logs. That being said I find that the error messages within the Visual Run History can be a little more vague and harder to track down the exact error or how to fix it, its a lot easier to paste an error message online and find people discussing the error vs logic apps errors.

### Cost

Going with Scenario A from my understanding will always be cheaper than Scenario B. Due to Azure offering a monthly free grant for the first million requests the overall price per month would be minimal. On the other hand Logic Apps can be much more expensive and requires the service bus base fee which makes it more costly especially at only 100 expense/day.

End with a recommendation (200-300 words): If a team asked you to build this for production, which approach would you choose and why? When would you choose the other instead?

## Recommendation

If a team me to build this I would always choose to go with the first approach as I am much more comfortable implementing and working on it. This experience trying to setup the logic app workflow was extremely fristrating and I would avoid it as much as possible in the future until I am more comfortable with it and feel like I could actually set up a proper workflow.

## References

[Durable Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/durable-functions/)

[Service Bus Connector Documentation](https://learn.microsoft.com/en-us/connectors/servicebus/)

## AI Disclosure

- I used AI to help me troubleshoot the function_app.py and help to setup the http test files properly.
- I also used AI to help design slides.
