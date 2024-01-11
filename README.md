# Snapcrafters CI

This repository contains common actions and tools used throughout the Snapcrafters [organisation](https://github.com/snapcrafters) for the testing and delivery of our snaps.

## Snapcrafters Actions

The actions in this repo are all used during the build, test and release of our snaps. Each of them listed below has it's own README

- [snapcrafters/ci/call-for-testing](call-for-testing/README.md)
- [snapcrafters/ci/get-architectures](get-architectures/README.md)
- [snapcrafters/ci/get-screenshots](get-screenshots/README.md)
- [snapcrafters/ci/parse-snapcraft-yaml](parse-snapcraft-yaml/README.md)
- [snapcrafters/ci/promote-to-stable](promote-to-stable/README.md)
- [snapcrafters/ci/release-to-candidate](release-to-candidate/README.md)
- [snapcrafters/ci/sync-version](sync-version/README.md)
- [snapcrafters/ci/test-snap-build](test-snap-build/README.md)

### Usage

You can see examples of these actions in use in the following repos:

- [signal-desktop](https://github.com/snapcrafters/signal-desktop/tree/candidate/.github/workflows)
- [mattermost-desktop](https://github.com/snapcrafters/mattermost-desktop/tree/candidate/.github/workflows)
- [discord](https://github.com/snapcrafters/discord/tree/candidate/.github/workflows)

## Contributing

If you'd like to contribute to this repository, please feel free to fork and create a pull request.

There are a few style guidelines to keep in mind:

- Code should be linted using [Prettier](https://prettier.io/). You can achieve this with `make lint` and `make format`. The only requirements are [`npx`](https://www.npmjs.com/package/npx) and [`shellcheck`](https://github.com/koalaman/shellcheck).
- When defining inputs/outputs in `action.yaml`, or listing them in the tables within `README.md`, they should be listed in alphabetical order for easy reading and updating.
- Github Action inputs/outputs should be named all lowercase, separated by `-` where needed. The applies to inputs/outputs to actions themselves, and for individual steps within the actions. For example: `snap-name` or `token`.
- Environment variables referring to repository level secrets and variables should be named all uppercase, and separated by `_`. For example: `SNAPCRAFTERS_BOT_COMMIT`.
- Step/job level environment variables should be named all lowercase, and separated by `_`. For example: `snap_name` or `yaml_path`.
- All `bash` variables should be quoted.
- Scripts of all kinds, including those within actions `run:|` directives should follow the [Google styleguide](https://google.github.io/styleguide/shellguide.html)
