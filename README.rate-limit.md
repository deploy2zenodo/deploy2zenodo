---
author: Daniel Mohr
date: 2026-11-05
license: Apache-2.0
home: https://gitlab.com/deploy2zenodo/deploy2zenodo
mirror: https://github.com/deploy2zenodo/deploy2zenodo
latest_release: https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest
doi: 10.5281/zenodo.10112959
---

# rate limits

[[_TOC_]]

Both gitlab.com and zenodo.org have rate limits.
Here is some more information.

## zenodo.org

zenodo.org currently enforces a rate limit of
[30 requests per minute](https://blog.zenodo.org/2025/11/25/2025-11-14-search-api-updates/).

Both `deploy2zenodo` and `deploy2inveniordm` have flags to work around the
rate limit:

* [DEPLOY2ZENODO_RATE_LIMIT](README.deploy2zenodo.md)
* [DEPLOY2INVENIORDM_RATE_LIMIT](README.deploy2inveniordm.md)

## gitlab.com

gitlab.com has limited unauthenticated requests to 60 requests per hour
per IP address since 2026-10-19
([announcement](https://about.gitlab.com/blog/rate-limit-change-2026/)).

The `include:remote` runs on your GitLab instance and is an unauthenticated
request. If your pipelines (or other pipelines) run frequently and include a
remote from gitlab.com, you have a few options (or workarounds):

### use a public release mirror

At the moment, we provide a
[public release mirror](https://codebase.helmholtz.cloud/deploy2zenodo/deploy2zenodo_release_mirror)
not subject to gitlab.com's rate limits.

Wherever a release of the upstream project is referenced, simply replace
`gitlab.com/deploy2zenodo/deploy2zenodo` with
`codebase.helmholtz.cloud/deploy2zenodo/deploy2zenodo_release_mirror`.

```diff
include:
-  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'
+  - remote: 'https://codebase.helmholtz.cloud/deploy2zenodo/deploy2zenodo_release_mirror/-/releases/permalink/latest/downloads/deploy2zenodo.yaml'
```

```diff
-SCRIPTURL=https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo
+SCRIPTURL=https://codebase.helmholtz.cloud/deploy2zenodo/deploy2zenodo_release_mirror/-/releases/permalink/latest/downloads/deploy2zenodo
```

In the same way, you can also get pinned versions:

```diff
include:
-  - remote: 'https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/0.8.1/downloads/deploy2inveniordm.yaml'
+  - remote: 'https://codebase.helmholtz.cloud/deploy2zenodo/deploy2zenodo_release_mirror/-/releases/0.8.1/downloads/deploy2inveniordm.yaml'
```

```diff
-SCRIPTURL=https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/0.8.1/downloads/deploy2inveniordm
+SCRIPTURL=https://codebase.helmholtz.cloud/deploy2zenodo/deploy2zenodo_release_mirror/-/releases/0.8.1/downloads/deploy2inveniordm
```

You can also create a release mirror on your own GitLab instance.

Note on freshness: A mirror on your own GitLab instance is pulled from upstream
and therefore lags behind it.

### download via gitlab runner

Instead of doing the include on the GitLab instance, you can also download and
run the shell script inside the GitLab runner. A minimal example could be:

```yaml
deploy2inveniordm:
  variables:
    SCRIPTURL: "https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2inveniordm"
  stage: .post
  image:
    name: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - curl -fL "$SCRIPTURL" | sh
```

### use a personal access token

The previous option already moves the request to your runner's IP.
Adding a
[personal access token](https://docs.gitlab.com/user/profile/personal_access_tokens/)
(PAT) further removes the request from the anonymous 60/h budget
entirely -- it then counts against your plan's authenticated limit
(5,000/h on Free).

1. Create a personal access token with the `read_api` scope
   (User Settings -> Access Tokens). For a minimal scope, use a
   "Fine-Grained PAT" with read-only access to the `deploy2zenodo` project
   only.
2. Store it in your project as a
   [masked CI/CD variable](https://docs.gitlab.com/ee/ci/variables/index.html#mask-a-cicd-variable),
   e.g. `DEPLOY2ZENODO_GITLAB_TOKEN`.
3. Use the token in the `curl` request (as shown below).

A minimal example could be:

```yaml
deploy2zenodo:
  variables:
    SCRIPTURL: "https://gitlab.com/deploy2zenodo/deploy2zenodo/-/releases/permalink/latest/downloads/deploy2zenodo"
  stage: .post
  image:
    name: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - curl -fL --header "PRIVATE-TOKEN: $DEPLOY2ZENODO_GITLAB_TOKEN"
      "$SCRIPTURL" | sh
```

### skip the include and use git-over-https

`git` operations (clone/fetch/push) over HTTPS are exempt from the new
anonymous plan limit of 60 requests/hour per IP; they are subject to a
separate, much higher limit
([15,000 requests per minute per IP unauthenticated git https traffic](https://docs.gitlab.com/user/gitlab_com/rate_limits/#rate-limits-by-plan)).
We can therefore replace `include` with a `git clone`.

However, this bypasses the release build: the CI/CD template is not available,
and the script from the repo only carries the meta DOI of deploy2zenodo, not
the DOI of your release.

```yaml
deploy2zenodo:
  stage: deploy
  rules:
    - if: $CI_COMMIT_TAG
  variables:
    DEPLOY2ZENODO_API_URL: "https://sandbox.zenodo.org/api"
    DEPLOY2ZENODO_JSON: "metadata.json"
    DEPLOY2ZENODO_DEPOSITION_ID: "create NEW record"
    DEPLOY2ZENODO_UPLOAD: "data.zip"
  before_script:
    - apk add --no-cache curl jq git
    - DEPLOY2ZENODO_REPO="$(mktemp -d)"
    - git clone --depth 1 --branch 0.8.1
      https://gitlab.com/deploy2zenodo/deploy2zenodo.git "$DEPLOY2ZENODO_REPO"
    - DEPLOY2ZENODO_SCRIPT="$(mktemp)"
    - install -m 755 "$DEPLOY2ZENODO_REPO"/deploy2zenodo "$DEPLOY2ZENODO_SCRIPT"
    - pubdate=$(echo "$CI_COMMIT_TIMESTAMP" | grep -Eo "^[0-9]{4}-[0-9]{2}-[0-9]{2}")
    - |
      jq -c ".metadata.version = \"$CI_COMMIT_TAG\" |
        .metadata.publication_date = \"$pubdate\"" "$DEPLOY2ZENODO_JSON" | \
        tee "tmp.json" | jq -C .
    - mv "tmp.json" "$DEPLOY2ZENODO_JSON"
  script:
    - "$DEPLOY2ZENODO_SCRIPT"
```

You could also combine this workaround with a personal access token.
