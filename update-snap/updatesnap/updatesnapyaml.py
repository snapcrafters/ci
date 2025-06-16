#!/usr/bin/env python3

""" Analizes a YAML file and outputs  """

import sys
import argparse
import logging
import re
from SnapModule.snapmodule import Snapcraft, Github
from SnapModule.manageYAML import ManageYAML
from SnapVersionModule.snap_version_module import is_version_update, is_rock_version_update
UPDATE_BRANCH = 'update_versions'


class ProjectManager:
    """ This class is the one that searches in a remote project for
        the corresponding snapcraft.yaml file """
    def __init__(self, user=None, token=None, verbose=False):
        """ Constructor. """
        self._github = Github(not verbose)
        if user:
            self._github.set_secret('user', user)
        if token:
            self._github.set_secret('token', token)

    def get_working_branch(self, project_url):
        """ Returns the main branch of the project """

        branches = self._github.get_branches(project_url)
        working_branch = 'master'
        for branch in branches:
            if branch['name'] == UPDATE_BRANCH:
                working_branch = UPDATE_BRANCH
                break
            # give priority to 'main' over 'master'
            if branch['name'] == 'main':
                working_branch = 'main'
            # give priority to 'stable' over any other
            if branch['name'] == 'stable':
                working_branch = 'stable'
                break
        return working_branch

    def get_yaml_file(self, project_url, yaml_path):
        """ Searches in a project for the 'snapcraft.yaml' file and
            returns its contents """
        if yaml_path is not None:
            try:
                data = self._github.get_file(project_url, yaml_path)
            except (ValueError, ConnectionError):
                data = None
            return data

        yaml_path = 'snapcraft.yaml'
        try:
            data = self._github.get_file(project_url, yaml_path)
        except (ValueError, ConnectionError):
            data = None
        if not data:
            yaml_path = 'snap/snapcraft.yaml'
            try:
                data = self._github.get_file(project_url, yaml_path)
            except (ValueError, ConnectionError):
                data = None
        return data

    def get_readme_file(self, project_url, readme_path):
        """ Searches in a project for the 'README' file and
            returns its contents """
        try:
            data = self._github.get_file(project_url, readme_path)
        except (ValueError, ConnectionError):
            data = None
        return data

    def update_readme(self, project_url, parts, readme_path):
        """
        Updates the <!-- Begin Included Components --> to <!-- End Included Components -->
          sections in the README with the updated part list.
        """
        if readme_path is None:
            return

        readme_data = self.get_readme_file(project_url, readme_path)
        if not readme_data:
            print('Failed to get the README file.', file=sys.stderr)
            sys.exit(1)
        readme_content = readme_data.decode('utf-8')

        if (
            "<!-- Begin Included Components -->\n" not in readme_content
            or "<!-- End Included Components -->" not in readme_content
        ):
            print("The required markers are missing in the README file.", file=sys.stderr)
            return

        parts_contents = "\n".join([
            f"  - {part['name']} "
            f"{part['updates'][0]['name'] if part['updates'] else part['version'][0]}"
            for part in parts if part
        ])
        formatted_contents = f"## Included Components\n{parts_contents}"
        updated_readme = re.sub(
            r"<!-- Begin Included Components -->\n.*?\n<!-- End Included Components -->",
            f"<!-- Begin Included Components -->\n"
            f"{formatted_contents}\n"
            f"<!-- End Included Components -->",
            readme_content,
            flags=re.DOTALL
        )

        if updated_readme != readme_content:
            print("Updating README file", file=sys.stderr)
            with open('readme_output', 'w', encoding="utf8") as readme_output_file:
                readme_output_file.write(updated_readme)
        else:
            print("No updates available for README file", file=sys.stderr)


def parse_args():
    """ Parses command-line arguments for the script. """
    parser = argparse.ArgumentParser(prog='Update Snap YAML',
                                     description='Find the lastest source'
                                     ' versions for snap files and generates a new snapcraft.yaml.')
    parser.add_argument('--github-user', action='store', default=None,
                        help='User name for accessing Github projects.')
    parser.add_argument('--github-token', action='store', default=None,
                        help='Access token for accessing Github projects.')
    parser.add_argument('--version-schema', action='store', default=None,
                        help='Version schema of snapping repository')
    parser.add_argument('--rock-version-schema', action='store', default=None,
                        help='Version schema of rock repository')
    parser.add_argument('--yaml-path', action='store', default=None,
                        help='Path to the yaml file')
    parser.add_argument('--readme-path', action='store', default=None,
                        help='Path to the README.md file where the parts'
                        'and their version will be listed.')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('project', default='.', help='The project URI')

    return parser.parse_args(sys.argv[1:])


def main():
    """ Main code """
    arguments = parse_args()

    if arguments.project == '.':
        print('A project URI is mandatory', file=sys.stderr)
        sys.exit(-1)

    manager = ProjectManager(arguments.github_user, arguments.github_token, arguments.verbose)

    # get the most-updated SNAPCRAFT.YAML file

    data = manager.get_yaml_file(arguments.project, arguments.yaml_path)
    if not data:
        print('Failed to get the snapcraft.yaml file.', file=sys.stderr)
        sys.exit(-1)
    contents = data.decode('utf-8')

    manager_yaml = ManageYAML(contents)

    snap = Snapcraft(not arguments.verbose)
    snap.load_external_data(contents)
    if arguments.github_user:
        snap.set_secret('github', 'user', arguments.github_user)
    if arguments.github_token:
        snap.set_secret('github', 'token', arguments.github_token)
    parts, tag_error = snap.process_parts()

    if tag_error:
        sys.exit(1)

    if len(parts) == 0:
        print("The snapcraft.yaml file has no parts.", file=sys.stderr)
        sys.exit(0)  # no parts

    has_update = False
    for part in parts:
        if not part:
            continue
        if not part['updates']:
            continue
        version_data = manager_yaml.get_part_element(part['name'], 'source-tag:')
        if not version_data:
            continue
        print(f"Updating '{part['name']}' from version '{part['version'][0]}'"
              f" to version '{part['updates'][0]['name']}'", file=sys.stderr)
        version_data['data'] = f"source-tag: '{part['updates'][0]['name']}'"
        has_update = True

    manager.update_readme(arguments.project, parts, arguments.readme_path)

    logging.basicConfig(level=logging.INFO)
    if (is_version_update(snap, manager_yaml, arguments, has_update) or
            is_rock_version_update(snap, manager_yaml, arguments, has_update) or has_update):
        with open('output_file', 'w', encoding="utf8") as output_file:
            output_file.write(manager_yaml.get_yaml())
    else:
        print("No updates available", file=sys.stderr)


if __name__ == "__main__":
    main()
