# Snapcrafters CI

This repository contains common actions and tools used throughout the Snapcrafters
[organisation](https://github.com/snapcrafters) for the testing and delivery of our snaps.

## Snapcrafters Actions

The actions in this repo are all used during the build, test and release of our snaps. Each of them
listed below has it's own README

- [snapcrafters/ci/call-for-testing](call-for-testing/README.md)
- [snapcrafters/ci/get-architectures](get-architectures/README.md)
- [snapcrafters/ci/get-screenshots](get-screenshots/README.md)
- [snapcrafters/ci/promote-to-stable](promote-to-stable/README.md)
- [snapcrafters/ci/release-to-candidate](release-to-candidate/README.md)
- [snapcrafters/ci/sync-version](sync-version/README.md)
- [snapcrafters/ci/test-snap-build](test-snap-build/README.md)

### Usage

You can see examples of these actions in use in the following repos:

- [signal-desktop](https://github.com/snapcrafters/signal-desktop/main/.github/workflows)
- [mattermost-desktop](https://github.com/snapcrafters/mattermost-desktop/main/.github/workflows)
- [discord](https://github.com/snapcrafters/discord/main/.github/workflows)
