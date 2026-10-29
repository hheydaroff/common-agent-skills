---
name: aws
description: "All of AWS in one skill — 25 domains of references and runnable scripts, from credentials to production. Use for anything AWS: credentials (aws login, expired session, AccessDenied), Bedrock/Knowledge Bases/AgentCore/prompt caching, SageMaker training, fine-tuning, endpoints, IAM roles and policies, VPC/Route 53/CloudFront/WAF, EC2/ASG or ECS/EKS/Fargate, Lambda/serverless/Step Functions, S3/EBS/EFS storage, RDS/Aurora/DynamoDB/DSQL, SQS/SNS/EventBridge/Kinesis/Kafka, CDK/CloudFormation/CI-CD, Security Hub/GuardDuty/Inspector, CloudWatch/X-Ray/Application Signals/Omni, billing and cost optimisation or spend projection, Cognito auth, AWS Blocks, Well-Architected reviews, migrating a vibe-coded web app to AWS, or boto3 / @aws-sdk v3 / aws-sdk-swift code. Start with the routing table below."
---

# AWS

A single skill for all of AWS. One router (this file) → one self-contained domain per
task. Nothing here is loaded until you read the domain file.

## Where the files live

- Domains: `references/<domain>/INDEX.md` — the judgment content. **Read before answering.**
- Deeper detail, code templates, examples: files beside that INDEX (nested trees are
  preserved 1:1 from the upstream skills), reachable by the links inside it.
- Runnable scripts: `references/<domain>/scripts/` — e.g.
  `references/observability/scripts/cloudwatch-omni/evaluate_traces.py`,
  `references/bedrock/scripts/fetch_bedrock_agent.py`,
  `references/launch/scripts/launch_with_aws.py`. Run them, don't retype them.
- Paths written inside any domain file are **relative to this skill's root**
  (`references/<domain>/...`), not to the file you are reading. Resolve from the skill root.
- Local install: files are on disk. Ignore any "AWS MCP `retrieve_skill`" instructions in
  an older reference — never call that tool for these files.

## How to work

1. **Credentials only when needed** → `references/signin/INDEX.md`. Ask before running
   `aws login`; never print keys or secrets.
2. **Pick the domain** from the table below, read its INDEX, then follow its links.
3. Several INDEX files are themselves routers (serverless, compute, database, containers,
   networking, storage, observability). Follow their decision tree before naming a service —
   do not answer from memory when they give you a rule.
4. **Domain files beat model priors.** Bedrock model IDs, SageMaker paths, quotas and IAM
   semantics change often. If a domain file contradicts your memory, the file wins; if two
   domains disagree, prefer the more specific one and say which you followed.
5. Cross-domain pointers: a domain file may name another AWS skill
   (`aws-compute`, `aws-containers`, `amazon-bedrock`…). Those are rows in this table —
   drop the `aws-` prefix (`aws-compute` → `references/compute/`) and `amazon-bedrock` →
   `references/bedrock/`.

## Routing table

| Domain | Load when | Path |
|---|---|---|
| signin | getting CLI/SDK credentials, `aws login`, expired token, `aws configure`, SSO vs login | `references/signin/INDEX.md` |
| bedrock | model invocation (Converse/InvokeModel), Knowledge Bases + Managed KB migration, Agents → AgentCore Harness migration, Guardrails, AgentCore runtime/gateway/memory/registry/payments, model selection & migration, quota/throttling, prompt caching, Bedrock cost tracking | `references/bedrock/INDEX.md` |
| ai-ml | SageMaker: training/processing jobs, fine-tuning (SFT/DPO/RLVR/RLAIF), model & benchmark selection, dataset transformation/evaluation, deployment + inference optimisation, endpoint diagnostics, MLflow, IAM/S3 wiring | `references/ai-ml/INDEX.md` |
| auth | Cognito user/identity pools, login page, MFA, OAuth/OIDC/PKCE, social/SAML federation, token refresh, JWT authorizers on API Gateway/ALB | `references/auth/INDEX.md` |
| billing-and-cost | Cost Explorer, budgets, Savings Plans/RIs, right-sizing, CUR + Athena, anomalies, pricing lookup, Free Tier, billing views | `references/billing-and-cost/INDEX.md` |
| cost-projection | multi-account cost collection, MoM/QoQ growth, conservative/base/aggressive forecasts, reseller or contract negotiation | `references/cost-projection/INDEX.md` |
| blocks | AWS Blocks infra-from-code apps, building blocks (KVStore, DistributedTable, Database, Auth, Realtime, AsyncJob, FileBucket), local dev, deploy | `references/blocks/INDEX.md` |
| cdk | CDK in TS/Python: constructs, stacks, bootstrap/deploy/diff/synth, CDK+CloudFormation errors, drift, refactors that must not replace resources | `references/cdk/INDEX.md` |
| cloudformation | CFN templates: authoring, cfn-lint / cfn-guard / cloudformation-validate, pre-deploy validation, Express mode, failed-stack root cause | `references/cloudformation/INDEX.md` |
| compute | EC2 fleets: instance types (Graviton, T credits, GPU), launch templates, ASG policies/refresh/Spot/warm pools, IMDSv2, placement, EIPs, AMI lifecycle, SSM fleet ops | `references/compute/INDEX.md` |
| containers | ECS/EKS/Fargate/ECR/Elastic Beanstalk: task definitions, services, Exec, Express mode, Managed Instances, cluster add-ons, image lifecycle | `references/containers/INDEX.md` |
| database | choosing or operating Aurora, DSQL, RDS, DynamoDB, Keyspaces, DocumentDB, Neptune, Timestream, ElastiCache, MemoryDB | `references/database/INDEX.md` |
| deployment | CodePipeline/CodeBuild/CodeDeploy/CodeArtifact/CodeConnections, buildspec/appspec, blue-green + canary/linear | `references/deployment/INDEX.md` |
| iam | roles, trust policies, condition operators, STS, Organizations, MFA, confused-deputy, bucket-policy denies, generating policies from source or a terraform plan | `references/iam/INDEX.md` |
| messaging-and-streaming | SQS, SNS, EventBridge (rules/Scheduler/Pipes), MQ, Kinesis, Firehose, Flink, MSK; email/SMS/WhatsApp channel routing (SES, End User Messaging) | `references/messaging-and-streaming/INDEX.md` |
| networking | Route 53, CloudFront, Transit Gateway, Direct Connect, Site-to-Site VPN, WAF managed rules, Shield Advanced | `references/networking/INDEX.md` |
| observability | CloudWatch (alarms, Logs Insights, EMF, dashboards, X-Ray/ADOT, canaries, CloudTrail, Dynamic Instrumentation, Application Signals) and CloudWatch Omni (SQL over logs/traces, PromQL, dashboards, alerts, agent-quality evals) | `references/observability/INDEX.md` |
| sdk-js-v3 | writing TS/JS against `@aws-sdk/*` v3: clients, config, serialization, middleware, paginators | `references/sdk-js-v3/INDEX.md` |
| sdk-python | boto3/botocore: clients/resources, sessions and credentials, `ClientError`, paginators/waiters, S3 transfers, presigned URLs, DynamoDB | `references/sdk-python/INDEX.md` |
| sdk-swift | writing Swift against `aws-sdk-swift` | `references/sdk-swift/INDEX.md` |
| security | Security Hub v2 (OCSF) + CSPM controls, GuardDuty, Inspector, Macie, Detective, Security Lake; posture and findings triage | `references/security/INDEX.md` |
| serverless | Lambda, API Gateway, EventBridge, Step Functions: pick the compute form factor, durable workflows, cold starts/SnapStart, concurrency, event sources, throttling | `references/serverless/INDEX.md` |
| storage | choosing S3/EBS/EFS/FSx/Storage Gateway, migration, replication and protection, cost, vector-embedding storage | `references/storage/INDEX.md` |
| well-architected | full/quick/pillar/lens Well-Architected reviews with BP IDs and Eisenhower-prioritised remediation | `references/well-architected/INDEX.md` |
| launch | migrating a vibe-coded app (Lovable/Bolt/Replit) or any frontend web app to AWS, ending in deployable AWS Blocks code | `references/launch/INDEX.md` |

## Provenance

24 domains are the AWS skill pack (`amazon-bedrock`, `aws-*`, `launch-with-aws`,
`signing-in-to-aws`), copied verbatim with its internal links rewritten to this layout;
each INDEX header names the upstream skill and version. `cost-projection` is the user's own
skill, and the Bedrock TypeScript prompt-caching recipe is a local addition. See
[ATTRIBUTION.md](ATTRIBUTION.md).

To refresh after AWS ships new versions: let the AWS installer re-install the pack into
`~/.agents/skills/` (answer `y`, not `never`), run
`bash scripts/sync-from-aws-skills.sh`, review the diff, then `bash deploy.sh` — which
removes the loose copies again. Never hand-edit a domain file.