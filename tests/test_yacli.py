from yacli.yacli import (
    ValidationException,
    parse_cli,
    required,
    arg_type,
    choice,
    default,
    transform_argument,
    transform_arguments,
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


class test_transform_arguments(unittest.TestCase):
    def test_1_passes(self):
        template = {
            "--foo": int,
            "--bar": {
                "required": False,
            },
            "--baz": {
                "required": False,
                "default": False,
            },
        }
        given = {
            "--foo": "1",
        }
        gold = {"--foo": 1, "--baz": False}
        output = transform_arguments(template, given)
        self.assertEqual(gold, output)

    def test_2_fails(self):
        template = {
            "--foo": int,
            "--bar": {
                "required": False,
                "choices": ["hi", "bye"],
            },
            "--baz": {
                "required": False,
                "default": False,
            },
        }
        given = {"--foo": "1", "--bar": "hello"}
        with self.assertRaises(ValidationException):
            transform_arguments(template, given)


class test_transform_argument(unittest.TestCase):
    def test_no_params_given_value(self):
        arg = "--foo"
        params = int
        given = "1"
        gold = ("--foo", 1)
        output = transform_argument(arg, params, given)
        self.assertEqual(gold, output)

    def test_no_given_value_not_required(self):
        arg = "--foo"
        params = {"required": False}
        given = None
        gold = None
        output = transform_argument(arg, params, given)
        self.assertEqual(gold, output)

    def test_assortment_passes(self):
        arg = "--foo"
        params = {
            "required": False,
            "arg_type": float,
            "choice": [1.2, 2.3],
        }
        given = "1.2"
        gold = ("--foo", 1.2)
        output = transform_argument(arg, params, given)
        self.assertEqual(gold, output)

    def test_assortment_fails(self):
        arg = "--foo"
        params = {
            "required": True,
            "arg_type": float,
            "choice": [1.2, 2.3],
        }
        given = None
        with self.assertRaises(ValidationException):
            transform_argument(arg, params, given)

    def test_assortment_with_default(self):
        arg = "--foo"
        params = {"required": False, "default": 0}
        given = None
        gold = ("--foo", 0)
        output = transform_argument(arg, params, given)
        self.assertEqual(gold, output)

    def test_assortment_with_default_and_help(self):
        arg = "--foo"
        params = {
            "required": False,
            "default": 0,
            "help": "does foo",
        }
        given = None
        gold = ("--foo", 0)
        output = transform_argument(arg, params, given)
        self.assertEqual(gold, output)


# testing arg transformer functions
# ---------------------------------------------------------
class test_required(unittest.TestCase):
    def test_required_is_true_value_supplied(self):
        arg = "--foo"
        from_cli = "1"
        from_template = True
        gold = "1"
        output = required(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_required_is_false_value_supplied(self):
        arg = "--foo"
        from_cli = "1"
        from_template = False
        gold = "1"
        output = required(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_required_is_true_value_not_supplied(self):
        arg = "--foo"
        from_cli = None
        from_template = True
        with self.assertRaises(ValidationException):
            required(arg, from_cli, from_template)

    def test_required_is_false_value_not_supplied(self):
        arg = "--foo"
        from_cli = None
        from_template = False
        gold = None
        output = required(arg, from_cli, from_template)
        self.assertEqual(gold, output)


class test_arg_type(unittest.TestCase):
    def test_no_given_value(self):
        arg = "--foo"
        from_cli = None
        from_template = int
        gold = None
        output = arg_type(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_arg_type_converts(self):
        arg = "--foo"
        from_cli = "1"
        from_template = int
        gold = 1
        output = arg_type(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_arg_type_fails_to_convert(self):
        arg = "--foo"
        from_cli = "hi"
        from_template = int
        with self.assertRaises(ValidationException):
            arg_type(arg, from_cli, from_template)


class test_choice(unittest.TestCase):
    def test_no_given_value(self):
        arg = "--foo"
        from_cli = None
        from_template = [1, 2]
        gold = None
        output = choice(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_given_is_allowed(self):
        arg = "--foo"
        from_cli = 1
        from_template = [1, 2]
        gold = 1
        output = choice(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_given_is_not_allowed(self):
        arg = "--foo"
        from_cli = 3
        from_template = [1, 2]
        with self.assertRaises(ValidationException):
            choice(arg, from_cli, from_template)


class test_default(unittest.TestCase):
    def test_no_given_value(self):
        arg = "--foo"
        from_cli = None
        from_template = 1
        gold = 1
        output = default(arg, from_cli, from_template)
        self.assertEqual(gold, output)

    def test_given_value(self):
        arg = "--foo"
        from_cli = 2
        from_template = 1
        gold = 2
        output = default(arg, from_cli, from_template)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
