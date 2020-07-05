### Подготовка

#### Пользователи и директории

    groupadd scripts
    usermod root -aG scripts
    usermod gamer -aG scripts
    usermod zabbix -aG scripts
    mkdir /scripts
    chown root:scripts /scripts
    chmod g+s /scripts
    
#### gsinfo.py

    yum -y install python2-pip
    yum -y install systemd-python
    pip install --upgrade pip
    pip install py-zabbix
    pip install prometheus_client

### Установка

    wget https://raw.githubusercontent.com/Tualua/playkey/master/scripts/zabbix/gsinfo.py -O /scripts/gsinfo.py
    wget https://raw.githubusercontent.com/Tualua/playkey/master/scripts/zabbix/vms.py -O /scripts/vms.py
    wget https://raw.githubusercontent.com/Tualua/playkey/master/scripts/zabbix/vminfo.py -O /scripts/vminfo.py
    wget https://raw.githubusercontent.com/Tualua/playkey/master/scripts/zabbix/dsinfo.py -O /scripts/dsinfo.py
    chmod +x /scripts/*.py
    wget https://raw.githubusercontent.com/Tualua/playkey/master/scripts/zabbix/gsinfo.service -O /lib/systemd/system/gsinfo.service
    systemctl daemon-reload
    systemctl enable gsinfo --now
    
#### sudo

Агент должен запускаться от имени пользователя, который имеет право пользоваться sudo. Вы можете использовать уже существующего пользователя gamer, но лучше будет наделить этим правом пользователя zabbix
Создайте `/etc/sudoers.d/zabbix` и впишите туда

    Defaults:zabbix    !requiretty
    zabbix ALL=(ALL) NOPASSWD:ALL

#### SELinux

Для того, чтобы Zabbix Agent мог получать данные от libvirtd нужно включить permissive-режим, мне так и не удалось найти нужные разрешения, чтобы это работало в обычном режиме. Если у кого-то получилось - пишите в issues, а пока даем команду

    semanage permissive -a zabbix_agent_t

#### Zabbix Agent

Добавьте строки из файла zabbix_agentd.conf. Раскомментируйте нужные строки в зависимости от того, какой у Вас процессор. Для AMD потребуется https://github.com/ocerman/zenpower. Установите и настройте lm_sensors. 

#### Zabbix Server

Импортируйте шаблон и привяжите к нужным хостам

#### Возможные проблемы

Если Zabbix не получает _Template PlayKey: Get VM data_ с ошибкой _timeout while executing a shell script_, увеличьте параметр Timeout в конфигурационых файлах Zabbix Server и Zabbix Agent
