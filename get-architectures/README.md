# snapcrafters/ci/get-architectures

Parses a `snapcraft.yaml` and returns the list of architectures supported both as a JSON array, and
a space-separated string.

## Usage

```yaml
# ...
jobs:
  get-architectures:
    name: 🖥 Get snap architectures
    runs-on: ubuntu-latest
    outputs:
      architectures: ${{ steps.get-architectures.outputs.architectures }}
      architectures-list: ${{ steps.get-architectures.outputs.architectures-list }}
    steps:
      - name: 🖥 Get snap architectures
        id: get-architectures
        uses: snapcrafters/ci/get-architectures@main
```

## API

### Inputs

None

### Outputs

| Key                  | Description                                                    | Example             |
| -------------------- | -------------------------------------------------------------- | ------------------- |
| `architectures`      | A space-separated list of architectures supported by the snap. | `amd64 arm64`       |
| `architectures-list` | A JSON list of architectures supported by the snap             | `["amd64" "arm64"]` |
