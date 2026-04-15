---
author: Daniel Mohr
date: 2026-04-15
license: Apache-2.0
home: https://gitlab.com/deploy2zenodo/deploy2zenodo
mirror: https://github.com/deploy2zenodo/deploy2zenodo
latest_release: https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest
doi: 10.5281/zenodo.10112959
---

# `deploy2inveniordm`

[[_TOC_]]

## preamble

[`deploy2inveniordm`](https://gitlab.com/projects/51392274) is a
[shell](https://en.wikipedia.org/wiki/Bourne_shell) script to deploy
your data to [Zenodo](https://zenodo.org/) using the
[Invenio RDM](https://inveniosoftware.org/products/rdm/) API.
You can use it in a [CI pipeline](https://docs.gitlab.com/ee/ci/pipelines/) as
an automatic workflow.

Environmental variables allow very flexible use.
Depending on the selected flags, the data can be curated before deployment
in a merge request, in the zenodo web interface or not curated at all.

**Note:** `deploy2inveniordm` is designed for the
[Invenio RDM](https://inveniosoftware.org/products/rdm/) API
used by Zenodo.
It may also work with
[Invenio RDM](https://inveniosoftware.org/products/rdm/),
but compatibility is not guaranteed or tested.
Test the script with any new API before using it.

## intention

To satisfy the FAIR[^fair1] principles[^fair2], publications should be
deployed to an open repository. In this way the publication gets a PID
([persistent identifier](https://en.wikipedia.org/wiki/Persistent_identifier))
and at least the metadata is publicly accessible, findable and citable.
Furthermore, current discussions about KPIs
([key performance indicator](https://en.wikipedia.org/wiki/Performance_indicator))
for software and data publications also lead to the need to generate PIDs
for software and data.

[^fair1]: [FAIR Principles](https://www.go-fair.org/fair-principles/)

[^fair2]: [An interpretation of the FAIR principles to guide implementations in the HMC digital ecosystem.](https://doi.org/10.3289/HMC_publ_01)

Especially software usually is not citable by a PID.
To overcome this and make software academically significant we provide here a
tool for automatic publication to the open repository [zenodo](https://zenodo.org/).

In principal the same is true for all kind of scientific data
(e. g. measurements, software and results such as papers).
For every data managed in a version control system an automatic publication
to an open repository is useful[^versioning].

[^versioning]: [Guidance on Versioning of Digital Assets.](https://doi.org/10.3289/HMC_publ_04)

Software in particular is subject to frequent changes, resulting in many
versions. This leads to the urge to automate the publishing process.
This is not only about making the software usable through software repositories,
but also about the citability of individual versions.

## how-to

There are many possibilities to use `deploy2inveniordm` but in this how-to section
we will focus on a few typically use cases.

### simple workflow

This workflow reflects the primary focus of `deploy2inveniordm`.

Go to your zenodo account and create an
[access token](https://developers.zenodo.org/?shell#authentication).

Store it in a [GitLab CI/CD variable](https://docs.gitlab.com/ee/ci/variables/)
as `DEPLOY2INVENIORDM_ACCESS_TOKEN`. Use the flags
[Mask variable](https://docs.gitlab.com/ee/ci/variables/index.html#mask-a-cicd-variable)
and [Protect variable](https://docs.gitlab.com/ee/ci/variables/index.html#protect-a-cicd-variable).
Masking ensures that the variable is not displayed in the CI/CD logs, and
protecting the variable limits access to authorized users.
Keep in mind the token is sensitive and private information.
Therefore you should not share it or make it public available.

Then the [GitLab CI/CD pipeline](https://docs.gitlab.com/ee/ci/pipelines/)
could look like (we use here [sandbox.zenodo.org](https://sandbox.zenodo.org/)
instead of [zenodo.org](https://zenodo.org/) for testing purpose):

```yaml
include:
  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2inveniordm.yaml'

prepare_release_and_deploy2inveniordm:
  stage: build
  image:
    name: alpine:latest
  variables:
    DEPLOY2INVENIORDM_JSON: "mymetadata.json"
  script:
    # prepare
    - TAG=$(grep version library.properties | cut -d "=" -f 2)
    - |
      echo '{"metadata":{"creators":[{"name":"family, given"}],\
        "license":{"id":"GPL-3.0-or-later"},"title":"test script alpine",\
        "version":"***","upload_type":"software"}}' | \
        jq ".metadata.version = \"$TAG\"" | tee "$DEPLOY2INVENIORDM_JSON"
    # prepare release
    - echo "DESCRIPTION=README.md" > variables.env
    - echo "TAG=$TAG" >> variables.env
    # prepare deploy2inveniordm
    - echo "DEPLOY2INVENIORDM_JSON=$DEPLOY2INVENIORDM_JSON" >> variables.env
    - DEPLOY2INVENIORDM_UPLOAD="v$TAG.zip"
    - git archive --format zip --output "$DEPLOY2INVENIORDM_UPLOAD" "$TAG"
    - echo "DEPLOY2INVENIORDM_UPLOAD=$DEPLOY2INVENIORDM_UPLOAD" >> variables.env
  artifacts:
    reports:
      dotenv: variables.env
    paths:
      - $DEPLOY2INVENIORDM_JSON

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

deploy2inveniordm:
  rules:
    - if: $CI_COMMIT_TAG
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  variables:
    DEPLOY2INVENIORDM_API_URL: "https://sandbox.zenodo.org/api"
    DEPLOY2INVENIORDM_DEPOSITION_ID: "create NEW record"
```

We use here 3 jobs:

* The job `prepare_release_and_deploy2inveniordm` prepares the
  variables and data for the following jobs. You can choose how to get
  the variables and data from your project/repository.
  (see hints in [DEPLOY2INVENIORDM_JSON](#deploy2inveniordm_json) and
  [DEPLOY2INVENIORDM_UPLOAD](#deploy2inveniordm_upload))
* The job `release_job` uses the workflow
  [Create release metadata in a custom script](https://docs.gitlab.com/ee/user/project/releases/release_cicd_examples.html#create-release-metadata-in-a-custom-script).
* The job `deploy2inveniordm` publishes the data to zenodo.

The variables are passed between the jobs using
[dotenv variables](https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html#artifactsreportsdotenv).
And the data are passed using
[job artifacts](https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html).

After the first run of the above pipeline (job `deploy2inveniordm`) adapt
`DEPLOY2INVENIORDM_DEPOSITION_ID` to store the record id. Only then you are
able to release new versions to zenodo.

In this example, `prepare_release_and_deploy2inveniordm` always runs
while the other jobs only run when the default branch is changed.
This makes it possible to check the artifacts during a merge request.

The used environment variables (see [script parameter](#script-parameter)) can
be provided in many different ways as a
[GitLab CI/CD variable](https://docs.gitlab.com/ee/ci/variables/), e. g.:

* [CI/CD variable in the UI](https://docs.gitlab.com/ee/ci/variables/#define-a-cicd-variable-in-the-ui)
  * not stored in the repository
  * possible to [Mask variable](https://docs.gitlab.com/ee/ci/variables/index.html#mask-a-cicd-variable)
  * possible to [Protect variable](https://docs.gitlab.com/ee/ci/variables/index.html#protect-a-cicd-variable)
  * used for private data (e. g. access token)
* [CI/CD variable in the .gitlab-ci.yml](https://docs.gitlab.com/ee/ci/variables/#define-a-cicd-variable-in-the-gitlab-ciyml-file)
  * stored in the repository
  * in public projects also publicly accessable

You should think about which information to store at which place.
Here a few simple considerations:

| variable | private data | note |
| ------ | ------ | ------ |
| DEPLOY2INVENIORDM_API_URL | no | Should a user find your publication? |
| DEPLOY2INVENIORDM_ACCESS_TOKEN | YES | Should not be shared with anyone! |
| DEPLOY2INVENIORDM_DEPOSITION_ID | no | Should a user find your publication? |
| DEPLOY2INVENIORDM_JSON | ? | Is the publication public? |
| DEPLOY2INVENIORDM_UPLOAD | ? | Is the publication public? |

Sometimes it is easier to change the variable in the UI.
For example in your first step you should set
`DEPLOY2INVENIORDM_API_URL="https://sandbox.zenodo.org/api"` and
`DEPLOY2INVENIORDM_DEPOSITION_ID="create NEW record"` to initiate and test your
pipeline. After success you should change to
`DEPLOY2INVENIORDM_API_URL="https://zenodo.org/api"`.
And after you have created your first record, also change
`DEPLOY2INVENIORDM_DEPOSITION_ID` to the returned value to update your dataset
next time (and not create a new one). If you store these variables in the user
interface, you can change them without touching your repository.
On the other hand, the metadata provided via `DEPLOY2INVENIORDM_JSON` and the
data provided via `DEPLOY2INVENIORDM_UPLOAD` may be created dynamically and
it could therefore make sense to create these variables dynamically as well.

There are also optional variables that can help to adapt the workflow to the
the individual use case.
For example, [DEPLOY2INVENIORDM_SKIP_PUBLISH](#deploy2inveniordm_skip_publish) allows
you to curate the upload to zenodo in the zenodo web interface before
publishing. This is especially useful if you are setting up the workflow for
the first time in your own project -- but can also be used at any time.

Depending on where variables are defined, they have different priorities.
For example, CI variables defined in the UI have priority and override the
variables stored in the `.gitlab-ci.yml` file with the
[keyword `variables`](https://docs.gitlab.com/ee/ci/yaml/#variables).
Variables that are defined at job level, in the `script`, `before_script` or
`after_script` sections, have the highest priority

An example test project is [deploy2inveniordm_test_simple_workflow_update](https://gitlab.com/projects/51647607).

### very simple workflow

It is not necessary to create a release for publication. But we think this
is the typically use case for software publication.

For a very simple workflow running when creating a tag,
you could use something like:

```yaml
include:
  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2inveniordm.yaml'

deploy2inveniordm:
  stage: deploy
  rules:
    - if: $CI_COMMIT_TAG
  variables:
    DEPLOY2INVENIORDM_API_URL: "https://sandbox.zenodo.org/api"
    DEPLOY2INVENIORDM_JSON: "CITATION.json"
    DEPLOY2INVENIORDM_DEPOSITION_ID: "create NEW record"
    DEPLOY2INVENIORDM_UPLOAD: "$CI_PROJECT_NAME-$CI_COMMIT_TAG.zip"
    DEPLOY2INVENIORDM_ADD_IsCompiledBy_DEPLOY2INVENIORDM: "yes"
    DEPLOY2INVENIORDM_ADD_IsNewVersionOf: "yes"
    DEPLOY2INVENIORDM_ADD_IsPartOf: "yes"
    DEPLOY2INVENIORDM_GET_METADATA: "result.json"
  before_script:
    - env
    - echo https://dl-cdn.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
    - apk add --no-cache cffconvert curl git jq
    - publication_date=$(echo "$CI_COMMIT_TIMESTAMP" | grep -Eo "^[0-9]{4}-[0-9]{2}-[0-9]{2}")
    - |
      cffconvert -i CITATION.cff -f zenodo | \
        jq -c '{"metadata": .} | .metadata += {"upload_type": "software"}' | \
        jq -c ".metadata.related_identifiers += [
          {\"relation\": \"isDerivedFrom\",
          \"identifier\": \"$CI_SERVER_URL/projects/$CI_PROJECT_ID\"}] |
          .metadata.version = \"$CI_COMMIT_TAG\" |
          .metadata.publication_date = \"$publication_date\"" | \
        tee "$DEPLOY2INVENIORDM_JSON" | jq -C .
    - git archive --format zip --output "$DEPLOY2INVENIORDM_UPLOAD" "$CI_COMMIT_TAG"
  artifacts:
    paths:
      - $DEPLOY2INVENIORDM_JSON
      - $DEPLOY2INVENIORDM_GET_METADATA
```

## license: Apache-2.0

`deploy2zenodo` has the license [Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0).

```txt
Copyright 2023-2026 Daniel Mohr and
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
