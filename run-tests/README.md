# snapcrafters/ci/run-tests

Runs tests on a snap deployed from a specified channel and logs the result to the provided issue. If the given test command writes any markdown to the file in the environment variable `$GITHUB_STEP_SUMMARY`, that will be included in the resulting comment. See [the GitHub workflows documentation](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary) for more info.

## Usage

```yaml
# ...
jobs:
  test:
    name: 🗒️ Test snap
    needs: call-for-testing
    runs-on: ubuntu-latest
    steps:
      - name: 🗒️ Run tests
        uses: snapcrafters/ci/run-tests@main
        with:
          issue-number: ${{ needs.call-for-testing.outputs.issue-number }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          test-command: ./test.sh
```

## API

### Inputs

| Key                      | Description                                                                                                                       | Required | Default            |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | :------: | :----------------- |
| `issue-number`           | The issue number to post the result to.                                                                                           |    Y     |                    |
| `channel`                | The channel to create the call for testing for.                                                                                   |    N     | `latest/candidate` |
| `github-token`           | A token with permissions to common on issues in the repository.                                                                   |    Y     |                    |
| `snapcraft-project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. Do not include the trailing `/`. |    N     |                    |
| `test-script`            | The script containing the tests.                                                                                                  |    Y     |                    |
