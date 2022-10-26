#!/bin/bash

# Packages
sudo mkdir /usr/local/maven
wget http://ftp.yz.yamagata-u.ac.jp/pub/network/apache/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz -O /tmp/apache-maven-3.8.6-bin.tar.gz
sudo tar xvzf /tmp/apache-maven-3.8.6-bin.tar.gz -C /usr/local/maven
#ln -s /usr/local/maven/apache-maven-3.8.6 /usr/local/maven/default

export PATH=$PATH:/usr/local/maven/apache-maven-3.8.6/bin

sudo yum install -y git

# Download sources
sudo mkdir /usr/local/bigdl
sudo chmod 777 /usr/local/bigdl -R
cd /usr/local/bigdl
git clone https://github.com/intel-analytics/BigDL.git master
cd master/scala
export MAVEN_OPTS="-Xmx2g -XX:ReservedCodeCacheSize=512m"

# Build
bash make-dist.sh -P spark_2.x
