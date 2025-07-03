import unittest
from solution import strict


class TestStrictDecorator(unittest.TestCase):
    def test_valid_types(self):
        @strict
        def sum_two(a: int, b: float) -> float:
            return a + b

        result = sum_two(1, 2.0)
        self.assertEqual(result, 3.0, "Expected sum_two(1, 2.0) to return 3.0")

    def test_invalid_type_raises_typeerror(self):
        @strict
        def sum_two(a: int, b: float) -> float:
            return a + float(b)

        with self.assertRaises(TypeError) as context:
            sum_two(1, "2")
        self.assertEqual(
            str(context.exception),
            "Argument 'b' must be float, got str",
            "Expected TypeError with correct message for invalid type"
        )

    def test_keyword_arguments(self):
        @strict
        def sum_two(a: int, b: int) -> float:
            return a + b

        result = sum_two(a=1, b=2)
        self.assertEqual(result, 3.0, "Expected sum_two with keyword args to return 3.0")

    def test_default_arguments(self):
        @strict
        def sum_two(a: int, b: int = 0) -> float:
            return a + b

        result = sum_two(1)
        self.assertEqual(result, 1.0, "Expected sum_two(1) with defaults to return 1.0")

    def test_no_annotations(self):
        @strict
        def no_annotations(a, b):
            return a + b

        result = no_annotations(1, 2)
        self.assertEqual(result, 3, "Expected no_annotations(1, 2) to return 3")

    def test_mixed_types(self):
        class MyStr(str):
            pass

        @strict
        def mixed(a: int, b: str, c: float, d: bool, e: MyStr) -> float:
            return a + float(b) + c + int(d) + float(e)

        result = mixed(1, "2", 3.0, True, MyStr("5.0"))
        self.assertEqual(result, 12.0, "Expected mixed(1, '2', 3.0, True) to return 12.0")

        with self.assertRaises(TypeError) as context:
            mixed(1, 2, 3.0, True, MyStr("5.0"))
        self.assertEqual(
            str(context.exception),
            "Argument 'b' must be str, got int",
            "Expected TypeError for invalid type in mixed function"
        )

        with self.assertRaises(TypeError) as context:
            mixed(1, "2", 3.0, True, 5.0)
        self.assertEqual(
            str(context.exception),
            "Argument 'e' must be MyStr, got float",
            "Expected TypeError for invalid type in mixed function"
        )

    def test_strict_type_checking(self):
        class MyInt(int):
            pass

        @strict
        def strict_int(a: int) -> int:
            return a

        result = strict_int(42)
        self.assertEqual(result, 42, "Expected strict_int(42) to return 42")

        with self.assertRaises(TypeError) as context:
            strict_int(MyInt(42))
        self.assertIsInstance(
            MyInt(42), int,
            "Always true"
        )
        self.assertEqual(
            str(context.exception),
            "Argument 'a' must be int, got MyInt",
            "Expected TypeError for subclass type MyInt"
        )

        with self.assertRaises(TypeError) as context:
            strict_int(True)
        self.assertIsInstance(
            True, int,
            "Always true"
        )
        self.assertEqual(
            str(context.exception),
            "Argument 'a' must be int, got bool",
            "Expected TypeError for subclass type bool"
        )

    if __name__ == '__main__':
        unittest.main()
