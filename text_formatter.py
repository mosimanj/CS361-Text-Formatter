"""
Text Formatter Microservice

TODO: NOTE TO RYAN: I put this here for now but we should probably make a nice
TODO: README file that has all this info on how to use this service.

This microservice provides multiple text formatting options.
Users can specify which type of formatting they want:
- sentence: Capitalize first letter only (default)
- upper: Convert all text to uppercase
- lower: Convert all text to lowercase
- title: Capitalize first letter of each word

Communication: ZeroMQ REQ-REP pattern
Port: 5555
Protocol: JSON

Request Format:
{
    "text": "  example text  ",
    "format_type": "upper"  // Optional: "sentence", "upper", "lower", "title"
}

Response Format:
{
    "formatted_text": "EXAMPLE TEXT"
}

If format_type is not specified, defaults to "sentence" for backward compatibility
"""

import zmq
import json


def format_text_sentence(text):
    """
    Format text as sentence case (capitalize first letter only)
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    # remove extra spaces between words and trim
    formatted = ' '.join(text.split())

    # capitalize first letter if there's any text
    if formatted:
        formatted = formatted[0].upper() + formatted[1:] if len(formatted) > 1 else formatted.upper()

    return formatted


def format_text_upper(text):
    """
    Convert all text to uppercase
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    # Remove extra spaces between words and trim
    formatted = ' '.join(text.split())

    # Convert to uppercase
    return formatted.upper()


def format_text_lower(text):
    """
    Convert all text to lowercase
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    # remove extra spaces between words and trim
    formatted = ' '.join(text.split())

    # convert to lowercase
    return formatted.lower()


def format_text_title(text):
    """
    Convert text to title case (capitalize first letter of each word)
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    # remove extra spaces between words and trim
    formatted = ' '.join(text.split())

    # capitalize first letter of each word
    return formatted.title()


def format_text(text, format_type="sentence"):
    """
    Format text according to specified format type
    """
    # normalize format_type to lowercase
    format_type = format_type.lower() if format_type else "sentence"

    # route to appropriate formatting function
    if format_type == "sentence":
        return format_text_sentence(text), None
    elif format_type == "upper":
        return format_text_upper(text), None
    elif format_type == "lower":
        return format_text_lower(text), None
    elif format_type == "title":
        return format_text_title(text), None
    else:
        return "", f"Invalid format_type: '{format_type}'. Valid options: 'sentence', 'upper', 'lower', 'title'"


def main():
    """
    Main service loop
    Sets up ZeroMQ and listens for formatting requests
    """
    # create zeromq context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Bind to port 5555
    #TODO: we need to agree as a team which of our services use which ports
    #TODO: so we don't step on each other's toes

    port = 5555
    socket.bind(f"tcp://*:{port}")

    # printing to it's easy to see what's going on
    print("=" * 60)
    print("Text Formatter Microservice - Enhanced Version")
    print("=" * 60)
    print(f"Status: Running")
    print(f"Port: {port}")
    print(f"Format types: sentence, upper, lower, title")
    print(f"Waiting for requests...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()

    request_count = 0

    try:
        while True:
            # wait for request from client
            message = socket.recv_string()
            request_count += 1

            print(f"[Request #{request_count}] Received: {message}")

            try:
                # parse JSON request
                request = json.loads(message)

                # get text and format_type from request
                text = request.get("text", "")
                format_type = request.get("format_type", "sentence")

                # format the text
                formatted_text, error = format_text(text, format_type)

                # create response
                if error:
                    response = {
                        "formatted_text": "",
                        "error": error
                    }
                else:
                    response = {
                        "formatted_text": formatted_text
                    }

                # send JSON response
                response_json = json.dumps(response)
                socket.send_string(response_json)

                print(f"[Request #{request_count}] Sent: {response_json}")
                print()

            except json.JSONDecodeError as e:
                # handle invalid JSON
                error_response = {
                    "formatted_text": "",
                    "error": f"Invalid JSON: {str(e)}"
                }
                socket.send_string(json.dumps(error_response))
                print(f"[Request #{request_count}] Error: Invalid JSON")
                print()

            except Exception as e:
                # handle other errors
                error_response = {
                    "formatted_text": "",
                    "error": f"Server error: {str(e)}"
                }
                socket.send_string(json.dumps(error_response))
                print(f"[Request #{request_count}] Error: {str(e)}")
                print()

    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Shutting down Text Formatter service...")
        print(f"Total requests processed: {request_count}")
        print("=" * 60)

    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
