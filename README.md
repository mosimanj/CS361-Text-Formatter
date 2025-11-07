# Text Formatter Microservice

## Description and Features
This microservice provides multiple text formatting options.

Users can specify which type of formatting they want:
- sentence: Capitalize first letter of every sentence (default)
- upper: Convert all text to uppercase
- lower: Convert all text to lowercase
- title: Capitalize first letter of each word

## Communication Contract

### Communication Method
ZeroMQ REQ-REP pattern
- Port: 5555
- Protocol: JSON

### How to Request Data
Each request must be a JSON object with parameters:
- “text” (string, required): The main text that you want to format. Always strips whitespace and remove extra spaces within the text. Has additional formatting options that can be indicated by “format_type” parameter.
- “format_type” (string, optional – defaults to “sentence”). All possible values include:
    - “sentence”: capitalizes the first alphabetic character of every sentence
    - “upper”: converts all characters to uppercase
    - “lower”: converts all characters to lowercase
    - “title: capitalizes first letter of each word

```
Example Call:

request = {
    "text": "example sentence.     another example sentence.",
    "format_type": "sentence"
}
request_json = json.dumps(request)

#  Context and Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Send request
socket.send_string(request_json)
```

### How to Receive Data
Each response will be a JSON object with parameters:
- “formatted_text” (required): the formatted text
- “error" (optional): error message if microservice encountered an error
```
Example Call:

#  Receive response and parse
response_json = socket.recv_string()
response = json.loads(response_json)
formatted_text = response.get("formatted_text", "")
print(formatted_text) # Example sentence. Another example sentence.
```
### UML sequence diagram