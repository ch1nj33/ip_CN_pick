# -*- coding:utf-8 -*-
# @Time : 2023/8/12 10:59
# @Author : Ch1nJ33
# @Project : 0x03 Python_Script_Chin
# @File : pickup_ipcn_from_list.py
# @Description :

import os
import sys
import re
import getopt
from qqwry import QQwry
from alive_progress import alive_bar

cn_province_list = ['河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省',
                    '江西省', '山东省', '河南省', '广东省', '湖南省', '湖北省', '海南省', '四川省', '贵州省', '云南省',
                    '陕西省', '甘肃省', '青海省', '内蒙古', '广西', '西藏', '宁夏',
                    '新疆', '北京市', '天津市', '上海市', '重庆市']
cn_province_list = [province.strip() for province in cn_province_list]

# 初始化QQwry类
qqwry = QQwry()
# 加载纯真数据库
qqwry.load_file('./dat/qqwry_lastest.dat')


# IP地址格式检查
def re_match_ip_format(ip):
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if re.match(ip_pattern, ip):
        return True
    else:
        return False

def get_location(ip):
    if re_match_ip_format(ip):
        # 查询IP地址
        try:
            result = qqwry.lookup(ip)
        except:
            result = "IP地址格式错误"
    else:
        result = "IP地址格式错误"
    # 返回结果
    return result


def get_ip_cn_list(file_path):
    ip_cn_list = []
    ip_information_cn_list = []
    file = open(file_path, "r")
    ip_list = file.readlines()
    ip_list = [ip.rstrip() for ip in ip_list]
    len_of_file = len(ip_list)
    with alive_bar(len_of_file, title="loading", bar="blocks", spinner='waves2') as bar:
        for ip in ip_list:
            location_set = get_location(ip)
            ip_province = location_set[0]
            if location_set == 'IP地址格式错误':
                print(ip, 'IP地址格式错误')
            for province in cn_province_list:
                if re.match(province, ip_province):
                    # print('catch')
                    ip_information = ip + ' ' + ip_province
                    ip_cn_list.append(ip)
                    ip_information_cn_list.append(ip_information)
                    break
            bar()

    return ip_cn_list, ip_information_cn_list


def write_list_to_file(ip_cn_list, ip_information_cn_list, file_path_new):
    len_of_ip_cn_list = len(ip_cn_list)
    file_path_new_ip_cn = file_path_new + '_checkip' + '.txt'
    file_path_new_ip_information_cn = file_path_new + '_checkip_information' + '.txt'
    print("[*] IP_CN_list is ", file_path_new_ip_cn)
    with open(file_path_new_ip_cn, 'w') as fip:
        with alive_bar(len_of_ip_cn_list, title="loading", bar="blocks", spinner='waves3') as bar:
            for i in ip_cn_list:
                fip.write(i + '\n')
                bar()
    print("[*] IP_CN_information_list is ", file_path_new_ip_information_cn)
    with open(file_path_new_ip_information_cn, 'w') as fip_information:
        with alive_bar(len_of_ip_cn_list, title="loading", bar="blocks", spinner='waves3') as bar:
            for i in ip_information_cn_list:
                fip_information.write(i + '\n')
                bar()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '-h-f:-v', ['help', 'filename=', 'version', 'output='])
    except getopt.GetoptError as err:
        print("[-] 参数错误", str(err))
        usage()
        sys.exit(2)

    output = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-v', '--version'):
            print("[*] 版本信息 Version is 1.03 ")
            exit()
        elif opt in ('-f', '--filename'):
            file_path = arg
            file_name = os.path.basename(file_path)
            print("[*] Filename is ", file_name)
            # do something
            file_path_new = str(file_name).replace('.txt', '')
            print("[*] 开始检索--->")
            p_cn_list, ip_information_cn_list = get_ip_cn_list(file_path)
            print("[*] 开始保存--->")
            write_list_to_file(p_cn_list, ip_information_cn_list, file_path_new)
            exit()
        # elif opt == "--output":
        #     output = arg
        else:
            usage()
    usage()


def usage():
    print("usage: ip_CN_pick.py [-f <ip_list.txt>] ")
    print("                     [-v] [--version] ")
    print("                     [-h] [--help]")


if __name__ == "__main__":
    print("""
     ___________   _____  _   _  ______ _      _    
    |_   _| ___ \ /  __ \| \ | | | ___ (_)    | |   
      | | | |_/ / | /  \/|  \| | | |_/ /_  ___| | __
      | | |  __/  | |    | . ` | |  __/| |/ __| |/ /
     _| |_| |     | \__/\| |\  | | |   | | (__|   < 
     \___/\_|      \____/\_| \_/ \_|   |_|\___|_|\_\\
                                    Power by Ch1nJ33""")

    main()
