---
author: Daniel Mohr
date: 2023-10-30
license: Apache-2.0
home: https://gitlab.com/deploy2zenodo/deploy2zenodo
mirror: ?
latest_release: https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest
---

# `deploy2zenodo`

`deploy2zenodo` is a script to deploy your data to
[zenodo](https://zenodo.org/). You can use it in a CI pipeline.

## script parameter

Instead of command line parameters we use environment variables.

You have to provide the following variables:

| variable | content |
| ------ | ------ |
| DEPLOY2ZENODO_API_URL | The URL of the API to use. |
| DEPLOY2ZENODO_ACCESS_TOKEN | access token of zenodo |
| DEPLOY2ZENODO_DEPOSITION_ID | id of the deposition/record on zenodo |
| DEPLOY2ZENODO_JSON | file name with metadata in JSON format to upload |
| DEPLOY2ZENODO_UPLOAD | file name(s) to upload |

There are other optional variables:

| variable | content |
| ------ | ------ |
| DEPLOY2ZENODO_SKIP_PUBLISH | prepare record, but skip publishing |
| DEPLOY2ZENODO_DRYRUN | skip communicating with the external URL |
| DEPLOY2ZENODO_SKIPRUN | skip everything, only prints commands to execute |

### DEPLOY2ZENODO_API_URL

You can use the API of your own zenodo instance or you can use the
official [zenodo instance](https://about.zenodo.org/):

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
to `create NEW record`,
e. g. `DEPLOY2ZENODO_DEPOSITION_ID="create NEW record"`.
After creating this record read the script output
and adapt `DEPLOY2ZENODO_DEPOSITION_ID` for the next run with the returned
record `id`.

### DEPLOY2ZENODO_JSON

The given file should contain the metadata in JSON format.

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

You can find the necessary and possible fields on
[zenodo: Deposit metadata](https://developers.zenodo.org/#representation).

Or [cffconvert](https://github.com/citation-file-format/cffconvert) can help
you to create the necessary metadata in JSON format from a
[CITATION.cff file](https://github.com/citation-file-format/citation-file-format).
Unfortunately we need [jq](https://github.com/jqlang/jq) to correct the format,
e. g.:

```sh
cffconvert -i CITATION.cff -f zenodo | \
  jq -c '{"metadata": .}' | jq '.metadata += {"upload_type": "software"}' | \
  tee CITATION.json
```

As `description` you can use HTML. For example you could use
[pandoc](https://pandoc.org/) to convert your `README.md` to HTML and
[jq](https://github.com/jqlang/jq) to add the HTML code as JSON value:

```sh
pandoc -o README.html README.md
echo '{"metadata":{"title":"foo","upload_type":"software",
  "creators":[{"name":"ich","affiliation":"bar"}],
  "description":"foos description"}}' | \
  jq --rawfile README README.html '.metadata.description = $README' | jq . | \
  tee metadata.json
```

### DEPLOY2ZENODO_UPLOAD

The given file(s) will be uploaded as data. Typically this would be an archive.

For example you can create an archive of a tag from a git repository:

```sh
TAG=0.0.3
git archive --format zip --output $TAG.zip $TAG
```

File names with spaces are not supported. Instead if `DEPLOY2ZENODO_UPLOAD`
contains space(s) it is assumed that splitting at the spaces leads to many
files which should each be uploaded.

The reason not supporting spaces is that
[you cannot create a CI/CD variable that is an array](https://docs.gitlab.com/ee/ci/variables/index.html#store-multiple-values-in-one-variable).

### DEPLOY2ZENODO_SKIP_PUBLISH

If this variable is not empty the publishing step is skipped, e. g.:

```sh
 DEPLOY2ZENODO_SKIP_PUBLISH="true"
```

Only the record is prepared -- metadata and data is uploaded -- but not
published.
You can see what will be published as a preview in the web interface of zenodo
and initiate the publishing by pressing the button in the web interface.

This helps to integrate `deploy2zenodo` in your project.

### DEPLOY2ZENODO_DRYRUN

If this variable is not empty the communication to the given URL is skipped.
But your parameter are analyzed. This could help to integrate `deploy2zenodo`
in your project.

### DEPLOY2ZENODO_SKIPRUN

If this variable is not empty nearly everything is skipped.
Only the commands to be executed are echoed. This is for debugging purpose.

## CI pipeline

Using the keyword
[`include`](https://docs.gitlab.com/ee/ci/yaml/index.html#include)
it is possible to include YAML files and/or CI pipelines in your
[GitLab](https://about.gitlab.com/) CI pipeline.
In this way you can use a template of `deploy2zenodo` for your CI pipeline.

You can use the latest version
[deploy2zenodo.yaml](https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml)
in your CI pipeline.
Or you can use any special versions, e. g.
[deploy2zenodo.yaml v0.1.0](https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/0.1.0/downloads/deploy2zenodo.yaml).

A simple example choosing the stage to run could be:

```yaml
include:
  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  stage: deploy
```

The provided GitLab ci template of `deploy2zenodo` uses
[`alpine:latest`](https://hub.docker.com/_/alpine)
and installs necessary software in `before_script`.
To use other images you must adapt it, e. g.:

```yaml
include:
  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  image:
    name: almalinux:latest
  before_script:
    - echo "nothing to do"
```

## license: Apache-2.0

`deploy2zenodo` has the license [Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0).

```txt
Copyright 2023 Daniel Mohr and
   Deutsches Zentrum fuer Luft- und Raumfahrt e. V., D-51170 Koeln

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
