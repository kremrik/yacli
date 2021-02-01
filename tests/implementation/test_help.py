from yacli.help import format_help_output
import unittest


class test_format_help(unittest.TestCase):
    def test_no_help(self):
        app_name = "test"
        template = {"--foo": int}
        gold = "test\n  --foo\n"
        output = format_help_output(
            app_name=app_name, template=template
        )
        self.assertEqual(gold, output)

    def test_one_help_arg(self):
        app_name = "test"
        template = {"--foo": {"help": "does foo stuff"}}
        gold = "test\n  --foo    does foo stuff\n"
        output = format_help_output(
            app_name=app_name, template=template
        )
        self.assertEqual(gold, output)

    def test_one_with_help_one_without(self):
        app_name = "test"
        template = {
            "--foo": {"help": "does foo stuff"},
            "--bar": int,
        }
        gold = "test\n  --foo    does foo stuff\n  --bar\n"
        output = format_help_output(
            app_name=app_name, template=template
        )
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
