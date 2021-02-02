from yacli.yacli import (
    ValidationException,
    parse_args,
)
import unittest


class test_parse_args(unittest.TestCase):
    def test(self):
        template = {
            "--foo": ...,
            "-v": {"required": False, "default": False},
        }
        inpt = ["--foo", "hi", "--verbose"]
        gold = (
            {"--foo": ["hi"], "-v": False},
            {"--verbose": None},
        )
        output = parse_args(template=template, inpt=inpt)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
