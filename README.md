# Security Group Shepherd


Security Group Shepherd is a tool that enforces state across security groups. Security Group Shepherd monitors security groups in an AWS Account and enforce rules on **ingress rules** attached to those groups.

This project is a work in progress.

# Proposal

Security groups can easily present a security risk. One open port to the internet can spell disaster.

While least privledge principles can prevent security groups from being opened up broadly, least privledge isn't always implemented perfectly, and can be bypassed in break-glass emergencies.

Cloudformation, Terraform, and Config Rules all have their own issues. They can declare security group configuration, but they don't **actively maintain state.**

I am proposing a tool that takes in a configuration file and maintains _boundaries_ of rules in that security group.

```yaml
rules:
  - matching_tags: 
      env: prod
    mode: enforce
    group_rules:
      tcp:
        22:
          - 10.0.0.0/8
          - sg-1234
        443:
          - 10.0.0.0/16
```

The above configuration would look for security groups with tags `env=prod` and remove all rules that are broader than the ones specified.

Examples:
- A rule allowing tcp traffic on port 123 to 0.0.0.0/0 would be removed, because we only allow tcp traffic on port 22 and 443.
- A rule allowing tcp traffic on port 22 to 10.216.124.0/24 would be untouched. This is a stricter rule than allowing tcp on port 22 to 10.0.0.0/8.
- A rule allowing all udp traffic would be removed. We do not have rules allowing udp traffic.
    
