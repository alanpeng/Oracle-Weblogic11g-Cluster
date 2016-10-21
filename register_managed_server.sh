# Set environment.
export MW_HOME=/root/Oracle/Middleware
export WLS_HOME=$MW_HOME/wlserver_10.3
export WL_HOME=$WLS_HOME
export JAVA_HOME=/root/jdk/$JAVA16_HOME
export PATH=$JAVA_HOME/bin:$PATH
export DOMAIN_HOME=/root/Oracle/Middleware/user_projects/domains/base_domain

. $DOMAIN_HOME/bin/setDomainEnv.sh

# Create the managed servers.
java weblogic.WLST /root/Oracle/create_managed_server.py -p /root/Oracle/ManagedServer.properties
