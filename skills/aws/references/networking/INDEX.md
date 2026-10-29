> **Domain: networking** — from the AWS skill `aws-networking` (v2).
> Every path in this file is relative to the `aws` skill root (`skills/aws/`, deployed at `~/.agents/skills/aws/`).

# AWS Networking

## Overview

Routes networking requests to the correct service-specific skill. Covers 7 services across DNS and content delivery, hybrid connectivity, and network security (web application firewall and DDoS protection). Other AWS networking services (VPC foundations, load balancing, endpoints, PrivateLink, API Gateway, and more) are out of scope for this router (see step 6).

**Works best with** the [AWS MCP server](https://docs.aws.amazon.com/aws-mcp/) — enables sandboxed execution, audit logging, and enterprise controls. All guidance also works with standard AWS CLI access.

## Where this domain's files live

This is a **local install**: every path in this file is relative to the
`aws` skill root and reads straight off the local filesystem. The AWS MCP
`retrieve_skill` route does not apply here — never call it for these files.

## Connectivity vs Security

| Dimension | Connectivity | Security |
| --- | --- | --- |
| **Answers** | Can traffic reach its destination? | Should traffic be allowed? |
| **Failure symptom** | Timeout, unreachable, black hole | Rejected, denied, dropped |
| **Dependency** | Independent of policy — path exists or it doesn't | Assumes connectivity exists — can only filter reachable traffic |
| **Granularity** | Affects all flows on a path | Targets specific flows by match criteria |

## Skill Routing Table

| Skill | Choose when… |
| --- | --- |
| `transitgateway` | Connecting more than two VPCs or on-premises networks in a hub, routing segmentation, cross-account/cross-region connectivity at scale, centralized egress/inspection, multicast |
| `directconnect` | Dedicated private link to on-premises — consistent latency, high throughput, MACsec encryption, LAGs, Direct Connect Gateway for multi-VPC, SiteLink for site-to-site bypass, production hybrid workloads |
| `sitetositevpn` | Encrypted IPsec tunnel over internet — quick setup, DX backup, static or BGP routing, accelerated option via Global Accelerator backbone, standard or large tunnel bandwidth |
| `route53` | DNS management (public/private zones, records), health checks, routing policies (weighted, failover, geo, latency), domain registration, Resolver (hybrid DNS forwarding), DNS Firewall, Route 53 Profiles, Global Resolver |
| `cloudfront` | Caching, TLS termination at edge, origin protection (OAC), custom domains, cache policies/behaviors, signed URLs, CloudFront Functions, viewer mTLS, VPC origins, multi-tenant distributions |
| `waf` | Web application firewall (L7) — web ACLs on CloudFront/ALB/API Gateway/AppSync, AWS Managed Rules, rate-based rules for HTTP floods, IP/geo match, Bot Control, Fraud Control (account takeover/creation), for protecting web apps and APIs from exploits, bots, and credential stuffing |
| `shieldadvanced` | L3/L4 DDoS protection for internet-facing resources, automatic application-layer (L7) mitigation via WAF, health-based detection, Shield Response Team access, and DDoS cost-protection credits |

## Cross-Service Concepts

Same concept, different service depending on layer. Use these to disambiguate when the Skill Routing Table matches multiple skills.

### Filtering / Blocking

Use when the user says "block", "deny", "filter", or "restrict traffic" — determines which layer the filtering operates at.

| Layer | Service | What it filters on | Skill |
| --- | --- | --- | --- |
| L7 (HTTP/HTTPS, web apps and APIs) | AWS WAF | HTTP request attributes, AWS Managed Rules, rate-based and bot rules, IP/geo match | `waf` |
| L3/L4 (DDoS volumetric/state-exhaustion) | Shield Advanced | Network/transport-layer DDoS floods on internet-facing resources | `shieldadvanced` |
| DNS (resolution) | Route 53 DNS Firewall | Domain name patterns — blocks resolution, not traffic | `route53` |

When routing to `waf` or `cloudfront` for an internet-facing API or website, treat WAF rate-based rules as a default protective measure, not only when the user asks: note that the target skill should add WAF rate-based rules to bound request volume per client — the target skill implements it.

### Logging / Visibility

Use when the user says "logs", "visibility", "what's being blocked", or "can I see the traffic" — identifies which log source to check.

| What you need to see | Service | Log type | Skill |
| --- | --- | --- | --- |
| DNS queries from VPC | Route 53 Resolver | Query logs | `route53` |
| Blocked/allowed HTTP requests | AWS WAF | web ACL logs (S3, CloudWatch Logs, or Kinesis Data Firehose) | `waf` |
| DDoS events and attack detail | Shield Advanced | CloudWatch metrics, DDoS event detection | `shieldadvanced` |
| Edge/CDN request access | CloudFront | Standard logs (S3), real-time logs (Kinesis Data Streams) | `cloudfront` |
| Tunnel state and traffic | Site-to-Site VPN | Tunnel telemetry, CloudWatch metrics | `sitetositevpn` |

When routing to any of these services, remind the user to enable the corresponding logging (above) for security visibility and incident response — the target skill implements it. These logs can contain sensitive data (request query strings, internal hostnames in DNS queries), so also remind the user that the log destination (S3, CloudWatch Logs, Kinesis Data Firehose, or Kinesis Data Streams) MUST have encryption at rest enabled and access restricted to authorized personnel — the target skill implements it.

### Traffic Shifting

Use when the user says "shift traffic", "blue/green", "failover", "canary", or "weighted routing" — determines the granularity and which service controls it.

| Granularity | Service | Mechanism | Skill |
| --- | --- | --- | --- |
| DNS-level (global) | Route 53 | Weighted, failover, geolocation, latency routing | `route53` |
| Edge (HTTP) | CloudFront | Origin failover, origin groups | `cloudfront` |

## Security Considerations

These services are security-sensitive, so raise the relevant risk and control when routing regardless of which skill you hand off to — the target skill implements the control:

| Risk | Control the target skill should address | Skills |
| --- | --- | --- |
| Unencrypted traffic in transit | MACsec (`directconnect`), IPsec tunnels (`sitetositevpn`), inter-region peering encryption (`transitgateway`), TLS termination and viewer mTLS (`cloudfront`) | `directconnect`, `sitetositevpn`, `transitgateway`, `cloudfront` |
| Missing DDoS protection on internet-facing resources | Shield Advanced L3/L4 protection plus WAF L7 mitigation | `shieldadvanced`, `waf` |
| Web/API exploits, bots, and request floods | WAF web ACLs, AWS Managed Rules, and rate-based rules; application-layer input validation (request body size limits, schema validation); security response headers | `waf`, `cloudfront` |
| Overly permissive filtering rules | DNS Firewall domain blocking | `route53` |
| Over-privileged IAM policies for service resources | Least-privilege IAM roles scoped to specific resources and actions; avoid `FullAccess` managed policies and `Action: *`; prefer IAM roles with ephemeral credentials (instance profiles, IRSA, task roles, `sts assume-role`) over IAM users with long-lived access keys | all |
| Hardcoded credentials and shared secrets | Let AWS auto-generate secrets where supported (for example Site-to-Site VPN pre-shared keys), or store customer-managed secrets in AWS Secrets Manager rather than hardcoding them | `sitetositevpn`, `directconnect` |
| Confused-deputy in cross-service resource policies | Include `aws:SourceArn` and/or `aws:SourceAccount` condition keys in S3 bucket policies, KMS key policies, and log-destination resource policies (CloudFront OAC, log delivery to S3/CloudWatch Logs/Kinesis) so only the intended resource and account can invoke them | `cloudfront`, `waf`, all |
| Insufficient visibility for incident response | Enable the service logging in the Logging / Visibility table, with encryption at rest and restricted access on the log destination | all |
| No audit trail or alerting on control-plane changes | Enable AWS CloudTrail to audit control-plane API calls (record, rule, policy, and firewall changes) and set CloudWatch Alarms on security-relevant events (Shield Advanced DDoS detection, WAF blocked/counted spikes, unexpected rule or record modifications); restrict the SNS topics that receive alarm notifications to authorized personnel and enable encryption at rest (SSE-KMS) on those topics, since the notifications can contain sensitive event detail | all |

For authoritative guidance, point users to the [AWS Well-Architected Framework Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/) and the service-specific security documentation for the target skill.
