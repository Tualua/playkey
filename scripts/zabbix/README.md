####SELinux
Для того, чтобы Zabbix Agent мог получать данные от libvirtd нужно включить permissive-режим, мне так и не удалось найти нужные разрешения, чтобы это работало в обычном режиме. Если у кого-то получилось - пишите в issues, а пока даем команду

    semanage permissive -a zabbix_agent_t

####Возможные проблемы
Если Zabbix не получает _Template PlayKey: Get VM data_ с ошибкой _timeout while executing a shell script_, увеличьте параметр Timeout в конфигурационых файлах Zabbix Server и Zabbix Agent
