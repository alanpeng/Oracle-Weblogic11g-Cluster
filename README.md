# Oracle-Weblogic11g-Cluster-Rancher
Oracle WebLogic 11g version 1036 Dockerfile for cluster deployment on Rancher.

Usage:

One AdminServer with volume mount on local host or NFS shared storage and scalable ManagedServers in one Cluster.

To build your docker image, please modify the username and password of the Oracle website with your own.Please update 2 lines as below in the file "download_jdk6.sh" and "download_weblogic1036.sh":

v_oracle_website_user=peng.alan@gmail.com

v_oracle_website_password=Docker88

Source code: https://github.com/alanpeng/Oracle-Weblogic11g-Cluster

Anyway, you can pull the image directly form docker hub as below:

docker pull alanpeng/oracle-weblogic11g-cluster:1036

Once the stack has been launched, please log in the WebLogic admin console by http://your-admin-server-address:AdminPort

Default admin console port: 8001

Username: weblogic

Default password: 999999999

Default publish port for managed servers is 7001.
