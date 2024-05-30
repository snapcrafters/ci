---
title: Call for testing `{{ env.snap_name }}`
labels: testing
---

A new version ({{ env.version }}) of `{{ env.snap_name }}` was just pushed to the `{{ env.channel }}` channel [in the snap store](https://snapcraft.io/{{ env.snap_name }}). The following revisions are available.

{{ env.table }}

## Automated testing

If configured, the snap will be installed in a VM, and any test results or screenshots will be posted to this issue as a comment shortly.

## How to test it manually

TESTING_INSTRUCTIONS

## How to release it

Maintainers can promote this to stable by commenting `/promote <rev>[,<rev>] {{ env.promotion_channel }} [done]`.

> For example
>
> - To promote a single revision, run `/promote <rev> {{ env.promotion_channel }}`
> - To promote multiple revisions, run `/promote <rev>,<rev> {{ env.promotion_channel }}`
> - To promote a revision and close the issue, run `/promote <rev>,<rev> {{ env.promotion_channel }} done`

You can promote all revisions that were just built with:

```
/promote {{ env.revisions }} {{ env.promotion_channel }} done
```
