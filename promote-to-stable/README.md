# snapcrafters/ci/promote-to-stable

Promote to stable is generally triggered in response to a Snapcrafters reviewer posting a comment
containing a `/promote` command. Once the arguments are successfully parsed, the specified
revisions are promoted to `latest/stable`

## Usage

```yaml
# ...
jobs:
  promote:
    name: ⬆️ Promote to stable
    runs-on: ubuntu-latest
    steps:
      - name: ⬆️ Promote to stable
        uses: snapcrafters/ci/promote-to-stable@main
        with:
          store-token: ${{ secrets.SNAP_STORE_STABLE }}
```

## API

### Inputs

| Key            | Description                                                                              | Required | Default |
| -------------- | ---------------------------------------------------------------------------------------- | :------: | :------ |
| `github-token` | A token with permissions to write issues on the repository                               |    Y     |         |
| `store-token`  | A token with permissions to upload and release to the `stable` channel in the Snap Store |    Y     |         |

### Outputs

None
