yum install libseccomp-devel -y
cmake .
make
make install
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python36u -y
ln -s /bin/python3.6 /bin/python
yum install python36u-pip -y
ln -s /bin/pip3.6 /bin/pip3
cd bindings
python3 setup.py install
