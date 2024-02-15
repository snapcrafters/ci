# snapcrafters/ci/setup-tests

Deploys the snap from the specified channel, ready for tests to run.

## Usage

```yaml
# ...
jobs:
  test:
    name: 🗒️ Test snap
    needs: call-for-testing
    runs-on: ubuntu-latest
    steps:
      - name: 💾 Setup tests
        uses: snapcrafters/ci/setup-tests@main
        with:
          issue-number: ${{ needs.call-for-testing.outputs.issue-number }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
      - name: Run tests
        id: tests
        run: |
          # Your tests here. Write the results to $GITHUB_OUTPUT with the variable name status
          if true; then
            echo "status=success" >> $GITHUB_OUTPUT
          else
            echo "status=failed with exit code $?" >> $GITHUB_OUTPUT
      - name: 🗒️ Log test results
        uses: snapcrafters/ci/log-test-results@main
        with:
          issue-number: ${{ needs.call-for-testing.outputs.issue-number }}
          test-status: ${{ steps.tests.outputs.status }}

```

## API

### Inputs

| Key                      | Description                                                                                                                       | Required | Default                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | :------: | :---------------------------- |
| `issue-number`           | The issue number to post the screenshots to.                                                                                      |    Y     |                               |
| `channel`                | The channel to create the call for testing for.                                                                                   |    N     | `latest/candidate`            |
| `github-token`           | A token with permissions to common on issues in the repository.                                                                   |    Y     |                               |
| `snapcraft-project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. Do not include the trailing `/`. |    N     |                               |
