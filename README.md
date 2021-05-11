# Assisted Log Enabler for AWS - Find resources that are not logging, and turn them on.
This script is for customers who do not have logging turned on for various services, and lack knowledge of best practices and/or how to turn them on.

With this script, logging is turned on automatically for the various AWS Services for a customer:
* VPC Flow Logs (Single Account and Multi-Account using Organizations)
* CloudTrail (Single Account Only)
* EKS Audit and Authenticator Logs (Single Account Only)
* S3 Access Logs (future release)
* NEW! Route 53 Query Logs (Single Account Only)

## Use Case
There are customers of AWS who sometimes do not have logging turned on. When no logs are available, the ability to assist customers with analysis becomes limited, to the point that performing analysis may not be possible. Additionally, there are customers who use AWS that may not have the full technical expertise of how to set up logging for the various AWS services.

Assisted Log Enabler for AWS is designed to ease the customer burden of learning how to turn on logs in the middle of a security incident. Assisted Log Enabler for AWS performs the work of creating an S3 bucket, checking the services to see if logging is turned on, and activating logging when it's found to be off. When this is performed, the customer can be assured that logging within their AWS environment is active, in order to investigate future (and possibly ongoing) security incidents.

## Diagram
The following is a simple diagram on how Assisted Log Enabler for AWS works in a single account, in order to turn on logging for customers.

![Alt text](diagrams/assisted_log_enabler.png)

## Prerequesites
### Permissions
The following permissions are needed within AWS IAM for Assisted Log Enabler for AWS to run:
```
"ec2:DescribeVpcs",
"ec2:DescribeFlowLogs",
"ec2:CreateFlowLogs",
"logs:CreateLogDelivery",
"s3:GetBucketPolicy",
"s3:PutBucketPolicy",
"s3:PutLifecycleConfiguration"
"s3:PutObject",
"s3:CreateBucket",
"cloudtrail:StartLogging",
"cloudtrail:CreateTrail",
"cloudtrail:DescribeTrails",
"eks:UpdateClusterConfig",
"eks:ListClusters",
"route53resolver:ListResolverQueryLogConfigAssociations",
"route53resolver:CreateResolverQueryLogConfig",
"route53resolver:AssociateResolverQueryLogConfig"
```
Additionally, if running from within a AWS Lambda function, the function will need the AWSLambdaBasicExecutionRole in order to run successfully. Please refer to the following link for more details: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html

### Workflow Details
The following are the details of what happens within the Assisted Log Enabler for AWS workflow:
* An Amazon S3 bucket is created within the customer's account.
* A Lifecycle Policy is created for the bucket, with the following parameters:
   * Converts files to Intelligent-Tiering storage after 90 days
   * Deletes files after 365 days
* Block Public Access is explicitly set to On for the S3 bucket created. (Single Account only as of this release)
* VPCs are checked to see if flow logs are turned on or off.
* For VPCs that do not have flow logs turned on, VPC Flow Logging is turned on, and sent to the bucket created.
   * Amazon VPC Flow Logs version 2, 3, 4, and 5 fields are all enabled.
* AWS CloudTrail service is checked to see there is at least one CloudTrail configured. (Single Account only as of this release)
* If no trail is configured, one is created and configured to log to the bucket created. (Single Account only as of this release)
* If EKS Clusters exist, audit & authenticator logs are turned on. (Single Account only as of this release)
* NEW! Route 53 Query Logging is turned on for VPCs that do not have it turned on already.


### Running the Code
The code in its current form can be ran inside the following:
* AWS CloudShell (preferred)
* AWS Lambda

```
python3 assisted_log_enabler.py

 █████  ███████ ███████ ██ ███████ ████████ ███████ ██████  
██   ██ ██      ██      ██ ██         ██    ██      ██   ██ 
███████ ███████ ███████ ██ ███████    ██    █████   ██   ██ 
██   ██      ██      ██ ██      ██    ██    ██      ██   ██ 
██   ██ ███████ ███████ ██ ███████    ██    ███████ ██████  
                                                            
                                                            
                ██       ██████   ██████                   
                ██      ██    ██ ██                        
                ██      ██    ██ ██   ███                  
                ██      ██    ██ ██    ██                  
                ███████  ██████   ██████                    
                                                            
                                                            
███████ ███    ██  █████  ██████  ██      ███████ ██████    
██      ████   ██ ██   ██ ██   ██ ██      ██      ██   ██   
█████   ██ ██  ██ ███████ ██████  ██      █████   ██████    
██      ██  ██ ██ ██   ██ ██   ██ ██      ██      ██   ██   
███████ ██   ████ ██   ██ ██████  ███████ ███████ ██   ██ 
         Joshua "DozerCat" McKiddy - Team DragonCat - AWS
         Type -h for help.

No valid option selected. Please run with -h to display valid options.
```
* Options
```
python3 assisted_log_enabler.py -h
usage: assisted_log_enabler.py [-h] [--single_account] [--multi_account]

Assisted Log Enabler - Find resources that are not logging, and turn them on.

optional arguments:
  -h, --help        show this help message and exit
  --single_account  Run Assisted Log Enabler against a single AWS account.
  --multi_account   Run Assisted Log Enabler against a multi account AWS environment.
                    WARNING: You must have the associated CloudFormation
                    template deployed as a StackSet before running this
                    option.
```

#### Step-by-Step Instructions (for running in AWS CloudShell, single account mode)
1. Log into the AWS Console of the account you want to run the Assisted Log Enabler.
   * Ensure that the principal being used to log into the AWS Console has the permissions [above](https://github.com/awslabs/assisted-log-enabler-for-aws#permissions).
2. Click on the icon for AWS Cloudshell next to the search bar.
   * Ensure that you're in a region where AWS CloudShell is currently available.
3. Once the session begins, download the Assisted Log Enabler within the AWS CloudShell session.
```
git clone https://github.com/awslabs/assisted-log-enabler-for-aws.git
```
4. Unzip the file, and change the directory to the unzipped folder:
```
unzip assisted-log-enabler-for-aws-main.zip
cd assisted-log-enabler-for-aws-main
```
5. Run the following command to run the Assisted Log Enabler in single account mode:
```
python3 assisted_log_enabler.py --single_account
```


### Logging
A log file containing the detailed output of actions will be placed in the root directory of the Assited Log Enabler for AWS tool. The format of the file will be ALE_<timestamp>.log

Sample output within the log file:
```
2021-02-23 05:31:54,207 - INFO - Creating a list of VPCs without Flow Logs on in region us-west-2.
2021-02-23 05:31:54,208 - INFO - DescribeVpcs API Call
2021-02-23 05:31:54,679 - INFO - List of VPCs found within account 111122223333, region us-west-2:
2021-02-23 05:31:54,679 - INFO - DescribeFlowLogs API Call
2021-02-23 05:31:54,849 - INFO - List of VPCs found within account 111122223333, region us-west-2 WITHOUT VPC Flow Logs:
2021-02-23 05:31:54,849 - INFO - Activating logs for VPCs that do not have them turned on.
2021-02-23 05:31:54,849 - INFO - If all VPCs have Flow Logs turned on, you will get an MissingParameter error. That is normal.
2021-02-23 05:31:54,849 - INFO - CreateFlowLogs API Call
2021-02-23 05:31:54,944 - ERROR - An error occurred (MissingParameter) when calling the CreateFlowLogs operation: The request must include the ResourceIds parameter. Add the required parameter and retry the request.
2021-02-23 05:31:54,946 - INFO - Checking to see if CloudTrail is on, and will activate if needed.
2021-02-23 05:31:54,946 - INFO - DescribeTrails API Call
2021-02-23 05:31:54,983 - INFO - There is a CloudTrail trail active. No action needed.
2021-02-23 05:31:54,984 - INFO - Turning on audit and authenticator logging for EKS clusters in region af-south-1.
```

### Current Restrictions
* Currently, only the VPC Flow Logs can be turned on by the multi-account version.
   * Looking to add multi-account CloudTrail check in the next update.
   * Looking to add multi-account & multi-region EKS audit and authenticator logs in the next update.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.


## License

This project is licensed under the Apache-2.0 License.
