#!/bin/bash
# Replace the IP 172.17.x.x with 10.42.x.x in the hosts file
SELF_IP=`curl -s http://rancher-metadata/latest/self/container/ips/0`
rm -f /etc/hosts.old
cp /etc/hosts /etc/hosts.old
/bin/sed -e "s/.*`hostname`/${SELF_IP} `hostname`/g" /etc/hosts.old > /etc/hosts

# Update the create-wls-domain.py file
/bin/sed -i "s/^.*cmo.setPassword.*$/cmo.setPassword('${base_domain_default_password}')/" /root/Oracle/create-wls-domain.py
/bin/sed -i "s/^.*ListenAddress.*$/set('ListenAddress','${SELF_IP}')/" /root/Oracle/create-wls-domain.py
/bin/sed -i "s/^.*ListenPort.*$/set('ListenPort',${AdminPort})/" /root/Oracle/create-wls-domain.py

# Init the base domain
startfile="/root/Oracle/Middleware/user_projects/domains/base_domain/startWebLogic.sh"
if [ ! -f "$startfile" ] 
then
    /root/Oracle/Middleware/wlserver_10.3/common/bin/wlst.sh -skipWLSModuleScanning /root/Oracle/create-wls-domain.py
fi

# Start Weblogic Server or Managed Server
if [ "$Server_Role" = 'Admin' ]; then
    /root/Oracle/Middleware/user_projects/domains/base_domain/startWebLogic.sh
fi

if [ "$Server_Role" = 'Managed' ]; then
    
    /bin/sed -i "s/^.*admin.password=.*$/admin.password=${base_domain_default_password}/" /root/Oracle/ManagedServer.properties
    /bin/sed -i "s/^.*admin.url=.*$/admin.url=t3:\/\/AdminServer:${AdminPort}/" /root/Oracle/ManagedServer.properties
    /bin/sed -i "s/^.*ms.address=.*$/ms.address=${SELF_IP}/g" /root/Oracle/ManagedServer.properties
    /bin/sed -i "s/^.*ms.name=.*$/ms.name=${HOSTNAME}/g" /root/Oracle/ManagedServer.properties

    /bin/sed -i "s/^.*WLS_USER=.*$/WLS_USER=\"weblogic\"/" /root/Oracle/Middleware/user_projects/domains/base_domain/bin/startManagedWebLogic.sh
    /bin/sed -i "s/^.*WLS_PW=.*$/WLS_PW=\"${base_domain_default_password}\"/" /root/Oracle/Middleware/user_projects/domains/base_domain/bin/startManagedWebLogic.sh

    /root/Oracle/register_managed_server.sh

    /root/Oracle/Middleware/user_projects/domains/base_domain/bin/startManagedWebLogic.sh $HOSTNAME http://AdminServer:$AdminPort
fi
