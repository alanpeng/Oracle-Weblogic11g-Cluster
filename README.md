# Oracle-Weblogic11g-Cluster-Rancher
Oracle11g version 1036 Dockerfile for cluster deployment on Rancher.

ManagedServer:
  ports:
  - 7001:7001/tcp
  environment:
    AdminPort: '8001'
    Server_Role: Managed
    base_domain_default_password: '999999999'
  labels:
    io.rancher.scheduler.affinity:host_label: ManagedServer=True
    io.rancher.container.hostname_override: container_name
  tty: true
  image: alanpeng/oracle-weblogic11g-cluster
  stdin_open: true
  
AdminServer:
  ports:
  - 8001:8001/tcp
  environment:
    AdminPort: '8001'
    Server_Role: Admin
    base_domain_default_password: '999999999'
  labels:
    io.rancher.scheduler.affinity:host_label: AdminServer=True
    io.rancher.container.hostname_override: container_name
  tty: true
  image: alanpeng/oracle-weblogic11g-cluster
  volumes:
  - /root/WebLogic/user_projects:/root/Oracle/Middleware/user_projects
