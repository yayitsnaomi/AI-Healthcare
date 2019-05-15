#!/bin/bash

# To run this, use source project_init.sh

# Add project path as an environment variable
export PYTHONPATH='/nfs/home/user/project'

# Add S3 bucket and keys
export AWS_BUCKET_NAME=''
export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''

# Add RDS MySQL login info
export MYSQL_HOST=''
export MYSQL_USER=''
export MYSQL_PASSWORD=''