# snapcrafters/ci/test

Deploys the snap from the specified channel and runs the specified test script.
Results are then linked in the call for testing issue.

## Usage

```yaml
# ...
jobs:
  screenshots:
    name: 📸 Gather screenshots
    needs: call-for-testing
    runs-on: ubuntu-latest
    steps:
      - name: 📸 Gather screenshots
        uses: snapcrafters/ci/get-screenshots@main
        with:
          issue-number: ${{ needs.call-for-testing.outputs.issue-number }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          screenshots-token: ${{ secrets.SCREENSHOT_COMMIT_TOKEN }}
```

## API

### Inputs

| Key                      | Description                                                                                                                       | Required | Default                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | :------: | :---------------------------- |
| `issue-number`           | The issue number to post the screenshots to.                                                                                      |    Y     |                               |
| `ci-repo`                | The repo to fetch tools/templates from. Only for debugging.                                                                       |    N     | `snapcrafters/ci`             |
| `channel`                | The channel to create the call for testing for.                                                                                   |    N     | `latest/candidate`            |
| `github-token`           | A token with permissions to common on issues in the repository.                                                                   |    Y     |                               |
| `snapcraft-project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. Do not include the trailing `/`. |    N     |                               |
| `test-script`            | The relative path to the test script for this snap, including `./` if it is in the root directory.                                |    Y     |                               |

### Outputs

| Key      | Description                      |
| -------- | ---------------------------------|
| `status` | Text of the outcome of the tests |
