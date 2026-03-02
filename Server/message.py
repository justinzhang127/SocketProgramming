def parse_message(raw_message):
    parts = raw_message.split("|")
    command = parts[0]

    if command == "DISCOVER":
        return {}
    elif command == "LOGIN":
        return {}
    elif command == "LOGOUT":
        return {}
    elif command == "CREATE_GROUP":
        return {}
    elif command == "JOIN_GROUP":
        return {}
    elif command == "LEAVE_GROUP":
        return {}
    elif command == "SEND_PRIVATE":
        return {}
    elif command == "SEND_GROUP":
        return {}
    else:
        return {}