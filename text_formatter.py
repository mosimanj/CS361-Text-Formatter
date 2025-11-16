import zmq
import json


def format_text_sentence(text):
    """
    Format text as sentence case (capitalize first letter of every sentence)
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    formatted = ' '.join(text.split())

    # split formatted text by sentence
    sentences = []
    current = ""
    punctuation = ".!?"
    for char in formatted:
        current += char
        if char in punctuation:
            sentences.append(current)
            current = ""
            
    if current:
        sentences.append(current)

    # capitalize first letter of every sentence
    upper_sentences = []
    if sentences:
        for s in sentences:
            s = s.strip()
            upper_sentences.append(s[0].upper() + s[1:] if len(s) > 1 else s.upper())

    return " ".join(upper_sentences)


def format_text_upper(text):
    """
    Convert all text to uppercase
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    formatted = ' '.join(text.split())

    return formatted.upper()


def format_text_lower(text):
    """
    Convert all text to lowercase
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    formatted = ' '.join(text.split())

    return formatted.lower()


def format_text_title(text):
    """
    Convert text to title case (capitalize first letter of each word)
    Also removes extra spaces and trims whitespace
    """
    if not text:
        return ""

    formatted = ' '.join(text.split())

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
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    #TODO: we need to agree as a team which of our services use which ports
    #TODO: so we don't step on each other's toes

    port = 5555
    socket.bind(f"tcp://*:{port}")

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
            message = socket.recv_string()
            request_count += 1

            print(f"[Request #{request_count}] Received: {message}")

            try:
                request = json.loads(message)

                text = request.get("text", "")
                format_type = request.get("format_type", "sentence")

                formatted_text, error = format_text(text, format_type)

                if error:
                    response = {
                        "formatted_text": "",
                        "error": error
                    }
                else:
                    response = {
                        "formatted_text": formatted_text
                    }

                response_json = json.dumps(response)
                socket.send_string(response_json)

                print(f"[Request #{request_count}] Sent: {response_json}")
                print()

            except json.JSONDecodeError as e:
                error_response = {
                    "formatted_text": "",
                    "error": f"Invalid JSON: {str(e)}"
                }
                socket.send_string(json.dumps(error_response))
                print(f"[Request #{request_count}] Error: Invalid JSON")
                print()

            except Exception as e:
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
