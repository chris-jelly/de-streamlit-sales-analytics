## 1. Align runtime declarations to Python 3.13+

- [x] 1.1 Update `Dockerfile` base image tag to Python 3.13-slim and keep current runtime entrypoint/healthcheck behavior unchanged
- [x] 1.2 Update `.github/workflows/container-build.yml` test job to run on Python 3.13+
- [x] 1.3 Update `pyproject.toml` `requires-python` floor to 3.13+
- [x] 1.4 Update `README.md` and runtime contract docs to state Python 3.13+ requirement for local and container execution
- [x] 1.5 Replace Docker dependency installation from `pip` to `uv`
- [x] 1.6 Remove `requirements.txt` and update dependency workflow docs to use `uv` commands only

## 2. Validate dependency and execution compatibility

- [x] 2.1 Verify `uv sync` succeeds from `pyproject.toml` + `uv.lock` under Python 3.13
- [x] 2.2 Fix Python packaging discovery/configuration so `uv sync` completes without editable-build errors
- [x] 2.3 Run test suite under Python 3.13 and resolve any runtime incompatibilities
- [x] 2.4 Verify container build completes and app healthcheck still passes using Python 3.13 image

## 3. Apply annotation import policy

- [x] 3.1 Inventory all `from __future__ import annotations` usages in app and tests
- [x] 3.2 Remove redundant `from __future__ import annotations` imports where no concrete file-specific need exists
- [x] 3.3 Re-run tests after annotation-import cleanup to confirm no behavior changes

## 4. Finalize change quality gates

- [x] 4.1 Ensure CI workflow and docs consistently reflect the Python 3.13+ baseline
- [x] 4.2 Confirm all tasks map back to updated specs before requesting implementation review
