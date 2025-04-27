import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor

# 测试 IP 速度（通过下载小文件计算）
def test_speed(ip, port, timeout=5):
    try:
        proxy = {"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"}
        test_url = "http://speedtest.tele2.net/10MB.zip"  # 10MB 测试文件
        start_time = time.time()
        response = requests.get(test_url, proxies=proxy, timeout=timeout, stream=True)
        response.raise_for_status()
        downloaded = 0
        chunk_size = 1024  # 1KB per chunk
        for chunk in response.iter_content(chunk_size=chunk_size):
            downloaded += len(chunk)
            if time.time() - start_time > timeout:  # 超时停止
                break
        elapsed = time.time() - start_time
        speed_kbs = (downloaded / 1024) / elapsed  # 计算 KB/s
        return speed_kbs >= 700  # 只保留 ≥700Kb/s 的 IP
    except:
        return False

# 抓取 IP 并分类（示例：从公开代理网站）
def fetch_ips():
    ip_sources = {
        "电信": "https://www.example.com/telecom-proxies",
        "联通": "https://www.example.com/unicom-proxies",
        "移动": "https://www.example.com/mobile-proxies",
    }
    
    valid_ips = {"电信": [], "联通": [], "移动": []}
    
    for net, url in ip_sources.items():
        try:
            response = requests.get(url, timeout=10)
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)  # 匹配 IP:Port
            print(f"Found {len(ips)} {net} IPs, testing speed...")
            
            # 多线程测试速度（提高效率）
            with ThreadPoolExecutor(max_workers=10) as executor:
                for ip_port in ips:
                    ip, port = ip_port.split(":")
                    if executor.submit(test_speed, ip, port).result():
                        valid_ips[net].append(ip_port)
            
            print(f"✅ {net} 有效 IP: {len(valid_ips[net])}")
        except Exception as e:
            print(f"❌ {net} 抓取失败: {e}")
    
    return valid_ips

# 写入 ip.txt（标注运营商和速度）
def write_ips(ip_dict):
    with open("ip.txt", "w", encoding="utf-8") as f:
        for net, ips in ip_dict.items():
            if ips:
                f.write(f"# {net} (≥700Kb/s)\n")
                for ip in ips:
                    f.write(f"{ip}\n")
                f.write("\n")  # 空行分隔

if __name__ == "__main__":
    ip_dict = fetch_ips()
    write_ips(ip_dict)