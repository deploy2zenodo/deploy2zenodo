---
author: Daniel Mohr
date: 2026-05-26
license: Apache-2.0
home: https://gitlab.com/deploy2zenodo/deploy2zenodo
mirror: https://github.com/deploy2zenodo/deploy2zenodo
latest_release: https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest
doi: 10.5281/zenodo.10112959
---

# `deploy2zenodo` + `deploy2inveniordm`

[[_TOC_]]

## quick start (tldr)

Two lightweight shell scripts to automatically deploy your data or software to:

* Zenodo
* Invenio RDM instances

### which script to use

| target platform | script to use | API type | 
| ------ | ------ | ------ |
| [Zenodo](https://zenodo.org/) | [`deploy2zenodo`](README.deploy2zenodo.md) or [`deploy2inveniordm`](README.deploy2inveniordm.md) | Zenodo API or Zenodo Invenio RDM API (beta) |
| [Invenio RDM](https://inveniosoftware.org/products/rdm/) Instance | [`deploy2inveniordm`](README.deploy2inveniordm.md) | Invenio RDM API |

### example CI/CD integration

```yaml
include:
  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'

deploy2zenodo:
  rules:
    - if: $CI_COMMIT_TAG
  variables:
    DEPLOY2ZENODO_API_URL: "https://sandbox.zenodo.org/api"
    DEPLOY2ZENODO_JSON: "metadata.json"
    DEPLOY2ZENODO_DEPOSITION_ID: "create NEW record"
    DEPLOY2ZENODO_UPLOAD: "data.zip"
  before_script:
    - apk add --no-cache curl jq
    - publication_date=$(echo "$CI_COMMIT_TIMESTAMP" | grep -Eo "^[0-9]{4}-[0-9]{2}-[0-9]{2}")
    - |
      jq -c ".metadata.version = \"$CI_COMMIT_TAG\" |
        .metadata.publication_date = \"$publication_date\"" "$DEPLOY2ZENODO_JSON" | \
        tee "tmp.json" | jq -C .
    - mv "tmp.json" "$DEPLOY2ZENODO_JSON"
```

### example bash script

```bash
curl -L \
  "https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2inveniordm" \
  -o deploy2inveniordm && chmod +x deploy2inveniordm
export DEPLOY2INVENIORDM_API_URL="https://sandbox.zenodo.org/api"
 export DEPLOY2INVENIORDM_ACCESS_TOKEN="your-access-token"
export DEPLOY2INVENIORDM_JSON="metadata.json"
export DEPLOY2INVENIORDM_DEPOSITION_ID="create NEW record"
export DEPLOY2INVENIORDM_UPLOAD="data.zip"
./deploy2inveniordm
```

## preamble

[`deploy2zenodo`](https://gitlab.com/projects/51392274) are two lightweight
[shell](https://en.wikipedia.org/wiki/Bourne_shell) scripts to deploy
your data to [Zenodo](https://zenodo.org/) or
[Invenio RDM](https://inveniosoftware.org/products/rdm/),
the open-source repository platform powering Zenodo.
You can use them in a [CI pipeline](https://docs.gitlab.com/ee/ci/pipelines/)
as an automatic workflow.

Environmental variables provide high flexibility.
Depending on the selected flags, data can be curated

* before deployment in a merge request
* manually via the Zenodo web interface, or
* not curated at all.

**Note:** While `deploy2zenodo` is primarily tailored for the Zenodo API,
`deploy2inveniordm` is specifically designed for the
[Invenio RDM](https://inveniosoftware.org/products/rdm/) API
used by Zenodo.

## intention

To satisfy the FAIR[^fair1] principles[^fair2], publications should be
deposited to an open, persistent repository.
By publishing to such repositories, each publication receives a PID
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
tool for automatic publication to the open repository
[zenodo](https://zenodo.org/).

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

* [README.deploy2zenodo.md](README.deploy2zenodo.md)
* [README.deploy2inveniordm.md](README.deploy2inveniordm.md)

## license: Apache-2.0

`deploy2zenodo` and `deploy2inveniordm` are licensed under the [Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0).

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
