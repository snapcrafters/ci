# snapcrafters/ci/update-snap

Checks all the sources in the snapcraft.yaml file of the repository, updates it
with any new version from the upstreams, and builds the snap to ensure that
everything works as expected.

## Usage

```yaml
name: Push new tag update to stable branch

on:
  schedule:
    # Daily for now
    - cron: '9 7 * * *'
  workflow_dispatch:

jobs:
  update-snapcraft-yaml:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout this repo
        uses: actions/checkout@v4
      - name: Run desktop-snaps action
        uses: ubuntu/desktop-snaps@stable
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repo: ${{ github.repository }}
```

## Repository with the python code

The updatesnapyaml.py program is available at https://github.com/ubuntu/desktop-snaps/

## Extra tokens in the snapcraft.yaml file

It is possible to add extra tokens in the snapcraft.yaml file to allow to specify
extra metadata about versions. These extra tokens are added as comments to avoid
them interfering with snap*. The format is the following:

```
parts:
  PART_NAME:
    PART_TOKENS
# ext:updatesnap
#   version-format:
#     EXTRA_TOKENS
# endext
    MORE_PART_TOKENS
```

The "# endext" line is optional. This format is designed to allow *update_snaps* to
just replace the '#' symbol with an space in the lines between 'ext:updatesnap' and
'endext', converting that in standard YAML code.

The available extra tokens are:

* format: includes an string specifying the version format. Thus, if the tags for this
  part are in the form "pixman-0.40.0", then the token should be:

    format: "pixman-%M.%m.%R"

  The %M token specifies where is the Major value; the %m specifies the minor, and
  the %R the revision.

  Format can also be defined in form of "%V" or "prefix/%V". The %V token indicates variation in versions or beta-releases.

  For example if tags follows format "1.0b2" or "debian/3.22.10+dfsg0-4", then token should be:
    format: "%V" or format: "debian/%V" respectively

  If the format is "%M.%m.%R", "%M.%m" or "v%M.%m.%R", *update_snap* will autodetect
  it, so in those cases it can be skipped.

* lower-than: followed by a version number in %M.%m.%R format, specifies that the only
  valid version values must be lower than that specified. An example is Gtk3, which
  has "lower-than: 4" to avoid showing Gtk4 updates.

* ignore-odd-minor: if specified as TRUE, version numbers with odd minor values will be
  ignored, because they are presumed to be development versions.

* same-major: if specified as TRUE, version numbers with a different major value than the
  current version will be ignored.

* same-minor: if specified as TRUE, version numbers with a different minor value than the
  current version will be ignored.

* no-9x-minors: if specified as TRUE, version numbers with a minor value equal or
  greater than 90 will be ignored. Useful for projects that use these minor numbers
  as "prelude" to a new major version.

* no-9x-revisions: if specified as TRUE, version numbers with a revision value equal or
  greater than 90 will be ignored. Useful for projects that use these revision numbers
  as "prelude" to a new minor version.

* ignore: don't try to check this entry. Useful for "archived" projects.

* allow-neither-tag-nor-branch: allows this part to have neither *source-tag* nor
  *source-branch* elements, thus using the default (usually *main*) branch. Without
  this element, a file with a part that has neither *source-tag* nor *source-branch*
  will be considered invalid.

* allow-branch: allows to use *source-branch* in the part instead of *source-tag*.
  A file with a part that has neither *source-tag* nor this element will be considered
  invalid.

* ignore-version: it can contain either a single string with a version number, or a
  list of strings with version numbers. Those versions would be ignored as update
  candidates. It is useful to avoid updating to versions that fail to build, or
  contain important errors.

## TODO

* Migrate to specific github and gitlab modules instead of using custom code

