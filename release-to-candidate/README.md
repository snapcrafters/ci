# snapcrafters/ci/release-to-candidate

This action is used to run `snapcraft remote-build` for a given Snap, and a given architecture.
Following that, the snap is released to the `latest/candidate` automatically.

## Usage

```yaml
# ...
jobs:
  release:
    name: 🚢 Release to latest/candidate
    runs-on: ubuntu-latest
    steps:
      - name: 🚢 Release to latest/candidate
        uses: snapcrafters/ci/release-to-candidate@main
        with:
          architecture: arm64
          launchpad-token: ${{ secrets.LAUNCHPAD_TOKEN }}
          store-token: ${{ secrets.STORE_TOKEN }}
```

## API

### Inputs

| Key                      | Description                                                                               | Required | Default     |
| ------------------------ | ----------------------------------------------------------------------------------------- | :------: | :---------- |
| `architecture`           | The architecture for which to build the snap.                                             |    N     | `amd64`     |
| `channel`                | The channel to release the snap to.                                                       |    N     | `candidate` |
| `launchpad-token`        | A token with permissions to create Launchpad remote builds.                               |    Y     |             |
| `repo-token`             | A token with privileges to create and push tags to the repository.                        |    Y     |             |
| `snapcraft-project-root` | The path to the Snapcraft YAML file.                                                      |    N     |             |
| `store-token`            | A token with permissions to upload and release to the specified channel in the Snap Store |    Y     |             |

### Outputs

| Key        | Description                               | Example |
| ---------- | ----------------------------------------- | ------- |
| `revision` | The Snap Store revision that was created. | `15`    |
