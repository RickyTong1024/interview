yum install libseccomp-devel cmake redis -y
cmake .
make
make install
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python36u -y
ln -s /bin/python3.6 /bin/python3
yum install python36u-pip -y
ln -s /bin/pip3.6 /bin/pip3
cd bindings
python3 setup.py install
pip3 install --upgrade pip
pip3 install tornado
pip3 install django==2.1.2
pip3 install celery
pip3 install django-bootstrap3
pip3 install django-celery
pip3 install pymysql
pip3 install redis==2.10.6
pip3 install httplib2