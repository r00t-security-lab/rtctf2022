#!/bin/bash
#echo "root:pyy" | chpasswd

# apt

# sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.tuna.tsinghua.edu.cn\/ubuntu\//g' /etc/apt/sources.list
# sed -i '/security/d' /etc/apt/sources.list

# mv /etc/apt/sources.list /etc/apt/sources.list.bak
# apt-key adv --keyserver hkp://keyserver.ubuntu.com --recv-keys ED444FF07D8D0BF6
# echo -e "deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib \n">/etc/apt/sources.list
# echo -e "deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib">>/etc/apt/sources.list

# apt update -y

pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple
pip install uvicorn[standard]
pip install -r requirements.txt
