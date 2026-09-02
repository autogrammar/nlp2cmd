# Apache-2.0 License Migration Plan

## Objective

Make the repository's distributable license consistently Apache License 2.0.

## Current state

- `pyproject.toml` declares `Apache-2.0`.
- `README.md` declares Apache-2.0.
- The MIT text in `LICENSE` has been replaced with the standard Apache License 2.0 text.
- Commit `b7eadc9` has been pushed to `license/apache-2.0`.
- Pull request [#5](https://github.com/autogrammar/nlp2cmd/pull/5) contains only the `LICENSE` change.
- Required test jobs for Python 3.11 and 3.12 have passed.

## Remaining work

1. A repository collaborator other than the author of the last push must approve pull request #5. Repository rules require this approval.
2. Merge pull request #5 into `main` after the approval is present.
3. Confirm that GitHub recognizes the default branch as Apache-2.0 and that the displayed repository license is updated.
4. Include the updated `LICENSE` file in the next package release so PyPI source and wheel distributions match the project metadata.

## Scope decisions

- No other repository in the `autogrammar` organization was detected as MIT-licensed when this migration was prepared.
- Repositories with another license or without an identified license are out of scope for this change.
- This migration changes the license for future distributions. Existing copies received under MIT retain their already-granted MIT permissions.

## Completion criteria

The migration is complete when pull request #5 is merged, GitHub reports Apache-2.0 for `autogrammar/nlp2cmd`, and the next published package includes the Apache License 2.0 `LICENSE` file.
