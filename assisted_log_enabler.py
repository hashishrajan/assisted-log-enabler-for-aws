#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# Assisted Log Enabler (ALE) - Find resources that are not logging, and turn them on.
# Joshua "DozerCat" McKiddy - Team DragonCat - AWS

import logging
import os
import json
import boto3
import time
import datetime
import argparse
from botocore.exceptions import ClientError
from datetime import timezone


from subfunctions import ALE_multi_account
from subfunctions import ALE_single_account


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
output_handle = logging.FileHandler('ALE_' + timestamp_date_string + '.log')
output_handle.setLevel(logging.INFO)
logger.addHandler(output_handle)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
output_handle.setFormatter(formatter)


def banner():
    """Function for Assisted Log Enabler banner"""
    print('''
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
         Twitter: @jdubm31
         Type -h for help.
    ''')


def assisted_log_enabler():
    """Function to run Assisted Log Enabler"""
    output_handle = logging.FileHandler('ALE_' + timestamp_date_string + '.log')
    output_handle.setLevel(logging.INFO)
    logger.addHandler(output_handle)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    output_handle.setFormatter(formatter)

    parser = argparse.ArgumentParser(description='Assisted Log Enabler - Find resources that are not logging, and turn them on.')
    parser.add_argument('--mode',help=' Choose the mode that you want to run Assisted Log Enabler in. Available modes: single_account, multi_account. WARNING: For multi_account, You must have the associated CloudFormation template deployed as a StackSet. See the README file for more details.')
    
    function_parser_group = parser.add_argument_group('Service Options', 'Use these flags to choose which services you want to turn logging on for.')
    function_parser_group.add_argument('--all', action='store_true', help=' Turns on all of the log types within the Assisted Log Enabler for AWS.')
    function_parser_group.add_argument('--eks', action='store_true', help=' Turns on Amazon EKS audit & authenticator logs.')
    function_parser_group.add_argument('--vpcflow', action='store_true', help=' Turns on Amazon VPC Flow Logs.')
    function_parser_group.add_argument('--r53querylogs', action='store_true', help=' Turns on Amazon Route 53 Resolver Query Logs.')
    function_parser_group.add_argument('--cloudtrail', action='store_true', help=' Turns on AWS CloudTrail.')

    args = parser.parse_args()
    banner()

    event = 'event'
    context = 'context'
    if args.mode == 'single_account':
        if args.eks:
            ALE_single_account.run_eks()
        elif args.vpcflow:
            ALE_single_account.run_vpc_flow_logs()
        elif args.r53querylogs:
            ALE_single_account.run_r53_query_logs()
        elif args.cloudtrail:
            ALE_single_account.run_cloudtrail()
        elif args.all:
            ALE_single_account.lambda_handler(event, context)
        else:
            logging.info("No valid option selected. Please run with -h to display valid options.")
    elif args.mode == 'multi_account':
        if args.eks:
            ALE_multi_account.run_eks()
        elif args.vpcflow:
            ALE_multi_account.run_vpc_flow_logs()
        elif args.r53querylogs:
            ALE_multi_account.run_r53_query_logs()
        elif args.all:
            ALE_multi_account.lambda_handler(event, context)
        else:
            logging.info("No valid option selected. Please run with -h to display valid options.")
    else:
        print("No valid option selected. Please run with -h to display valid options.")


if __name__ == '__main__':
    assisted_log_enabler()
