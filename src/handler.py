from yaml import load, dump
import boto3
from shepherd import Shepherd
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

'''
Example Config file looks like:
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

We will iterate through each rule:
  - Use the AWS Tags api to find matching security groups.
  - Create an insance of Shepherd class with the provided rules
  - If the rule is set to enforce, make changes to the security groups via Shepherd.
  - Notify if any changes were made or would be made (if mode is not enforce)
'''

ec2 = boto3.client('ec2')

def handler(event,context):
    f = open("example_config.yaml","r")
    config = load(f.read(),Loader=Loader)
    f.close()
    for rule in config['rules']:
        groups = []
        for k,v in rule['matching_tags']:
            response = ec2.describe_security_groups(
                Filters=[
                    {
                        'Name': 'tag:'+k,
                        'Values': [
                            v,
                        ]
                    },
                ]
            )
            groups.extend(response['SecurityGroups'])
            while 'NextToken' in response:
                response = ec2.describe_security_groups(NextToken=response['NextToken'])
                groups.extend(response['SecurityGroups'])
        
        shepherd = Shepherd(rule['group_rules'],rule['mode'])
        shepherd.execute() #TODO







handler(0,0)