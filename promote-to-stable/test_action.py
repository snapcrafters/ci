"""Run with: uv run --with pyyaml python -m unittest discover -s promote-to-stable -v."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


STEPS = yaml.safe_load(Path(__file__).with_name("action.yaml").read_text())["runs"]["steps"]
COMMAND = next(step for step in STEPS if step.get("id") == "command")
PROMOTE = next(step for step in STEPS if step.get("id") == "promote")


class PromotionTests(unittest.TestCase):
    def command(self, body="/promote 123 latest/stable done", permission="write",
                event="issue_comment", action="created"):
        self.assertEqual(COMMAND["uses"], "actions/github-script@v8")
        fixture = json.dumps(dict(body=body, permission=permission, event=event, action=action))
        harness = """
const fixture = JSON.parse(process.argv[1]);
const result = { outputs: {}, permissions: [], reactions: [] };
const context = {
  eventName: fixture.event, actor: 'maintainer', repo: {owner: 'owner', repo: 'repo'},
  payload: {action: fixture.action, comment: {id: 42, body: fixture.body}},
};
const core = {
  setFailed: message => { result.failure = message; },
  setOutput: (key, value) => { result.outputs[key] = value; },
};
const github = {rest: {
  repos: {getCollaboratorPermissionLevel: async args => {
    result.permissions.push(args);
    return {data: {permission: fixture.permission}};
  }},
  reactions: {createForIssueComment: async args => { result.reactions.push(args); }},
}};
(async () => {
  await (async () => {
SCRIPT
  })();
  console.log(JSON.stringify(result));
})().catch(error => { console.error(error); process.exit(1); });
""".replace("SCRIPT", COMMAND["with"]["script"])
        process = subprocess.run(["node", "-e", harness, fixture], check=True,
                                 capture_output=True, text=True)
        return json.loads(process.stdout)

    def test_write_and_admin_can_promote(self):
        for permission in ("write", "admin"):
            with self.subTest(permission=permission):
                result = self.command(permission=permission)
                self.assertNotIn("failure", result)
                self.assertEqual(result["outputs"], {
                    "command-name": "promote", "command-arguments": "123 latest/stable done"})
                self.assertEqual(result["permissions"][0]["username"], "maintainer")
                self.assertEqual(result["reactions"][0]["content"], "eyes")
                self.assertEqual(result["reactions"][0]["comment_id"], 42)

    def test_rejects_other_events_edits_commands_and_permissions(self):
        cases = [dict(event="pull_request"), dict(action="edited"),
                 dict(body="/other 123"), dict(body="text /promote 123"),
                 dict(body="/promoter 123"), dict(body=""),
                 *[dict(permission=value) for value in ("read", "triage", "none")]]
        for case in cases:
            with self.subTest(case=case):
                result = self.command(**case)
                self.assertIn("failure", result)
                self.assertEqual(result["outputs"], {})
                self.assertEqual(result["reactions"], [])

    def test_multiline_comment_and_empty_arguments(self):
        result = self.command(body="Please release:\n/promote 123 latest/stable\nThanks")
        self.assertEqual(result["outputs"]["command-arguments"], "123 latest/stable")
        result = self.command(body="/promote")
        self.assertEqual(result["outputs"]["command-arguments"], "")

    def test_shell_treats_comment_as_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "snapcraft").write_text('#!/bin/bash\nprintf "%s\\n" "$*" >> "$releases"\n')
            (root / "snapcraft").chmod(0o755)
            for arguments, success in [
                ("123,456 latest/stable done", True),
                ("123 latest/stable", True),
                ("$(touch injected) latest/stable", False),
                ("123 latest/stable'; touch injected; #", False),
                ("123 latest/stable `touch injected`", False),
                ("* latest/stable", False),
                ("123 latest/candidate", False),
                ("", False),
            ]:
                with self.subTest(arguments=arguments):
                    (root / "injected").unlink(missing_ok=True)
                    script = PROMOTE["run"]
                    # Simulate GitHub's expression substitution for the old vulnerable script.
                    for key, value in {"command-name": "promote", "command-arguments": arguments}.items():
                        script = script.replace("${{ steps.command.outputs." + key + " }}", value)
                    env = dict(os.environ, command_name="promote", command_arguments=arguments,
                               channel="latest/stable", snap_name="example", valid_revisions="123 456",
                               GITHUB_OUTPUT=str(root / "output"), releases=str(root / "releases"),
                               PATH=str(root) + os.pathsep + os.environ["PATH"])
                    result = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
                                            cwd=root, env=env, capture_output=True, text=True)
                    self.assertFalse((root / "injected").exists(), "comment executed shell code")
                    self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
            self.assertEqual((root / "releases").read_text().splitlines(), [
                "release example 123 latest/stable", "release example 456 latest/stable",
                "release example 123 latest/stable"])


if __name__ == "__main__":
    unittest.main()
