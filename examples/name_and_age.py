from yacli import parse_args


template = {
    "--name": {"required": True, "help": "Your name"},
    "--age": {
        "required": True,
        "help": "Your age",
        "arg_type": int,
    },
}


if __name__ == "__main__":
    args, unexpected = parse_args(
        template=template,
        app_name="name-and-age",
    )
    name = args.get("--name")
    age = args.get("--age")
    print(f"Hello, {name} ({age})")
    print(f"Only {100-age} more years until you're 100")
