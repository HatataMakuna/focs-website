# Either add "sudo" before all commands or use "sudo su" first
# Amazon Linux 2023

#!/bin/bash
dnf install git python-pip -y
git clone https://github.com/HatataMakuna/focs-website.git
wget https://amazoncloudwatch-agent.s3.us-east-1.amazonaws.com/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm
echo "{\"agent\":{\"run_as_user\":\"root\"},\"logs\":{\"logs_collected\":{\"files\":{\"collect_list\":[{\"file_path\":\"/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log\",\"log_group_name\":\"/aws/ec2\",\"log_stream_name\":\"{instance_id}\",\"retention_in_days\":7}]}}}}" > /amazon-cloudwatch-agent.json
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/amazon-cloudwatch-agent.json
cd focs-website
pip3 install -r requirements.txt
python3 server/app.py
