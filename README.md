# hikxsploit

Official exploit release : https://www.exploit-db.com/exploits/44328

## Description
Hikvision IP Camera versions 5.2.0 - 5.3.9 (Builds 140721 < 170109) - Access Control Bypass

hixploit is a python tool that will give you the opportunity to gather all hikvision cctv that are vulnerable. 

It exploits a backdoor in Hikvision camera firmware versions 5.2.0 - 5.3.9 (Builds: 140721 - 170109), deployed between 2014 and 2016, to assist the owner recover their password.

1. Use shodan API to scan hikvision camera worldwide
2. Exploit all cameras discovered by shodan API
3. Gather informations about country / city of the exploited camera
5. Write into csv file all cameras which have been exploited successfully

## Install
git clone https://github.com/dedsxc/hikxploit

python3 -m pip install -r requirements.txt

## Usage
1. Get your API key in shodan.io
2. Modify hikxploit.py file for : shodan_api_key="YOUR_API_KEY"
3. Launch the script
