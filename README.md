---
author: Daniel Mohr
date: 2026-04-15
license: Apache-2.0
home: https://gitlab.com/deploy2zenodo/deploy2zenodo
mirror: https://github.com/deploy2zenodo/deploy2zenodo
latest_release: https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest
doi: 10.5281/zenodo.10112959
---

# `deploy2zenodo` + `deploy2inveniordm`

[[_TOC_]]

## preamble

[`deploy2zenodo`](https://gitlab.com/projects/51392274) are two
[shell](https://en.wikipedia.org/wiki/Bourne_shell) scripts to deploy
your data to [Zenodo](https://zenodo.org/) or
[Invenio RDM](https://inveniosoftware.org/products/rdm/).
You can use it in a [CI pipeline](https://docs.gitlab.com/ee/ci/pipelines/) as
an automatic workflow.

Environmental variables allow very flexible use.
Depending on the selected flags, the data can be curated before deployment
in a merge request, in the zenodo web interface or not curated at all.

**Note:** `deploy2zenodo` is primarily designed for the Zenodo API.
`deploy2inveniordm` is designed for the
[Invenio RDM](https://inveniosoftware.org/products/rdm/) API
used by Zenodo.

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

* [README.deploy2zenodo.md](README.deploy2zenodo.md)
* [README.deploy2inveniordm.md](README.deploy2inveniordm.md)

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
