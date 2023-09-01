#! /bin/bash

wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
apt-get update && apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev -y

tar -xzf Python-3.10.12.tgz && cd Python-3.10.12 && ./configure --prefix=/usr/local/python3.10 --enable-optimizations
make && make install
ln -s /usr/local/python3.10/bin/python3.10 /usr/bin/python
echo 'export PATH=$PATH:/usr/local/python3.10/bin' >> ~/.bashrc && source ~/.bashrc


apt-get install curl vim -y
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
ln -s /usr/local/python3.10/bin/pip /usr/bin/pip

apt-get install imagemagick -y
apt-get install ffmpeg -y
sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml



pip install --no-cache-dir --upgrade shortgpt -i https://mirrors.aliyun.com/pypi/simple/
