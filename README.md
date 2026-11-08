# opensees-osx-arm64-test

Smoke tests for the osx-arm64 (Apple Silicon) build of the conda-forge
[opensees](https://github.com/conda-forge/opensees-feedstock) package.

The osx-arm64 package is cross-compiled on osx-64 in conda-forge CI, so its
recipe tests are skipped there. This repository runs them on a native Apple
Silicon GitHub Actions runner (`macos-14`).

## Usage

1. Find the Azure Pipelines `buildId` of the feedstock PR build (the number in
   `.../_build/results?buildId=NNNNNNN`). The PR must have
   `azure: store_build_artifacts: true` in `conda-forge.yml`.
2. Run the **Test opensees osx-arm64 build** workflow from the Actions tab
   with that `buildId`, a Python version, and an hdf5 variant.

The workflow downloads the matching package artifact, installs it together with
its dependencies from conda-forge, checks that the binaries are arm64, and runs
an elastic cantilever analysis with both the Python module and the Tcl
interpreter, comparing the tip deflection with P L^3 / (3 E I).
