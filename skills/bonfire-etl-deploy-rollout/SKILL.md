---
name: bonfire-etl-deploy-rollout
description: Deploy or prepare rollout for Bonfire_ETL functions and infrastructure. Use for deploy_changed.sh, deploy_one.sh, rollout_catalog.sh, Terraform envs, ECR/Lambda image rollout, function URLs, SQS/DLQ wiring, dev/prod environment posture, or CI/CD deployment notes.
---

# Bonfire ETL Deploy Rollout

## Scope

Use this skill in `/Users/preston/Code/Bonfire_ETL` for deployment, rollout, Terraform, function catalog, and CI/CD work.

Bonfire_ETL deploys each ETL unit as an independently deployable AWS Lambda container image with SQS and Function URL triggers.

## First Reads

Read only what matches the task:

- `README.md` sections on infrastructure and current environment posture
- `docs/cicd-deployment-notes.md`
- `scripts/deploy_changed.sh`
- `scripts/deploy_one.sh`
- `scripts/rollout_catalog.sh`
- `scripts/build_lambda_image.sh`
- `scripts/validate_function_yaml.py`
- `infra/modules/bonfire_lambda_sqs_function/`
- `infra/envs/dev/main.tf`
- `infra/envs/dev/terraform.tfvars.example`

## Environment Rules

- The actively operated shared ETL environment is `dev` unless the user says otherwise.
- Treat `prod` as future or explicit-only.
- Do not apply Terraform or deploy to production without explicit user approval.
- Be careful with local Terraform state files; do not delete, reset, or migrate state unless the user requested that exact operation.
- Never print secrets from `terraform.tfvars`, environment files, AWS outputs, or logs.

## Workflow

1. Check `git status --short` to understand touched functions and unrelated changes.
2. Validate changed `function.yaml` files.
3. Run focused tests for changed functions before deploy when feasible.
4. Use existing scripts instead of ad hoc AWS commands when scripts cover the operation.
5. Confirm which environment is targeted before commands that deploy, apply Terraform, or mutate AWS.
6. Summarize function names, image/build/deploy status, Terraform status, and any manual follow-up.

## Useful Commands

```bash
python3 scripts/validate_function_yaml.py functions/<function_name>/function.yaml
./scripts/deploy_one.sh <function_name>
./scripts/deploy_changed.sh
./scripts/rollout_catalog.sh
./scripts/terraform_validate.sh
```

Inspect each script before using it if arguments, environment requirements, or side effects are unclear.

## Rollout Checks

For a new function, verify:

- `function.yaml` has queue, dlq, route, owner, image, and required env placeholders.
- Terraform includes the function and queue wiring.
- Queue names match router/env names.
- IAM permissions cover only needed services/secrets.
- Tests cover handler and logic behavior.
- README explains local invocation and expected payload shape when nearby functions do.
