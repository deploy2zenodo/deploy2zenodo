---
author: Daniel Mohr
date: 2023-10-30
license: Apache-2.0
home: https://gitlab.com/deploy2zenodo/deploy2zenodo
mirror: ?
latest_release: https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest
---

# `deploy2zenodo`

`deploy2zenodo` is a
[shell](https://en.wikipedia.org/wiki/Bourne_shell) script to deploy
your data to [zenodo](https://zenodo.org/).
You can use it in a [CI pipeline](https://docs.gitlab.com/ee/ci/pipelines/).

## how-to

There are many possibilities to use `deploy2zenodo` but in this how-to section
we will focus on a few typically use cases.

### simple workflow

This workflow reflects the primary focus of `deploy2zenodo`.

Go to your zenodo account and create an
[access token](https://developers.zenodo.org/?shell#authentication).

Store it in a [GitLab CI/CD variable](https://docs.gitlab.com/ee/ci/variables/)
as `DEPLOY2ZENODO_ACCESS_TOKEN`. Use the flags
[Mask variable](https://docs.gitlab.com/ee/ci/variables/index.html#mask-a-cicd-variable)
and [Protect variable](https://docs.gitlab.com/ee/ci/variables/index.html#protect-a-cicd-variable).

Then the [GitLab CI/CD pipeline](https://docs.gitlab.com/ee/ci/pipelines/)
could look like (we use here [sandbox.zenodo.org](https://sandbox.zenodo.org/)
instead of [zenodo](https://zenodo.org/) for testing purpose):

```yaml
include:
  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

prepare_release_and_deploy2zenodo:
  stage: build
  image:
    name: alpine:latest
  variables:
    DEPLOY2ZENODO_JSON: mymetadata.json
  script:
    # prepare
    - TAG=$(grep version library.properties | cut -d "=" -f 2)
    - |
      echo '{"metadata":{"creators":[{"name":"family, given"}],\
        "license":{"id":"GPL-3.0-or-later"},"title":"test script alpine",\
        "version":"***","upload_type":"software"}}' | \
        jq ".metadata.version = \"$TAG\"" | tee $DEPLOY2ZENODO_JSON
    # prepare release
    - echo "DESCRIPTION=README.md" > variables.env
    - echo "TAG=$TAG" >> variables.env
    # prepare deploy2zenodo
    - echo "DEPLOY2ZENODO_JSON=$DEPLOY2ZENODO_JSON" >> variables.env
    - DEPLOY2ZENODO_UPLOAD=v$TAG.zip
    - git archive --format zip --output v$TAG.zip $TAG
    - echo "DEPLOY2ZENODO_UPLOAD=$DEPLOY2ZENODO_UPLOAD" >> variables.env
  artifacts:
    expire_in: 1 hrs
    reports:
      dotenv: variables.env
    paths:
      - $DEPLOY2ZENODO_JSON

release_job:
  stage: deploy
  rules:
    - if: $CI_COMMIT_TAG
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  image:
    registry.gitlab.com/gitlab-org/release-cli:latest
  script:
    - cat /etc/os-release
  release:
    name: 'v$TAG'
    description: '$DESCRIPTION'
    tag_name: '$TAG'
    ref: '$CI_COMMIT_SHA'

deploy2zenodo:
  rules:
    - if: $CI_COMMIT_TAG
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  variables:
    DEPLOY2ZENODO_API_URL: https://sandbox.zenodo.org/api
    DEPLOY2ZENODO_DEPOSITION_ID: "create NEW record"
```

We use here 3 jobs:

* The job `prepare_release_and_deploy2zenodo` prepares the
  variables and data for the following jobs. You can choose how to get
  the variables and data from your project/repository.
* The job `release_job` uses the workflow
  [Create release metadata in a custom script](https://docs.gitlab.com/ee/user/project/releases/release_cicd_examples.html#create-release-metadata-in-a-custom-script).
* The job `deploy2zenodo` publishes the data to zenodo.

The variables are passed between the jobs using
[dotenv variables](https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html#artifactsreportsdotenv).
And the data are passed using
[job artifacts](https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html).

After the first run of the above pipeline (job `deploy2zenodo`) adapt
`DEPLOY2ZENODO_DEPOSITION_ID` to store the record id. Only then you are
able to release new versions to zenodo.

### triggered workflow

In many projects are more then one maintainer. Therefore it is not possible
to store the user token for zenodo as CI variable in the project.

But the project `A` with more then one maintainer can trigger a pipeline in
another (private) project `B` with only one maintainer, e. g.:

```yaml
trigger:
  stage: .post
  rules:
    - if: $CI_COMMIT_TAG
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  image:
    name: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -X POST --fail -F token="$TRIGGER_TOKEN" -F ref=main $TRIGGER_URL
```

In the project `B` you can do the normal use of `deploy2zenodo`, e. g.:

```yaml
prepare_deploy2zenodo:
  image:
    name: alpine:latest
  script:
    - PROJECT_A_REPO=$(mktemp -d)
    - git clone --branch main --depth 1 $PROJECT_A_URL
    - |
      (cd $PROJECT_A_REPO && \
       git archive --format zip -o $DEPLOY2ZENODO_UPLOAD \
       $(git tag | sort -t "." -n -k 3 | \
       tail -n 1)
  artifacts:
    expire_in: 1 hrs
    paths:
      - $DEPLOY2ZENODO_UPLOAD

deploy2zenodo:
  variables:
    DEPLOY2ZENODO_API_URL: https://sandbox.zenodo.org/api
    DEPLOY2ZENODO_DEPOSITION_ID: "create NEW record"
```

Be careful:
The trigger job from project `A` may overwrite variables in the triggered
job from project `B`. This could lead to security concerns.
Maybe [Restrict who can override variables](https://docs.gitlab.com/ee/ci/variables/index.html#restrict-who-can-override-variables)
could help to overcome this.

Another possibility is too use
[Secrets management providers](https://docs.gitlab.com/ee/ci/pipelines/pipeline_security.html#secrets-management-providers).

### complex workflow

This workflow splits the deploying to zenodo in steps. This allows to use
the zenodo record (e. g. the DOI) already in the data to publish.

```yaml
deploy2zenodo:
  rules:
    - if: '"0" == "1"'
      when: never

prepare_deploy2zenodo_step1:
  script:
    - ...

deploy2zenodo-step1:
  variables:
    - DEPLOY2ZENODO_SKIP_PUBLISH: "true"
    - DEPLOY2ZENODO_GET_METADATA: "newmetadata.json"
  extends: .deploy2zenodo
  after_script:
    - echo "DEPLOY2ZENODO_GET_METADATA=$DEPLOY2ZENODO_GET_METADATA" > variables.env
  artifacts:
    paths:
      - $DEPLOY2ZENODO_GET_METADATA
    reports:
      dotenv: variables.env

prepare_release:
  script:
    - echo "use the file \"$DEPLOY2ZENODO_GET_METADATA\""
    - ...

release_job:
  script:
    - ...

prepare_deploy2zenodo_step2:
  script:
    - ...

deploy2zenodo-step2:
  variables:
    - DEPLOY2ZENODO_SKIP_NEW_VERSION: "true"
  extends: .deploy2zenodo
```

In the step `prepare_release` you can use [jq](https://github.com/jqlang/jq)
to extract data. For example the preserved DOI is available by:

```sh
jq .metadata.prereserve_doi.doi "$DEPLOY2ZENODO_GET_METADATA"
```

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
| DEPLOY2ZENODO_SKIP_NEW_VERSION | skip creating new version |
| DEPLOY2ZENODO_GET_METADATA | write actual metadata to a file |
| DEPLOY2ZENODO_SKIP_UPLOAD | skip upload of data |

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
  jq --rawfile README README.html '.metadata.description = $README' | \
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

Together with DEPLOY2ZENODO_SKIP_NEW_VERSION this allows to split deploying
to zenodo in steps.

### DEPLOY2ZENODO_DRYRUN

If this variable is not empty the communication to the given URL is skipped.
But your parameter are analyzed. This could help to integrate `deploy2zenodo`
in your project.

### DEPLOY2ZENODO_SKIPRUN

If this variable is not empty nearly everything is skipped.
Only the commands to be executed are echoed. This is for debugging purpose.

### DEPLOY2ZENODO_SKIP_NEW_VERSION

If this variable is not empty the step creating a new version is skipped.
This allows to split deploying to zenodo in steps.

Between creating a new version and deploying to zenodo you can
use the zenodo record (e. g. the DOI) already in the data to publish:

```sh
jq .metadata.prereserve_doi.doi "$DEPLOY2ZENODO_GET_METADATA" >> README.md
```

Using a [manual job](https://docs.gitlab.com/ee/ci/jobs/job_control.html#create-a-job-that-must-be-run-manually)
allows you to first check the artifacts and data to be published
before the last job run.

### DEPLOY2ZENODO_GET_METADATA

If this variable is not empty the metadata of the record is stored in a
file with this name.

To get these data at the end of the script an additional communication
with the DEPLOY2ZENODO_API_URL server is done.

### DEPLOY2ZENODO_SKIP_UPLOAD

If this variable is not empty skip uploading the data. This is only
allowed if DEPLOY2ZENODO_SKIP_PUBLISH is not empty, too.

If you split deploying to zenodo in steps using DEPLOY2ZENODO_SKIP_PUBLISH and
DEPLOY2ZENODO_SKIP_NEW_VERSION you can avoid unnecessary traffic by using also
DEPLOY2ZENODO_SKIP_UPLOAD.

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

The provided GitLab CI template of `deploy2zenodo` uses
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
