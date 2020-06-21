
Установка и настройка CentOS
#############################

Системные требования
********************
* Компьютер, подходящий под требования PlayKey Pro
* Два жестких диска: первый под установку ОС, второй под раздел с играми. Второй диск рекомендуется от 1 ТБ


Подготовка
**********
Скачайте минимальный дистрибутив `CentOS 7.8 <https://mirror.yandex.ru/centos/7.8.2003/isos/x86_64/CentOS-7-x86_64-Minimal-2003.iso>`_

Запишите его на USB-флэшку при помощи `Win32DiskImager <https://sourceforge.net/projects/win32diskimager/files/latest/download>`_ или `Rufus <https://rufus.ie/>`_


Установка
*********
Загрузите настраиваемый компьютер с этой флэшки. Загружаться необходимо в режиме UEFI.

.. image:: /images/install-boot.png

Выберите **Install CentOS 7**

На экране выбора языков выберите любой подходящий Вам язык и нажмите кнопку продолжения (**Continue**). Здесь и далее все снимки экрана будут сделаны с англоязычного установщика.

.. image:: /images/install-language-sel.png


Разметка диска
==============
Стандартная разметка LVM, предлагаемая установщиком не подойдет, поэтому ее необходимо изменить. **GameServer НЕ РАБОТАЕТ С LVM-разметкой!!!**
На экране **Installation Summary** выберите пункт **INSTALLATION DESTINATION**

.. image:: /images/install-summary.png

Проверьте, что на этом экране Вы выделили нужный диск. 

*ВНИМАНИЕ! Дальнейшие шаги приведут к БЕЗВОЗВРАТНОМУ УНИЧТОЖЕНИЮ ВСЕХ ДАННЫХ НА ВЫБРАННОМ ДИСКЕ!*
Так же необходимо в разделе **Other Storage Options** выбрать пункт **I will configure partitioning**, после чего нужно нажать **Done**.

.. image:: /images/install-dev-sel.png

Если на выбранном диске уже есть разделы от предыдущих установок, необходимо их удалить кнопкой ➖.
В пункте **New mount points will use the following partitioning scheme** выберите **Standard Partitioning** и нажмите **Click here to create them automatically**.

.. image:: /images/install-part-step1.png

У Вас должная появится такая таблица разделов. В случае, если установщик создал отдельный раздел **/home**, его нужно удалить, а раздел **/** удалить и затем заново создать.
Для создания раздела возпользуйтесь кнопкой ➕. **Обязательно проверьте**, что разделы **/** и **/boot** созданы с файловой системой **XFS**.

.. image:: /images/install-part-step2.png

После заавершения операций по разметке диска нажмите **Done** и подтвердите изменения кнопкой **Accept Changes**. 

.. image:: /images/install-part-accept.png

Настройка сетевого подключения
==============================

На экране **INSTALLATION SUMMARY** выберите **NETWORK & HOST NAME**.

.. image:: /images/install-net1.png

В поле **Host name** задайте полное доменное имя Вашего компьютера (необязательно) и включите сетевое подключение.

.. image:: /images/install-net1.png

После завершения настройки сети нажмите кнопку **Done**.

Прочие настройки
================

В разделе **DATE & TIME** выставьте нужный часовой пояс, в разделе **LANGUAGE SUPPORT** добавьте необходимые языки (необязательно) и после возврата на экран **INSTALLATION SUMMARY** в правом нижем углу нажмите **Begin Installation**.

.. image:: /images/install-begin.png

Установка паролей
=================

Непосредственно во время процесса установки операционной системы необходимо задать пароль суперпользователя (**root**), а так же создать обычного непривилегированного пользователя

.. image:: /images/install-passwords.png

Сначала выберите **ROOT PASSWORD** и задайте пароль суперпользователя, затем - **USER CREATION** и создайте пользователя **gamer**.

.. image:: /images/install-user-gamer.png

Не забудьте поставить галочки в пунктах **Make this user administrator** и **Require a password** to use this account. По завершении нажмите кнопку **Done** и дождитесь завершения установки и появления кнопки **Finish configuration**.

.. image:: /images/install-finish.png

Нажмите кнопку **Finish configuration** и ожидайте окончания настройки системы и появления кнопки **Reboot**.

.. image:: /images/install-reboot.png

Компьютер перезагрузится и установка системы будет завершена.

.. image:: /images/install-first-boot.png

Настройка CentOS
****************

На данном этапе мы произведем настройку операционной системы.

.. role:: bash(code)
   :language: bash

Обновление системы
==================

Войдите в систему с учетной записью **root** и паролем, который Вы задали на этапе установки. 
Дайте команду :bash:`yum -y update`.

После окончания установки обновленных пакетов, перезагрузите компьютер. 

Подключение к комьютеру через SSH
=================================

Войдите под любой учетной записью и дайте команду :bash:`ip addr`

Вы должны увидеть похожую картинку:

.. image:: /images/config-ip-addr.png

В данном случае мы видим, что сетевой адаптер называется **ens33** и получил адрес **10.224.30.32**

С этого момента все манипуляции крайне желательно производить через удаленное подключение, для того чтобы Вы могли копировать и вставлять команды из этого руководства.
Для подключения к компьютеру можно использовать **putty**, **mremoteNG**, **RoyalTS** и т.д., в целом, любую программу которая поддерживает протокол **SSH**.

Используя одну из этих программ, подключитесь к адресу, который Вы нашли ранее. 

*ВНИМАНИЕ! Не рекомендуется подключаться удаленно с использованием учетной записи суперпользователя! Настройки безопасности системы будут рассмотрены в отдельном разделе.*

Используйте для подключения учетную запись **gamer**. Для выполнения команд от имени суперпользователя воспользуйтесь командой :bash:`sudo`. Так как, почти все команды в данном разделе необходимо запускать с привилегиями суперпользователя, можно начинать сеанс работы с команды :bash:`sudo su`. Эта команда переключит Вас на пользователя **root**.

Установка tmux
==============

**tmux** - консольный мультиплексор. Очень полезен тем, что в случае отключения от удаленного компьютера, все команды которые вы успели отдать продолжат выполнение в фоновом режиме. 

Установите **tmux**.

.. code-block:: bash

   yum -y install tmux

Я рекомендую все удаленные сеансы работы начинать с отдачи команды :bash:`tmux`. 
В случае, если по каким-либо причинам сеанс связи оборвался, переподключитесь и дайте команду :bash:`tmux ls` и Вы увидите на экране список Ваших сеансов с номерами. Подключитесь к нужному сеансу при помощи :bash:`tmux attach -t номер`.

Настройка репозиториев
======================

Не все пакеты программ, которые нам понадобятся, входят в состав репозиториев поставляемых вместе с CentOS. Поэтому необходимо добавить нужные репозитории вручную, но сначала установите в систему несколько полезных утилит.

.. code-block:: bash

   yum -y install nano wget mc

**nano** - удобный консольный текстовый редактор, **wget** - консольная программа для загрузки файлов, **mc** - консольный двухпанельный файловый менеджер.

Добавим репозиторий **Elastic**, он потребуется для установки **filebeat**. Откройте текстовый редактор командой :bash:`nano /etc/yum.repos.d/elastic.repo` и вставьте туда следующий текст:

.. code-block:: none

   [elastic-6.x]
   name=Elastic repository for 6.x packages
   baseurl=https://artifacts.elastic.co/packages/6.x/yum
   gpgcheck=1
   gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
   enabled=1
   autorefresh=1
   type=rpm-md

Выход  из редактора с сохранением файла осуществляется нажатием Ctrl+X. Нажмите Y для подтверждения сохранения, проверьте имя файла и нажмите Enter.

Добавьте временный репозиторий Oracle Linux, из которого нам потребуется ядро Unbreakable Enterprise Kernel Release 5 командой :bash:`nano /etc/yum.repos.d/ol7-temp.repo` и вставьте текст:

.. code-block:: none

   [ol7_latest]
   name=Oracle Linux $releasever Latest ($basearch)
   baseurl=https://yum.oracle.com/repo/OracleLinux/OL7/latest/$basearch/
   gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
   gpgcheck=1
   enabled=1

Закройте текстовый редактор и добавьте публичные ключи Oracle.

.. code-block:: bash

   wget https://yum.oracle.com/RPM-GPG-KEY-oracle-ol7 -O /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
   gpg --quiet --with-fingerprint /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle

Установите репозиторий EPEL и centos-release-qemu-ev

.. code-block:: bash
   
   yum -y install centos-release-qemu-ev epel-release


Установите репозиторий ZFS. 

*ВНИМАНИЕ! Несмотря на то, что у мы используем версию CentOS 7.8, необходимо установить репозиторий для версии CentOS 7.6, т.к. GameServer требует для работы ZFS  версии 0.7.13*.

.. code-block:: bash

   yum -y install http://download.zfsonlinux.org/epel/zfs-release.el7_6.noarch.rpm


Установка ядра Unbreakable Enterprise Kernel Release 5
======================================================

В состав Centos 7.8 включено достаточно старое ядро 3.10 и несмотря на то, что команда разработчиков постоянно бэкпортирует туда исправления и дополнения из более новых ядер, для нормальной работы новых процессоров, таких как, например AMD Ryzen 3000, необходимо установить другое ядро. Посмотреть версию ядра, установленного в Вашей системе можно командой :bash:`uname -r`.

.. code-block:: none

   $ uname -r   
   3.10.0-1127.el7.x86_64

Установите новое ядро.

.. code-block:: bash

   yum -y install oraclelinux-release-el7
   mv /etc/yum.repos.d/ol7-temp.repo /etc/yum.repos.d/ol7-temp.repo.disabled
   yum-config-manager --disable ol7_latest
   yum -y install kernel-uek --enablerepo=ol7_latest

После установки перезагрузите компьютер командой :bash:`reboot`, затем, проверьте, что новое ядро загрузилось, командой :bash:`uname -r`

.. code-block:: none

   $ uname -r
   4.14.35-1902.301.1.el7uek.x86_64

Данная версия была актуальна на момент написания данного руководства. В Вашем случае номер версии может быть другим.

Установка ZFS
=============

ZFS - продвинутая файловая система, которая необходима GameServer для хранения образов виртуальных машин.

.. code-block:: bash

   yum -y install kernel-devel kernel-uek-devel 
   yum -y install zfs

Процесс установки займет достаточно длительное время, т.к. установщику необходимо скомпилировать модули для конкретной версии ядра. После окончания установки дайте команду :bash:`modprobe zfs` для загрузки модуля. В случае успешной загрузки команда не выведет никакой информации. Дополнительно, можно проверить загрузку модуля командой :bash:`dmesg -wH`. В случае успешной загрузки Вы увидите строчки:

.. code-block:: bash

   SPL: Loaded module v0.7.13-1
   ZFS: Loaded module v0.7.13-1, ZFS pool version 5000, ZFS filesystem version 5


Установка поддержки виртуализации
=================================

.. code-block:: bash

   yum -y install qemu-kvm-ev libvirt virt-install libvirt-python virt-install libvirt-client OVMF
   systemctl enable libvirtd --now

Установка Cockpit
=================

**Cockpit** - удобная система управления операционными системами Linux через web-интерфейс.

Установка:

.. code-block:: bash

   yum -y install cockpit cockpit-machines cockpit-storaged
   systemctl enable cockpit.socket --now

Установка дополнительных утилит
===============================

.. code-block:: bash

   yum -y install policycoreutils-python atop htop tcpdump telnet net-tools iptables-services iptables iscsi-initiator-utils bind-utils curl bridge-utils pciutils ntp
   yum -y install filebeat-6.6.1-1

Настройка SSH
=============

Для того, чтобы администраторы и разработчики могли получить доступ к Вашему компьютеру, необходимо внести некоторые изменения в конфигурацию демона **sshd**

Добавьте дополнительный порт, на котором будет слушать **sshd**. Делать это нужно в два этапа, сначала следует настроить SELinux, чтобы он знал, что демон будет слушать на дополнительно порту:

.. code-block:: bash

   semanage port -a -t ssh_port_t -p tcp 14009

Затем, настроим сам sshd. Откройте редактор командой :bash:`nano /etc/ssh/sshd_config`. Найдите и раскомментируйте строчку *#Port 22*, удалив символ **#** в начале строки. Затем, строчкой ниже, добавьте еще одну директиву  *Port 14009*. Так же, рекомендуется запретить удаленный вход суперпользователяВыйдите из редактора с сохранением и дайте следующую команду:

.. code-block:: bash

   systemctl restart sshd

После проведенных манипуляций попробуйте подключиться к комьютеру через ssh указав порт 14009, вместо стандартного 22


Настройка сети
==============

Для обеспечения подключения виртуальных машин к локальной сети, необходимо настроить сетевой мост.

Сначала удалите уже существующий мост, конфигурация которого не подходит для GameServer.

.. code-block:: bash

   virsh net-destroy default
   virsh net-undefine default

Проверьте, что Вы не забыли запустить **tmux**. О том, что вы работаете через tmux свидетельствует зеленая строка внизу экрана.

**ВНИМАНИЕ! Следующие шаги приведут Вас к отключению от компьютера, если вы работаете через удаленное подключение!**

Создайте скрипт настройки сетевого моста командой :bash:`nano ~/configure-bridge.sh` и отредактируйте его следующим образом:

.. code-block:: none

   interface=$(ip addr | grep -i broadcast | awk NR==1'{ print substr($2, 1, length($2)-1)}')
   nmcli con delete $interface
   nmcli con add type bridge ifname br0
   nmcli con modify bridge-br0 ipv4.method auto
   nmcli con modify bridge-br0 bridge.stp no
   nmcli con add type bridge-slave ifname $interface master br0
   reboot

Установите разрешение на запуск скрипта.

.. code-block:: bash

   chmod +x ~/configure-bridge.sh

Запустите скрипт.

.. code-block:: bash

   bash ~/configure-bridge.sh

После завершения работы скрипта, компьютер перезагрузится автоматически. После перезагрузки войдите в систему и проверьте сетевые настройки командой :bash:`ip addr`.

.. code-block:: bash

   $ ip addr
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
       link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
       inet 127.0.0.1/8 scope host lo
          valid_lft forever preferred_lft forever
       inet6 ::1/128 scope host
          valid_lft forever preferred_lft forever
   2: enp6s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
       link/ether 0a:e0:af:a2:37:d6 brd ff:ff:ff:ff:ff:ff
   3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
       link/ether 0a:e0:af:a2:37:d6 brd ff:ff:ff:ff:ff:ff
       inet 172.17.19.49/25 brd 172.17.19.127 scope global noprefixroute dynamic br0
          valid_lft 86112sec preferred_lft 86112sec
       inet6 fe80::9d0f:8800:1fb7:5b97/64 scope link noprefixroute
          valid_lft forever preferred_lft forever

Обратите внимание, что IP-адрес теперь присвоен интерфейсу **br0**.

Создайте настройки сети для виртуальных машин командой :bash:`nano ~/default.xml`

.. code-block:: xml

   <network>
      <name>default</name>
      <forward mode="bridge"/>
      <bridge name="br0" />
   </network>

Сохраните файл и выполните следующие команды:

.. code-block:: bash

   virsh net-define ~/default.xml
   virsh net-autostart default
   virsh net-start default

Удалите **firewalld**. В официальном образе для запуска PlayKey Pro не используется firewalld, поэтому по рекомендациям, полученным от разработчиков, его необходимо удалить.

.. code-block:: bash

   yum -y erase firewalld

Создайте папку для хранения системного журнала, чтобы он не удалялся при перезагрузке. Это пригодится для анализа работы GameServer

.. code-block:: bash

   mkdir -p /var/log/journal

На этом основная настройка завершена, в следующей части будет рассмотрена установка и настройка GameServer.