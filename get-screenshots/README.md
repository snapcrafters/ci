# snapcrafters/ci/get-screenshots

Deploys the snap from `latest/candidate` in a LXD desktop VM, then takes screenshots of the whole
desktop, and the most recent active window after the snap was launched. Screenshots are then
committed to [ci-screenshots](https://github.com/snapcrafters/ci-screenshots), and added to a comment on
the original call for testing issue.

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

| Key                 | Description                                                                                                        | Required | Default                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | :------: | :---------------------------- |
| `issue-number`      | The issue number to post the screenshots to.                                                                       |    Y     |                               |
| `ci-repo`           | The repo to fetch tools/templates from. Only for debugging.                                                        |    N     | `snapcrafters/ci`             |
| `channel`           | The channel to create the call for testing for.                                                                    |    N     | `candidate`                   |
| `github-token`      | A token with permissions to common on issues in the repository.                                                    |    Y     |                               |
| `screenshots-repo`  | The repository where screenshots should be uploaded.                                                               |    N     | `snapcrafters/ci-screenshots` |
| `screesnhots-token` | A token with permissions to commit screenshots to [ci-screenshots](https://github.com/snapcrafters/ci-screenshots) |    Y     |                               |

### Outputs

| Key      | Description                                                   | Example |
| -------- | ------------------------------------------------------------- | ------- |
| `screen` | A URL pointing to a screenshot of the whole screen in the VM  | `12`    |
| `window` | A URL pointing to a screenshot of the active window in the VM | `12`    |
