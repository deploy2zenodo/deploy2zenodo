---
author: Daniel Mohr
date: 2023-10-23
license: ?
home: https://gitlab.com/daniel_mohr/deploy2zenodo/
mirror: ?
latest_release: https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest
---

# `deploy2zenodo`

`deploy2zenodo` is a small script to deploy your data to
[zenodo](https://zenodo.org/). You can use it in a CI pipeline.

## script parameter

Instead of command line parameters we use environment variables.

You have to provide the following variables:

| variable | content |
| ------ | ------ |
| DEPLOY2ZENODO_API_URL | The URL of the api to use. |
| DEPLOY2ZENODO_ACCESS_TOKEN | access token of zenodo |
| DEPLOY2ZENODO_DEPOSITION_ID | id of the deposition/record on zenodo |
| DEPLOY2ZENODO_JSON | file with metadata in json format to upload |
| DEPLOY2ZENODO_UPLOAD | file/data to upload |

### DEPLOY2ZENODO_API_URL

You can use the api of your own zenodo instance or you can use the
official [Zenodo instance](https://about.zenodo.org/):

| state | URL |
| ------ | ------ |
| production | [`https://zenodo.org/api`](https://zenodo.org/api) |
| testing | [`https://sandbox.zenodo.org/api`](https://sandbox.zenodo.org/api) |

### DEPLOY2ZENODO_ACCESS_TOKEN

To access your zenodo account you have to provide an
[access token](https://developers.zenodo.org/?shell#authentication).

### DEPLOY2ZENODO_DEPOSITION_ID

To update an existing record you have to provide the `id` of this record.

If you want to create a new record please set `DEPLOY2ZENODO_DEPOSITION_ID`
to `create NEW record`. After creating this record read the script output
and adapt `DEPLOY2ZENODO_DEPOSITION_ID` for the next run with the returned
record `id`.

### DEPLOY2ZENODO_JSON

The given file should contain the metadata in json format.

You can write this file on your own, e. g.:

```json
{
  "metadata": {
    "title": "foo",
    "upload_type": "software",
    "creators": [
      {
        "name": "ich",
        "affiliation": "bar"
      }
    ],
    "description": "foos description"
  }
}
```

Or you can create it from from a
[CITATION.cff file](https://github.com/citation-file-format/citation-file-format)
using [cffconvert](https://github.com/citation-file-format/cffconvert).

### DEPLOY2ZENODO_UPLOAD

The given file will be uploaded as data. Typically this would be an archive.

For example you can create an archive of a tag from a git repository:

```sh
TAG=0.0.3
git archive --format zip --output $TAG.zip $TAG
```

## CI pipeline

Using the keyword
[`include`](https://docs.gitlab.com/ee/ci/yaml/index.html#include)
it is possible to include YAML files and/or CI pipelines in your
[GitLab](https://about.gitlab.com/) CI pipeline.
In this way you can use a template of `deploy2zenodo` for your CI pipeline.

You can use the latest version
[deploy2zenodo.yaml](https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml)
in your CI pipeline.
Or you can use any special versions, e. g.
[deploy2zenodo.yaml v0.0.2](https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/0.0.2/downloads/deploy2zenodo.yaml).

A simple example choosing the stage to run could be:

```yaml
include:
  - remote: 'https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  stage: deploy
```

The provided GitLab ci template of `deploy2zenodo` uses
[`alpine:latest`](https://hub.docker.com/_/alpine)
and installs necessary software in `before_script`.
To use other images you must adapt it, e. g.:

```yaml
include:
  - remote: 'https://gitlab.com/daniel_mohr/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  image:
    name: almalinux:latest
  before_script:
    - echo "nothing to do"
```
