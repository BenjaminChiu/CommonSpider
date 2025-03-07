import socket  # 导入socket库以进行网络连接
import ipaddress  # 导入ipaddress库以处理IP地址


def scan_ip_range(ip_range):
    available_ips = []  # 用于存放可用的IP地址
    for ip in ip_range:
        try:
            socket.gethostbyaddr(ip)  # 尝试连接IP地址
            available_ips.append(ip)  # 连接成功则添加到可用IP列表
        except socket.herror:
            pass  # 连接失败则忽略
    return available_ips


def main():
    network = ipaddress.ip_network('192.168.10.0/24')  # 定义网段
    ip_range = [str(ip) for ip in network.hosts()]  # 获取网段内的所有主机IP
    available_ips = scan_ip_range(ip_range)  # 调用扫描函数

    print("可用的IP地址如下：")  # 提示信息
    for ip in available_ips:
        print(ip)  # 输出可用的IP地址


if __name__ == "__main__":
    main()  # 执行主函数