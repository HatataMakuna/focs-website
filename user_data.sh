# Either add "sudo" before all commands or use "sudo su" first
# Amazon Linux 2023

#!/bin/bash
dnf install git -y
git clone https://github.com/HatataMakuna/focs-website.git
cd focs-website
dnf install python-pip -y
pip3 install flask pymysql boto3
python3 app.py