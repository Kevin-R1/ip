import requests
from bs4 import BeautifulSoup
import re

def fetch_ips():
    # 示例：从不同API或网页抓取分类IP
    networks = {
        "电信": "https://monitor.gacjie.cn/page/cloudflare/ipv4.html",
        "联通": "https://ip.164746.xyz",
        "移动": "https://ip.164746.xyz"
    }
    
    ip_dict = {}
    for net, url in networks.items():
        try:
            response = requests.get(url, timeout=10)
            # 使用正则或BeautifulSoup提取IP（根据实际页面调整）
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+', response.text)
            ip_dict[net] = ips
        except Exception as e:
            print(f"Failed to fetch {net} IPs: {e}")
            ip_dict[net] = []
    return ip_dict

def write_ips(ip_dict):
    with open("ip.txt", "w", encoding="utf-8") as f:
        for net, ips in ip_dict.items():
            if ips:
                f.write(f"# {net} IP列表\n")
                for ip in ips:
                    f.write(f"{ip}\n")
                f.write("\n")  # 添加空行分隔不同网络

if __name__ == "__main__":
    ip_dict = fetch_ips()
    write_ips(ip_dict)