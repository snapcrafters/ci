# snapcrafters/ci/setup-ghvmctl

A simple Github Action for configuring [ghvmctl](https://github.com/snapcrafters/ghvmctl) for use
on Github Actions runners is also included in this repository. It has three major functions:

- Enable KVM on the runner
- Install and initialise LXD
- Install and configure `ghvmctl`

## Usage

```yaml
jobs:
  test-snap:
    runs-on: ubuntu-latest
    steps:
      - name: Setup ghvmctl
        uses: snapcrafters/ci/setup-ghvmctl@main

      - name: Prepare test environment
        run: |
          # Prepare the VM, install and launch the app on the desktop
          ghvmctl prepare
          ghvmctl snap-install signal-desktop --channel candidate
          ghvmctl snap-run signal-desktop

      - name: Take screenshots & output logs
        run: |
          ghvmctl screenshot-full
          ghvmctl screenshot-window
          ghvmctl exec "cat /home/ubuntu/signal-desktop.log"

      - name: Upload screenshots
        uses: actions/upload-artifact@v4
        with:
          name: "screenshots"
          path: "~/ghvmctl-screenshots/*.png"
```

## API

### Inputs

None

### Outputs

None
