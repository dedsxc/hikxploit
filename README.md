# hikxsploit

Fork of https://github.com/M0tHs3C/Hikxploit

# Description
hixploit is a python tool that will give you the opportunity to gather all hikvision cctv that are vulnerable to a specific exploit and then change its password.
1. Use shodan API to scan hikvision camera worldwide
2. Exploit all cameras discovered by shodan API
3. Gather informations about country / city of the exploited camera
5. Write into csv file all cameras which have been exploited successfully

# Install
git clone https://github.com/dedsec-xo/hikxploit
python3 -m pip install -r requirements.txt

# Usage
1. Get your API key in shodan.io
2. Modify hikxploit.py file for : shodan_api_key="YOUR_API_KEY"
3. Launch the script
