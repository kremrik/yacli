from yacli.cli_parser import parse_cli_string
import unittest


class test_parse_cli_string(unittest.TestCase):
    def test_no_args(self):
        arg_string = ""
        gold = []
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_one_bool_arg(self):
        arg_string = "-v"
        gold = [("-v", None, "flag")]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_bool_args(self):
        arg_string = "-v --w"
        gold = [
            ("-v", None, "flag"),
            ("--w", None, "flag")
        ]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_one_kwarg(self):
        arg_string = "--name joe"
        gold = [("--name", "joe", "kwarg")]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_kwargs(self):
        arg_string = "--first-name joe --last-name schmo"
        gold = [
            ("--first-name", "joe", "kwarg"),
            ("--last-name", "schmo", "kwarg")
        ]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_kwargs_sandwiching_bool(self):
        arg_string = "--first-name joe -v --last-name schmo"
        gold = [
            ("--first-name", "joe", "kwarg"),
            ("-v", None, "flag"),
            ("--last-name", "schmo", "kwarg")
        ]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_bools_sandwiching_kwarg(self):
        arg_string = " -x --name joe -v"
        gold = [
            ("-x", None, "flag"),
            ("--name", "joe", "kwarg"),
            ("-v", None, "flag")
        ]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_one_varargs(self):
        arg_string = "--foo 1 2"
        gold = [
            ("--foo", ["1", "2"], "varargs"),
        ]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_varargs_sandwiched(self):
        arg_string = "--foo hi --bar 1 2 --baz bye"
        gold = [
            ("--foo", "hi", "kwarg"),
            ("--bar", ["1", "2"], "varargs"),
            ("--baz", "bye", "kwarg"),
        ]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
