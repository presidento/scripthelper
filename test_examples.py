import unittest
import subprocess
import pathlib
import textwrap


class TestExamples(unittest.TestCase):
    def assert_output(self, command, expected, subprocess_check=True):
        result = subprocess.run(
            f"python {command}",
            stdout=subprocess.PIPE,
            check=subprocess_check,
            shell=True,
        )
        output = result.stdout.decode().replace("\r", "")
        self.assertEqual(output.strip(), expected.strip())

    def test_example1_without_arguments(self):
        self.assert_output(
            "example1.py",
            textwrap.dedent(
                """
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                INFO info message
                """
            ),
        )

    def test_example1_help(self):
        self.assert_output(
            "example1.py -h",
            textwrap.dedent(
                """
                usage: example1.py [-h] [-v] [-q] [--colors] [--no-colors]

                optional arguments:
                  -h, --help     show this help message and exit
                  -v, --verbose  Increase verbosity. Can be applied multiple times, like -vv
                  -q, --quiet    Decrease verbosity. Can be applied multiple times, like -qq
                  --colors       Force set colored output
                  --no-colors    Force set no-colored output
                """
            ),
        )

    def test_example1_with_1_quiet(self):
        self.assert_output(
            "example1.py -q",
            textwrap.dedent(
                """
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                """
            ),
        )

    def test_example1_with_2_quiet(self):
        self.assert_output(
            "example1.py -qq",
            textwrap.dedent(
                """
                CRITICAL critical message
                ERROR error message
                """
            ),
        )

    def test_example1_with_2_long_quiet(self):
        self.assert_output(
            "example1.py --quiet --quiet",
            textwrap.dedent(
                """
                CRITICAL critical message
                ERROR error message
                """
            ),
        )

    def test_example1_with_1_verbose(self):
        self.assert_output(
            "example1.py -v",
            textwrap.dedent(
                """
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                INFO info message
                VERBOSE verbose message
                """
            ),
        )

    def test_example1_with_2_verbose(self):
        self.assert_output(
            "example1.py -vv",
            textwrap.dedent(
                """
                DEBUG Arguments: Namespace(colors=None, quiet=None, verbose=2)
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                INFO info message
                VERBOSE verbose message
                DEBUG debug message
                """
            ),
        )

    def test_example1_with_3_verbose(self):
        self.assert_output(
            "example1.py -vvv",
            textwrap.dedent(
                """
                DEBUG Arguments: Namespace(colors=None, quiet=None, verbose=3)
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                INFO info message
                VERBOSE verbose message
                DEBUG debug message
                SPAM spam message
                """
            ),
        )

    def test_example1_with_3_long_verbose(self):
        self.assert_output(
            "example1.py --verbose --verbose --verbose",
            textwrap.dedent(
                """
                DEBUG Arguments: Namespace(colors=None, quiet=None, verbose=3)
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                INFO info message
                VERBOSE verbose message
                DEBUG debug message
                SPAM spam message
                """
            ),
        )

    def test_example2_without_arguments(self):
        self.assert_output("example2.py", "WARNING Name was not provided")

    def test_example2_with_name_provided(self):
        self.assert_output("example2.py --name World", "INFO Hello World")

    @unittest.skip(
        "Example3 demonstrates the progressbar, it should be checked manually."
    )
    def test_example3(self):
        pass

    def test_example4(self):
        self.assert_output("example4.py", "INFO Hello from a module.")

    def test_example5(self):
        log_file = pathlib.Path("example5.log")
        log_file.unlink(missing_ok=True)
        try:
            subprocess.run(f"python example5.py >NUL", shell=True)
            log_content = log_file.read_text().strip()
        finally:
            log_file.unlink(missing_ok=True)
        dates_removed = "\n".join([line[20:] for line in log_content.splitlines()])
        self.assertEqual(
            dates_removed,
            textwrap.dedent(
                """
                CRITICAL critical message
                ERROR error message
                WARNING warning message
                INFO info message
                """
            ).strip(),
        )

    def test_example6(self):
        self.assert_output(
            "example6.py",
            textwrap.dedent(
                """
                WARNING example6.py:14: UserWarning: This user warning will be captured.
                  warnings.warn("This user warning will be captured.")

                CRITICAL Uncaught RuntimeError: This exception should be handled.
                Traceback with variables (most recent call last):
                  File "example6.py", line 11, in uncaught_exception_test
                    raise RuntimeError("This exception should be handled.")
                      this_variable = 'will be displayed in stack trace'
                      as_well_as = 'the other variables'
                builtins.RuntimeError: This exception should be handled.
                """
            ),
            subprocess_check=False,
        )


    def test_example7(self):
        self.assert_output(
            "example7.py",
            textwrap.dedent(
                """
                {
                    'string': 'value1',
                    'bool': True,
                    'none': None,
                    'integer': 1234,
                    'item': Item(name='name', value=999)
                }
                """
            ),
            subprocess_check=False,
        )


    def test_example8(self):
        self.assert_output(
            "example8.py --no-colors",
            textwrap.dedent(
                """
                INFO Testing --colors and --no-colors options
                [True, 'string', 1234]
                CRITICAL Uncaught Exception: Unhandled Exception
                Traceback with variables (most recent call last):
                builtins.Exception: Unhandled Exception
                """
            ),
            subprocess_check=False,
        )
        self.assert_output(
            "example8.py --colors",
            textwrap.dedent(
                """
                \x1b[34mINFO\x1b[0m Testing --colors and --no-colors options
                \x1b[0m\x1b[37m[\x1b[0m\x1b[0m\x1b[36mTrue\x1b[0m\x1b[0m\x1b[37m,\x1b[0m \x1b[0m\x1b[33m'\x1b[0m\x1b[33mstring\x1b[0m\x1b[33m'\x1b[0m\x1b[0m\x1b[37m,\x1b[0m \x1b[0m\x1b[37m1234\x1b[0m\x1b[0m\x1b[37m]\x1b[0m
                \x1b[34mCRITICAL\x1b[0m \x1b[1;31mUncaught Exception: Unhandled Exception\x1b[0m
                \x1b[36mTraceback with variables (most recent call last):\x1b[0m
                \x1b[31mbuiltins.Exception:\x1b[0m\x1b[91m Unhandled Exception\x1b[0m
                """
            ),
            subprocess_check=False,
        )


if __name__ == "__main__":
    unittest.main()
