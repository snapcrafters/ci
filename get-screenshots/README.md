# snapcrafters/ci/get-screenshots

Deploys the snap from the specified channel in a LXD desktop VM, then takes screenshots of the whole
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

| Key                      | Description                                                                                                                       | Required | Default                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | :------: | :---------------------------- |
| `bot-email`              | The email address of the bot account to use to commit screenshots.                                                                |    N     | `snapforge.team@gmail.com`    |
| `bot-name`               | The name of the bot account to use to commit screenshots.                                                                        |    N     | `Snapcrafters Bot`            |
| `issue-number`           | The issue number to post the screenshots to.                                                                                      |    Y     |                               |
| `ci-repo`                | The repo to fetch tools/templates from. Only for debugging.                                                                       |    N     | `snapcrafters/ci`             |
| `channel`                | The channel to create the call for testing for.                                                                                   |    N     | `latest/candidate`            |
| `github-token`           | A token with permissions to common on issues in the repository.                                                                   |    Y     |                               |
| `screenshots-repo`       | The repository where screenshots should be uploaded.                                                                              |    N     | `snapcrafters/ci-screenshots` |
| `screenshots-token`      | A token with permissions to commit screenshots to [ci-screenshots](https://github.com/snapcrafters/ci-screenshots)                |    Y     |                               |
| `snap-application-name`  | The name of the application defined in `snapcraft.yaml` to run for screenshots.                                                   |    N     |                               |
| `snapcraft-project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. Do not include the trailing `/`. |    N     |

### Outputs

| Key      | Description                                                   |
| -------- | ------------------------------------------------------------- |
| `screen` | A URL pointing to a screenshot of the whole screen in the VM  |
| `window` | A URL pointing to a screenshot of the active window in the VM |
