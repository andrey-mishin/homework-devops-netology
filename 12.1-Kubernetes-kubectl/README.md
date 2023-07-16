# Домашнее задание к занятию «Kubernetes. Причины появления. Команда kubectl»

Рабочая машина под управлением Ubuntu 20.04 LTS, snap имеется, поэтому устанавливать его нет необходимости.  
  
Ход работы:
1. Установка `microk8s`:
```bash
baloo@pc:~$ sudo snap install microk8s --classic
[sudo] password for baloo:
microk8s (1.27/stable) v1.27.2 from Canonical✓ installed
```
  
2. Как в инструкции добавил своего пользователя в группу `microk8s`  
```bash
sudo usermod -a -G microk8s baloo
```
  
3. Менять права на директорию ~/.kube не пришлось, т.к. она и так принадлежала моему пользователю.  

4. Установил `Dashboard`:
```bash
baloo@pc:~$ microk8s enable bashboard
Addon bashboard was not found in any repository
baloo@pc:~$
baloo@pc:~$ microk8s enable dashboard
Infer repository core for addon dashboard
Enabling Kubernetes Dashboard
Infer repository core for addon metrics-server
Enabling Metrics-Server
serviceaccount/metrics-server created
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
clusterrole.rbac.authorization.k8s.io/system:metrics-server created
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created
service/metrics-server created
deployment.apps/metrics-server created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
clusterrolebinding.rbac.authorization.k8s.io/microk8s-admin created
[sudo] password for baloo:
Metrics-Server is enabled
Applying manifest
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
secret/microk8s-dashboard-token created

If RBAC is not enabled access the dashboard using the token retrieved with:

microk8s kubectl describe secret -n kube-system microk8s-dashboard-token

Use this token in the https login UI of the kubernetes-dashboard service.

In an RBAC enabled setup (microk8s enable RBAC) you need to create a user with restricted
permissions as shown in:
https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
```

5. Для первоначального захода в `Dashboard` создал **token**:
```bash
baloo@pc:~$ microk8s kubectl create token default
eyJhbGciOiJSUzI1NiIsImtpZCI6IkZCTnA1SjBwUEFtbVhfSllWUlp0bGRCOXVIRDVhUWYxU0JUZ2l4RjRaczgifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjIl0sImV4cCI6MTY4OTQ0MTM0OCwiaWF0IjoxNjg5NDM3NzQ4LCJpc3MiOiJodHRwczovL2t1YmVybmV0ZXMuZGVmYXVsdC5zdmMiLCJrdWJlcm5ldGVzLmlvIjp7Im5hbWVzcGFjZSI6ImRlZmF1bHQiLCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiZGVmYXVsdCIsInVpZCI6IjJlODNkMTNjLWExNWYtNDA0NS1iNGJiLWJjMjQ0MGQ4ZjY4YSJ9fSwibmJmIjoxNjg5NDM3NzQ4LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpkZWZhdWx0In0.inGD5r2rWZoPpDIDcynpUB-tD7R_vxN1LRlNjek-FSi8V5i4xnF_7sXxWmhwYkzcVa8XV22ZiyjlEnu03_Zgq2ORcTbCGLlnegsezyv8JRMsDgV6hbwWyU3rTe7fFFPZb-mEUCoUgMH-POpMs8I19tLSBT8r-uBevENc13tuTmAJMhUh0cjnXzlAnnRXJCaMNjXJ8_yWpK8tOzCdJqrufDBcyeaIxcqT4R-9GvSsicNxv1LnEKjIGgNdLIDnix1mwb7kV4qK0TyXFQkL5hG22vE7NofH9-SOsDQbI4LBsO9oQdx3st_5lStHc6UU9PT-9A92ApyEdCiupgpC1Bhkvg
```
  
6. Зашёл в [dashboard](./files/dashboard.jpeg) используя токен и проброс портов:
```bash
baloo@pc:~$ microk8s kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
Forwarding from 127.0.0.1:10443 -> 8443
Forwarding from [::1]:10443 -> 8443
Handling connection for 10443
Handling connection for 10443
Handling connection for 10443
```

![dashboard](./files/dashboard.jpeg)  
  
7. Самоподписанный сертификат создавал по это [инструкции](https://kubernetes.io/docs/tasks/administer-cluster/certificates/). Заменил исходные файлы (ca.crt, ca.key, ca.srl, server.crt, server.csr, server.key) вновь созданными, но `microk8s` отказался запускаться. После запуска, говорит, что не запущен:
```bash
baloo@pc:~$ microk8s status
microk8s is not running. Use microk8s inspect for a deeper inspection.
```
  
Пока что не знаю, что делать дальше.  
  
8. Скриншот команды `kubectl get nodes`:  
![nodes](./files/nodes.jpeg)


