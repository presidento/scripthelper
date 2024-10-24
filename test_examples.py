import unittest
import subprocess
import pathlib
import textwrap
import os
import sys


class TestExamples(unittest.TestCase):
    def assert_output(self, command, expected, subprocess_check=True):
        output = self.run_command(command, subprocess_check)
        self.assertEqual(expected.strip(), output.strip())

    def run_command(self, command, subprocess_check=True):
        # Workaround for bug with Nushell, see https://github.com/python/cpython/issues/102496
        sys_executable = str(pathlib.Path(sys.executable).absolute()).replace(
            "\\\\?\\", ""
        )
        result = subprocess.run(
            f'"{sys_executable}" {command}',
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=subprocess_check,
            shell=True,
            cwd=pathlib.Path(__file__).absolute().parent,
        )
        # There should be nothing on non-tty stderr.
        # (The progressbar is on stderr, but only for tty stderr)
        self.assertFalse(result.stderr.decode())
        output = result.stdout.decode().replace("\r", "")
        abs_path_dir = str(pathlib.Path(".").absolute()) + os.sep
        output = output.replace(abs_path_dir, "")
        return output

    def test_example1_without_arguments(self):
        self.assert_output(
            "example1.py",
            textwrap.dedent(
                """
                CRITICAL example1 critical message
                ERROR example1 error message
                WARNING example1 warning message
                INFO example1 info message
                """
            ),
        )

    def test_example1_help(self):
        output = self.run_command("example1.py -h")
        args_help = textwrap.dedent(
            """
            -h, --help
            show this help message and exit
            -v, --verbose
            Increase verbosity.
            -q, --quiet
            Decrease verbosity.
            --colors
            Force set colored output
            --no-colors
            Force set non-colored output
            --disable-traceback-variables
            Do not display variables in traceback context
            """
        )
        for arg_help in args_help.splitlines():
            assert arg_help in output, "Missing line: " + arg_help

    def test_example1_with_1_quiet(self):
        self.assert_output(
            "example1.py -q",
            textwrap.dedent(
                """
                CRITICAL example1 critical message
                ERROR example1 error message
                WARNING example1 warning message
                """
            ),
        )

    def test_example1_with_2_quiet(self):
        self.assert_output(
            "example1.py -qq",
            textwrap.dedent(
                """
                CRITICAL example1 critical message
                ERROR example1 error message
                """
            ),
        )

    def test_example1_with_2_long_quiet(self):
        self.assert_output(
            "example1.py --quiet --quiet",
            textwrap.dedent(
                """
                CRITICAL example1 critical message
                ERROR example1 error message
                """
            ),
        )

    def test_example1_with_1_verbose(self):
        self.assert_output(
            "example1.py -v",
            textwrap.dedent(
                """
                CRITICAL example1 critical message
                ERROR example1 error message
                WARNING example1 warning message
                INFO example1 info message
                VERBOSE example1 verbose message
                """
            ),
        )

    def test_example1_with_2_verbose(self):
        expected = textwrap.dedent(
            """
            DEBUG example1 Arguments: Namespace(verbose=2, quiet=None, colors=None, disable_traceback_variables=False)
            CRITICAL example1 critical message
            ERROR example1 error message
            WARNING example1 warning message
            INFO example1 info message
            VERBOSE example1 verbose message
            DEBUG example1 debug message
            """
        ).strip()
        self.assert_output("example1.py -vv", expected)

    def test_example1_with_3_verbose(self):
        expected = textwrap.dedent(
            """
            DEBUG example1 Arguments: Namespace(verbose=3, quiet=None, colors=None, disable_traceback_variables=False)
            CRITICAL example1 critical message
            ERROR example1 error message
            WARNING example1 warning message
            INFO example1 info message
            VERBOSE example1 verbose message
            DEBUG example1 debug message
            SPAM example1 spam message
            """
        ).strip()
        self.assert_output("example1.py -vvv", expected)

    def test_example1_with_3_long_verbose(self):
        expected = textwrap.dedent(
            """
            DEBUG example1 Arguments: Namespace(verbose=3, quiet=None, colors=None, disable_traceback_variables=False)
            CRITICAL example1 critical message
            ERROR example1 error message
            WARNING example1 warning message
            INFO example1 info message
            VERBOSE example1 verbose message
            DEBUG example1 debug message
            SPAM example1 spam message
            """
        ).strip()
        self.assert_output("example1.py --verbose --verbose --verbose", expected)

    def test_example2_without_arguments(self):
        self.assert_output("example2.py", "WARNING example2 Name was not provided")

    def test_example2_with_name_provided(self):
        self.assert_output("example2.py --name World", "INFO example2 Hello World")

    def test_example2b_with_name_provided(self):
        self.assert_output("example2b.py --name Nation", "INFO example2b Hello Nation")

    def test_example3(self):
        self.assert_output(
            "example3.py -v",
            textwrap.dedent(
                """
                INFO example3 Doing the calculations...
                VERBOSE example3 Iteration 0
                VERBOSE example3 Iteration 20
                VERBOSE example3 Iteration 40
                VERBOSE example3 Iteration 60
                VERBOSE example3 Iteration 80
                INFO example3 Done
                """
            ),
        )

    def test_example4(self):
        self.assert_output("example4.py", "INFO example4module Hello from a module.")

    def test_example5(self):
        log_file = pathlib.Path("example5.log")
        if log_file.is_file():
            log_file.unlink()
        try:
            # Workaround for bug with Nushell, see https://github.com/python/cpython/issues/102496
            sys_executable = str(pathlib.Path(sys.executable).absolute()).replace(
                "\\\\?\\", ""
            )
            subprocess.run(
                f'"{sys_executable}" example5.py >NUL', shell=True, check=True
            )
            log_content = log_file.read_text().strip()
        finally:
            if log_file.is_file():
                log_file.unlink()
        dates_removed = "\n".join([line[20:] for line in log_content.splitlines()])
        self.assertEqual(
            dates_removed,
            textwrap.dedent(
                """
                CRITICAL example5 critical message
                ERROR example5 error message
                WARNING example5 warning message
                INFO example5 info message
                """
            ).strip(),
        )

    def test_example6(self):
        variable_lines = [
            "this_variable = 'will be displayed in stack trace'",
            "as_well_as = 'the other variables'",
        ]
        warning_str = "This user warning will be captured."

        output = self.run_command("example6.py --no-colors", subprocess_check=False)
        assert warning_str in output
        for variable_line in variable_lines:
            assert variable_line in output, f"Missing: {variable_line}"

        output = self.run_command(
            "example6.py --no-colors --disable-traceback-variables",
            subprocess_check=False,
        )
        assert warning_str in output
        for variable_line in variable_lines:
            assert variable_line not in output, f"Displayed: {variable_line}"

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
        with_colors = self.run_command("example8.py --colors", subprocess_check=False)
        assert "\x1b[0m" in with_colors
        no_colors = self.run_command("example8.py --no-colors", subprocess_check=False)
        assert "\x1b[0m" not in no_colors

    def test_example9(self):
        pathlib.Path("example9.state").unlink(missing_ok=True)
        self.assert_output(
            "example9.py",
            textwrap.dedent(
                """
                INFO example9 Processing item #1
                INFO example9 - Element 1
                """
            ),
        )
        self.assert_output(
            "example9.py",
            textwrap.dedent(
                """
                INFO example9 Processing item #2
                INFO example9 - Element 1
                INFO example9 - Element 2
                """
            ),
        )
        self.assert_output(
            "example9.py",
            textwrap.dedent(
                """
                INFO example9 Processing item #3
                INFO example9 - Element 2
                INFO example9 - Element 3
                """
            ),
        )

    def test_example10(self):
        self.assert_output("example10.py", "WARNING example10 Item #12 has some errors")


if __name__ == "__main__":
    unittest.main()
