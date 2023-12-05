# snapcrafters/ci/parse-snapcraft-yaml

This action is more for use internally than otherwise. It's purpose is to either find a snapcraft.yaml file from a list of known common locations in a repository, or take the path to a snapcraft.yaml, then parse some information from it and provide that information as outputs. This action **will not** checkout the source code, and expects that to have already happened.

You only need to specify the `snapcraft-project-root` input if your `snapcraft.yaml` is not in one of the following locations:

- `.snapcraft.yaml`
- `build-aux/snap/snapcraft.yaml`
- `snap/snapcraft.yaml`
- `snapcraft.yaml`

The action will also try to locate files that can be used during the review phase to delcare plugs and slots. The default locations searched are:

- `slot-declaration.json`
- `.github/slot-declaration.json`
- `plug-declaration.json`
- `.github/plug-declaration.json`

## Usage

```yaml
# ...
jobs:
  parse-snapcraft-yaml:
    name: 🖥 Parse the snapcraft yaml file
    runs-on: ubuntu-latest
    steps:
      - name: Find and parse snapcraft.yaml
        id: snapcraft-yaml
        uses: snapcrafters/ci/parse-snapcraft-yaml@main
```

## API

### Inputs

| Key                      | Description                                                                                                                       | Required | Default |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | :------: | :------ |
| `snapcraft-project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. Do not include the trailing `/`. |    N     |         |

### Outputs

| Key            | Description                                                                                      | Example                    |
| -------------- | ------------------------------------------------------------------------------------------------ | -------------------------- |
| `classic`      | Whether to snap is strictly confined                                                             | `false`                    |
| `plugs-file`   | The location of a plugs declaration file to be used during review, if one was found              | `./plugs-declaration.json` |
| `project-root` | The root of the snapcraft project, where the `snapcraft` command would usually be executed from. | `./ffmpeg-2204-sdk`        |
| `slots-file`   | The location of a slots declaration file to be used during review, if one was found              | `./slots-declaration.json` |
| `snap_name`    | The name of the snap as declared in the snapcraft.yaml                                           | `signal-desktop`           |
| `version`      | The version declared in the snapcraft.yaml file                                                  | `6.41.0`                   |
| `yaml_path`    | The path to the snapcraft.yaml for the project                                                   | `snap/snapcraft.yaml`      |
