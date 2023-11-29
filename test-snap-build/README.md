# snapcrafters/ci/test-snap-build

This action tries to build the snap "locally" on the Github Actions runner for `amd64` only. Once
the snap is built, it is reviewed using [review-tools](https://snapcraft.io/review-tools). Designed
to be a quick "smoke test" that doesn't require any special credentials or secrets.

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

None

### Outputs

None
