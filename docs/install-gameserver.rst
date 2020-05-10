Установка и настройка GameServer
################################

.. role:: bash(code)
   :language: bash


Подготовка
**********

Подключитесь к настраиваемому компьютеру через SSH. 
Запустите tmux.
Дайте команду :bash:`sudo su` для перехода в режим суперпользователя

Создание раздела для виртуальных машин
======================================

Убедитесь, что модуль ядра zfs загружен, командой :bash:`lsmod | grep zfs`

.. code-block:: bash

    # lsmod | grep zfs
    zfs                  3555328  3
    zunicode              331776  1 zfs
    icp                   270336  1 zfs
    zcommon                69632  1 zfs
    znvpair                77824  2 zfs,zcommon
    spl                   106496  4 zfs,icp,znvpair,zcommon
    zavl                   16384  1 zfs

В случае, если вывод команды пустой, загрузите модуль командой :bash:`modprobe zfs`

Идентифицируйте диски, установленные в компьютере. Помните, мы используем один для системы, второй для данных. Выполните команду :bash:`lsblk`.

.. code-block:: bash

    # lsblk
    NAME    MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    nvme0n1 259:0    0 465.8G  0 disk
    sda       8:0    0 111.8G  0 disk
    ├─sda4    8:4    0  99.4G  0 part /
    ├─sda2    8:2    0     1G  0 part /boot
    ├─sda3    8:3    0  11.2G  0 part [SWAP]
    └─sda1    8:1    0   200M  0 part /boot/efi

В данном примере на диск с идентификатором **sda** установлена система, диск **nvme0n1** пустой и будет использован под хранение образов виртуальных машин.

Пример команды для создания пула ZFS Вы видите ниже. Обратите внимание на параметр **ashift**. При помощи него ZFS определяет минимальный размер транзакции (2\ :sup:`ashift`\). По поводу значения этого параметра нет единой точки зрения, я придерживаюсь мнения, что при создании пула на SSD его значение должно быть 13, для HDD его значение нужно выставить в 12. Если сомневаетесь - используйте значение 12, в любом случае, критичного влияния на производительность дисковой системы он не окажет. Также, не забудьте правильно указать путь к устройству. Если сомневаетесь, выполните команду :bash:`fdisk -l`, она покажет Вам информацию обо всех дисках, их разделах и вывыдет полный путь к каждому диску. Команда ниже создаст пул с именем data на устройстве **nvme0n1**. **Название пула изменять нельзя!**

*ВНИМАНИЕ! Данная команда УНИЧТОЖИТ ВСЕ ДАННЫЕ НА УКАЗАННОМ ДИСКЕ! ЕСЛИ У ВАС НА ЭТОМ ДИСКЕ УЖЕ ЛЕЖАТ ОБРАЗЫ ИГР PlayKey, то смотрите следующий пункт* 

.. code-block:: bash

    zpool create -o ashift=13 -f data /dev/nvme0n1

В случае, если Вы уже скачивали образы игр PlayKey на этот диск, выполните следующую команду:

.. code-block:: bash

    zpool import data

Установка GameServer
====================

Дистрибутив GameServer Вам необходимо получить у разработчиков. Он распространяется в виде бинарного пакета с именем GameServer. Скопируйте или скачайте его в домашнюю папку пользователя root - **/root** и выполните следующую команду:

.. code-block:: bash

    yum -y install /root/GameServer.rpm

Создайте и отредактируйте файл с настройками :bash:`nano /usr/local/etc/gameserver/conf.xml`

.. code-block:: bash

    <Config>
        <Host name="a">
            <UserId>1</UserId>
            <PlaykeyApi>http://api.playkey.net/</PlaykeyApi>
            <RemoteHost>52.136.241.61</RemoteHost>
            <RemotePort>13001</RemotePort>
            <AdapterName>NVIDIA GeForce GTX 1080 Ti</AdapterName>
            <SystemSnapshot>data/kvm/desktop/windows@</SystemSnapshot>
            <TemplateFile>/usr/local/etc/gameserver/template.xml</TemplateFile>
            <FilebeatConfig>/usr/local/share/GameServer/logstash/filebeat.yml</FilebeatConfig>
            <LogstashAddress>elk.playkey.net:12122</LogstashAddress>
            <VmAutoconf>
                <Minimal>
                    <Memory unit="GiB">8</Memory>
                    <Cpu>4</Cpu>
                </Minimal>
                <Memory unit="GiB">16</Memory>
                <Cpu>4</Cpu>
            </VmAutoconf>
        </Host>
    </Config>

Обратите внимание на параметры **UserID**, **TemplateFile** и раздел **VmAutoconf**. Первый параметр - это Ваш идентификатор в PlayKey и посмотреть его значение можно в личном кабинете по адресу https://playkey.net/en/account. Второй параметр - это путь к шаблону виртуальной машины. Если у Вас компьютер с процессором AMD, то необходимо это значение изменить на :bash:`/usr/local/etc/gameserver/template_amd.xml`, этот шаблон доступен после установки GameServer. В случае с процессором Intel, Вам необходимо загрузить его вручную перед запуском GameServer. Вы можете загрузить его из моего репозитория на GitHub следующей командой 

.. code-block:: bash

    wget https://raw.  -O /usr/local/etc/gameserver/template.xml



