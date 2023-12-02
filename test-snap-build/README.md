# snapcrafters/ci/test-snap-build

Designed to be a quick "smoke test" that doesn't require any special credentials or secrets. This
action tries to build the snap "locally" on the Github Actions runner for `amd64` only. Once the
snap is built, it is reviewed using [review-tools].

Information about your snap will be automatically parsed for the review stage. If you need to
specify plug or slot declarations per the [snapcraft-review-tools] README, you can include any of
the following files in your repository, which will be passed to the review action:

- `slot-declaration.json`
- `.github/slot-declaration.json`
- `plug-declaration.json`
- `.github/plug-declaration.json`

> [!NOTE]
> We don't use `remote-build` here, because that requires access to a Launchpad token.
> Exposing tokens in a PR build can be [dangerous] from a security standpoint.

## Usage

```yaml
# ...
jobs:
  build:
    name: 🧪 Build snap on amd64
    runs-on: ubuntu-latest
    steps:
      - name: 🧪 Build snap on amd64
        uses: snapcrafters/ci/test-snap-build@main
```

## API

### Inputs

| Key       | Description                                                    | Required | Default |
| --------- | -------------------------------------------------------------- | :------: | :------ |
| `install` | If `true`, the built snap is install on the runner after build |    N     | `false` |

### Outputs

None

[review-tools]: https://snapcraft.io/review-tools
[snapcraft-review-tools]: https://github.com/diddlesnaps/snapcraft-review-action/tree/master
[dangerous]: https://securitylab.github.com/research/github-actions-preventing-pwn-requests/
