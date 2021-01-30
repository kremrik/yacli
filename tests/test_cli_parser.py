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
        gold = [("-v",)]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_bool_args(self):
        arg_string = "-v --w"
        gold = [("-v",), ("--w",)]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_one_kwarg(self):
        arg_string = "--name joe"
        gold = [("--name", "joe")]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_kwargs(self):
        arg_string = "--first-name joe --last-name schmo"
        gold = [("--first-name", "joe"), ("--last-name", "schmo")]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_kwargs_sandwiching_bool(self):
        arg_string = "--first-name joe -v --last-name schmo"
        gold = [("--first-name", "joe"), ("-v",), ("--last-name", "schmo")]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)

    def test_two_bools_sandwiching_kwarg(self):
        arg_string = " -x --name joe -v"
        gold = [("-x",), ("--name", "joe"), ("-v",)]
        output = parse_cli_string(arg_string)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
