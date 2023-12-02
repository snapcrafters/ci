# snapcrafters/ci/sync-version

Takes an `update-script` input which should be a script that automatically checks for version
updates to the upstream application, and modifies the `snapcraft.yaml` as appropriate. This action
takes care of identifying and committing those changes.

## Usage

```yaml
jobs:
  sync:
    name: 🔄 Sync version with upstream
    runs-on: ubuntu-latest
    steps:
      - name: 🔄 Sync version with upstream
        uses: snapcrafters/ci/sync-version@main
        with:
          token: ${{ secrets.TOKEN }}
          update-script: |
            VERSION=$(
                curl -sL https://api.github.com/repos/jnsgruk/gosherve/releases | 
                jq .  | grep tag_name | grep -v beta | head -n 1 | cut -d'"' -f4 | tr -d 'v'
            )
            sed -i 's/^\(version: \).*$/\1'"$VERSION"'/' snap/snapcraft.yaml
```

## API

### Inputs

| Key             | Description                                                                                        | Required |
| --------------- | -------------------------------------------------------------------------------------------------- | :------: |
| `token`         | A token with permissions to commit to the repository.                                              |    Y     |
| `update-script` | A script that checks for version updates and updates `snapcraft.yaml` and other files if required. |    Y     |

### Outputs

None
