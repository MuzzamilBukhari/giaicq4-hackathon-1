# VLA Text-to-Action ROS 2 Action Contract

## Action Definition

```
# Goal: The text instruction to execute
string text_instruction
---
# Result: The outcome of the action
bool success
string message
string[] executed_commands
---
# Feedback: Progress information during execution
string current_step
float32 progress
string status
```

## Action Name
`/process_text_action`

## Message Types

### Goal (TextToAction_Goal)
- `text_instruction`: The natural language command from the user

### Result (TextToAction_Result)
- `success`: Whether the action was executed successfully
- `message`: Descriptive message about the result
- `executed_commands`: List of commands that were actually executed

### Feedback (TextToAction_Feedback)
- `current_step`: Current step being executed in the pipeline
- `progress`: Progress percentage (0.0 to 1.0)
- `status`: Current status message

## State Transitions

1. **Goal Received**: Action server receives the text instruction
2. **Processing**: Server parses and processes the instruction
3. **Execution**: Robot executes the planned actions
4. **Completed**: Action completes with success/failure result

## Example Usage

### Client Sends Goal
```
{
  "text_instruction": "Move the robot to the table and pick up the red object"
}
```

### Server Provides Feedback
```
{
  "current_step": "Parsing instruction",
  "progress": 0.2,
  "status": "Identified navigation and manipulation components"
}
```

### Server Returns Result
```
{
  "success": true,
  "message": "Successfully navigated to table and identified red object",
  "executed_commands": [
    "navigate_to(x=2.5, y=1.0)",
    "detect_object(color='red')"
  ]
}
```

## Error Handling

- Invalid instructions return success=false with descriptive message
- Execution failures provide detailed error information
- Timeout after 30 seconds if no progress is made