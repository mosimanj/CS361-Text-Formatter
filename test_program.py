import zmq
import json


def test_formatter(description, text, format_type="sentence"):
    """Run a test case against the microservice"""
    print(f"\n{'=' * 60}")
    print(f"TEST: {description}")
    print(f"{'=' * 60}")

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    request = {"text": text, "format_type": format_type}
    print(f"Request: {json.dumps(request, indent=2)}")

    socket.send_string(json.dumps(request))
    response = json.loads(socket.recv_string())

    print(f"Response: {json.dumps(response, indent=2)}")

    if response.get("error"):
        print(f"✗ Error: {response['error']}")
    else:
        print(f"✓ Formatted text: {response['formatted_text']}")

    socket.close()
    context.term()


if __name__ == "__main__":
    print("TEXT FORMATTER TEST PROGRAM")
    print("Testing various formatting scenarios...\n")

    # sentence case
    test_formatter("Sentence case formatting",
                   "  hello world.  goodbye world.  ",
                   "sentence")

    # uppercase
    test_formatter("Uppercase formatting",
                   "  hello world  ",
                   "upper")

    # lowercase
    test_formatter("Lowercase formatting",
                   "  HELLO WORLD  ",
                   "lower")

    # title case
    test_formatter("Title case formatting",
                   "  hello world  ",
                   "title")

    # default (no format_type entered)
    test_formatter("Default formatting (sentence)",
                   "  hello world.  ",
                   "")

    # invalid format_type entered
    test_formatter("Invalid format_type (error test)",
                   "  hello world  ",
                   "something_invalid")

    print(f"\n{'=' * 60}")
    print("ALL TESTS COMPLETE")
    print(f"{'=' * 60}")
