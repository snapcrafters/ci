# snapcrafters/ci/call-for-testing

Automatically creates a templated call for testing as a Github issue, containing the details of
newly released revisions and instructions on how to test and promote them.

## Usage

### Use in combination with `snapcrafters/ci/release-to-candidate`

In this mode, the action will look for an artifact uploaded by the
`snapcrafters/ci/release-to-candidate` action that contains a manifest detailing the exact
revisions that were uploaded, and use those to populate the call for testing template.

```yaml
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

  call-for-testing:
    name: 📣 Create call for testing
    needs: release
    runs-on: ubuntu-latest
    steps:
      - name: 📣 Create call for testing
        uses: snapcrafters/ci/call-for-testing@main
        with:
          architectures: "amd64 arm64"
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Use standalone - `store-token` required

In this mode, the action will use the store token to fetch the latest revision on the specified
channel (`latest/candidate` by default) for each architecture and populate the call for testing with those
revisions.

```yaml
jobs:
  call-for-testing:
    name: 📣 Create call for testing
    runs-on: ubuntu-latest
    steps:
      - name: 📣 Create call for testing
        uses: snapcrafters/ci/call-for-testing@main
        with:
          architectures: "amd64 arm64"
          github-token: ${{ secrets.GITHUB_TOKEN }}
          store-token: ${{ secrets.STORE_TOKEN }}
```

## API

### Inputs

| Key                      | Description                                                                                                                                                                              | Required | Default                                                                                              |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------: | :--------------------------------------------------------------------------------------------------- |
| `architectures`          | The architectures that the snap supports.                                                                                                                                                |    Y     |                                                                                                      |
| `ci-repo`                | The repo to fetch tools/templates from. Only for debugging.                                                                                                                              |    N     | `snapcrafters/ci`                                                                                    |
| `channel`                | The channel to create the call for testing for.                                                                                                                                          |    N     | `latest/candidate`                                                                                   |
| `github-token`           | A token with permissions to create issues on the repository.                                                                                                                             |    Y     |                                                                                                      |
| `promotion-channel`      | The channel the snap should be promoted to on successful test.                                                                                                                           |    N     | `latest/stable`                                                                                      |
| `snapcraft-channel`      | The channel to install Snapcraft from.                                                                                                                                                   |    N     | `latest/stable`                                                                                      |
| `snapcraft-project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. Do not include the trailing `/`.                                                        |    N     |
| `store-token`            | A token with permissions to query the specified channel in the Snap Store. Only required if the revisions to test are not passed to the workflow by the `release-to-candidate` workflow. |    N     |                                                                                                      |
| `testing-instructions`   | Custom testing instructions for testing the `candidate` snap.                                                                                                                            |    N     | See [action.yaml](https://github.com/snapcrafters/ci/blob/main/call-for-testing/action.yaml#L40-L52) |

### Outputs

| Key            | Description                                       | Example |
| -------------- | ------------------------------------------------- | ------- |
| `issue-number` | The issue number containing the call for testing. | `12`    |
