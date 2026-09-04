# Privacy Policy

Effective date: 2026-09-04

`aoa-tiktok-connector` is an operator-controlled connector developed under the
Agents of Abyss project. It helps an authorized creator read, organize, and
prepare content from the TikTok account that the creator explicitly connects.

## Data handled

With the account holder's authorization, the connector may process the minimum
profile and public-video metadata required for the enabled feature. The initial
sandbox path requests only `user.info.basic` and `video.list`.

The connector does not request a TikTok password. OAuth tokens are stored only
in an operator-controlled secret store outside the public source repository.

## Use, retention, and sharing

Data is used only for retrieval, organization, drafting, and separately approved
publication functions. Data is not sold. The operator controls retention and can
remove locally retained data after revoking TikTok authorization. Public source
code and fixtures contain no account tokens or private exports.

Questions or deletion requests can be opened through the project's
[issue tracker](https://github.com/8Dionysus/aoa-tiktok-connector/issues/new).
Do not include passwords, tokens, or private account data in a public issue.
