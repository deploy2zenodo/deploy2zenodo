---
author: Daniel Mohr
date: 2023-10-20
license: ?
home: https://gitlab.com/daniel_mohr/deploy2zenodo
mirror: ?
latest_release: https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest
---

# `deploy2zenodo`

`deploy2zenodo` is a small script to deploy your data to
[zenodo](https://zenodo.org/). You can use it in a CI pipeline.

## CI pipeline

Using the keyword
[`include`](https://docs.gitlab.com/ee/ci/yaml/index.html#include)
it is possible to include YAML files and/or CI piplines in your
[GitLab](https://about.gitlab.com/) CI pipline.
In this way you can use a template of `deploy2zenodo` for your CI pipeline.

You can use the latest version
[deploy2zenodo.yaml](https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml)
in your CI pipeline.

Or you can use any special versions, e. g.
[deploy2zenodo.yaml v0.0.2](https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/0.0.2/downloads/deploy2zenodo.yaml).

A simple example could be:

```yaml
include:
  - remote: 'https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  stage: deploy
```

The provided gitlab ci template of `deploy2zenodo` uses
[`alpine:latest`](https://hub.docker.com/_/alpine)
and installs necessary software in `before_script`.
To use other images you must adapt the it, e. g.:


```yaml
include:
  - remote: 'https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  image:
    name: almalinux:latest
  before_script:
    - echo "nothing todo"
```
