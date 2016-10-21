#!/usr/bin/python
# Save Script as : create_managed_server.py

import time
import getopt
import sys
import re

# Get location of the properties file.
properties = ''
try:
   opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
except getopt.GetoptError:
   print 'create_managed_server.py -p '
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'create_managed_server.py -p '
      sys.exit()
   elif opt in ("-p", "--properties"):
      properties = arg
print 'properties=', properties

# Load the properties from the properties file.
from java.io import FileInputStream
 
propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

# Set all variables from values in properties file.
adminUsername=configProps.get("admin.username")
adminPassword=configProps.get("admin.password")
adminURL=configProps.get("admin.url")
msName=configProps.get("ms.name")
msAddress=configProps.get("ms.address")
msPort=configProps.get("ms.port")
msCluster=configProps.get("ms.cluster")
msSSLPort=configProps.get("ms.sslport")
msMachine=configProps.get("ms.machine")

# Display the variable values.
print 'adminUsername=', adminUsername
print 'adminPassword=', adminPassword
print 'adminURL=', adminURL
print 'msName=', msName
print 'msAddress=', msAddress
print 'msPort=', msPort
print 'msCluster=', msCluster
print 'msSSLPort=', msSSLPort
print 'msMachine=', msMachine

# Connect to the AdminServer.
connect(adminUsername, adminPassword, adminURL)

edit()
startEdit()


# Create Cluster
try:
  cd('/Clusters/WebLogicCluster')
  print '===> Cluster \"WebLogicCluster\" already exists.'
  print '===> Bypass...'
except:
  cd('/')
  cmo.createCluster('WebLogicCluster')
  cd('/Clusters/WebLogicCluster')
  cmo.setClusterMessagingMode('unicast')
  cmo.setClusterBroadcastChannel('1');
#finally:
print '===> Created Cluster \"WebLogicCluster\".'

# Create Machine
try:
  cd('/Machines/Machine')
  print '===> Machine \"Machine\" already exists.'
  print '===> Bypass...'
except:
  cd('/')
  cmo.createMachine('Machine')
  cd('/Machines/Machine/NodeManager/Machine')
  cmo.setNMType('Plain');
#finally:
print '===> Created machine \"Machine\".'


# Check if the managed server is exists.
try: 
  cd('/Servers/' + msName)
  print '===> Server \"' +msName+'\" already exists.'
  print '===> It will be updated...'

  # No need to delete managed server
  #cmo.setCluster(None)
  #cmo.setMachine(None)
  #editService.getConfigurationManager().removeReferencesToBean(getMBean('/Servers/' + msName))
  #cd('/')
  #cmo.destroyServer(getMBean('/Servers/' + msName))
except:
  # Create the managed Server.
  cd('/')
  cmo.createServer(msName);
#finally:
print '===> Start to update managed server...'
  
cd('/Servers/' + msName)
cmo.setListenAddress(msAddress)
cmo.setListenPort(int(msPort))
#cmo.getWebServer().setMaxRequestParamterCount(25000)  ### It seems not compatible with version 11g.

# Direct stdout and stderr.
cd('/Servers/' + msName + '/Log/' + msName)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')

# Associate with a cluster.
cd('/Servers/' + msName)
cmo.setCluster(getMBean('/Clusters/' + msCluster))

# Enable SSL. Attach the keystore later.
cd('/Servers/' + msName + '/SSL/' + msName)
cmo.setEnabled(true)
cmo.setListenPort(int(msSSLPort))

# Associated with a node manager.
cd('/Servers/' + msName)
cmo.setMachine(getMBean('/Machines/' + msMachine))

# Build any data sources later.
cd('/Servers/' + msName + '/DataSource/' + msName)
cmo.setRmiJDBCSecurity(None)

# Manage logging.
cd('/Servers/' + msName + '/Log/' + msName)
cmo.setRotationType('byTime')
cmo.setFileCount(30)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')
cmo.setLogFileSeverity('Notice')

save()
activate()

disconnect()
exit()
