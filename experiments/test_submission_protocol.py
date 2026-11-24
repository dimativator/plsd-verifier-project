"""Offline literal Bash submission parsing; no commands or credentials are used."""
import unittest

from experiments.submission_protocol import (
    SUBMISSION_MARKER as MARKER, is_submission_action, non_submission_notice,
)


class SubmissionActionTests(unittest.TestCase):
    def test_allowed_literal_forms(self):
        commands = [
            f"echo {MARKER}",
            f"cd /work && echo {MARKER}",
            f'  "cd" \'/work\' && \'echo\' "{MARKER}" ;  ',
            f"\n\tcd /work &&\n\n echo '{MARKER}';\n\n",
            f"echo {MARKER};\r\n",
            f'e"ch"o {MARKER}',
            f"\\echo {MARKER}",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(is_submission_action(command))

    def test_write_check_and_additional_commands_are_never_submission(self):
        commands = [
            f"printf x > main.py; echo {MARKER}",
            f"echo {MARKER}; printf x > main.py",
            f"run_tests && echo {MARKER}",
            f"echo {MARKER} && run_tests",
            f"echo {MARKER}\nrun_tests",
            f"echo {MARKER}\npwd",
            f"echo\n{MARKER}",
            f"echo; {MARKER}",
            f"cd\n/work && echo {MARKER}",
            f"cd /work\n&& echo {MARKER}",
            f"cd /work; echo {MARKER}",
            f"cd /tmp && echo {MARKER}",
            f"env echo {MARKER}",
            f"command echo {MARKER}",
            f"echo {MARKER};;",
            f"echo {MARKER}\n;",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertFalse(is_submission_action(command))

    def test_expansion_redirects_pipes_and_nonliteral_operators_are_rejected(self):
        commands = [
            f"echo $(printf {MARKER})",
            f"echo `printf {MARKER}`",
            f"e$(printf cho) {MARKER}",
            f'echo "${{MARKER}}"',
            f"echo {MARKER} > output.txt",
            f"echo {MARKER} 2>/dev/null",
            f"echo {MARKER} | cat",
            f"echo {MARKER} &",
            f"echo {MARKER} || true",
            f'cd /work "&&" echo {MARKER}',
            f"cd /work '&'& echo {MARKER}",
            f"cd /work \\&\\& echo {MARKER}",
            f"echo {MARKER}\\;",
            f"echo\\\n {MARKER}",
            f"echo {MARKER} # trailing comment",
            f"echo '{MARKER}",
            f"echo \"{MARKER}",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertFalse(is_submission_action(command))

    def test_ordinary_and_commands_are_not_blocked_or_given_a_notice(self):
        command = "compile && run_tests"
        self.assertFalse(is_submission_action(command))
        self.assertEqual(non_submission_notice(command, "Public tests passed"), "")

    def test_marker_printed_in_combined_action_gets_actionable_notice(self):
        command = f"run_tests; echo {MARKER}"
        notice = non_submission_notice(command, f"tests passed\n{MARKER}\n")
        self.assertEqual(notice, f"not submitted, run echo {MARKER} to submit")

    def test_no_notice_for_allowed_submission_or_marker_mentioned_in_prose(self):
        self.assertEqual(non_submission_notice(f"cd /work && echo {MARKER}", MARKER), "")
        self.assertEqual(non_submission_notice("cat guide.txt", f"Submit with echo {MARKER}."), "")


if __name__ == "__main__":
    unittest.main()
