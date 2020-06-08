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
    zfs create -p /data/kvm/desktop

В случае, если Вы уже скачивали образы игр PlayKey на этот диск, выполните следующую команду:

.. code-block:: bash

    zpool import data

Копирование игр с другого хоста
===============================

В случае, если у Вас уже есть работающий хост с GameServer, Вы можете скачать игры с него. Процедуру необходимо делать под пользователем **root**.

На новом хосте создайте папку для хранения ключей и настройте права доступа:

.. code-block:: bash

    mkdir /root/.ssh
    chmod 700 /root/.ssh

Включите авторизацию по открытому ключу для **ssh**. Для этого отредактируйте конфигурационный файл демона sshd командой :bash:`nano /etc/ssh/sshd_config` и найдите там строчку *PubkeyAuthentication*. Раскомментируйте ее (удалите символ **#** в начале строки). Строка должна выглядеть так:

.. code-block:: bash

    PubkeyAuthentication yes

Сохраните файл, выйдите из редактора и перезапустите демон sshd командой:

.. code-block:: bash

    systemctl restart sshd

Сгенерируйте SSH-ключи для пользователя root на уже работающем хосте:

.. code-block:: bash

    sudo su
    ssh-keygen -t ecdsa -b 521

Путь для ключа оставьте по умолчанию (просто нажмите Enter), кодовую фразу тоже вводить не нужно. Примерный вывод результатов:

.. code-block:: bash

    # ssh-keygen -t ecdsa -b 521
    Generating public/private ecdsa key pair.
    Enter file in which to save the key (/root/.ssh/id_ecdsa):
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /root/.ssh/id_ecdsa.
    Your public key has been saved in /root/.ssh/id_ecdsa.pub.
    The key fingerprint is:
    SHA256:BKKNlwGDVTAAw5Hwq2E6D31Z+FgMORJm2UFpnJ08XWY root@hostname
    The key's randomart image is:
    +---[ECDSA 521]---+
    |O=%O**.o .E      |
    |.B.B*==..o       |
    |  =.B  ..        |
    |   + = .         |
    |... . + S        |
    |o+   *           |
    |= . + .          |
    | + .             |
    |  .              |
    +----[SHA256]-----+

Теперь передайте открытый ключ на новый хост

.. code-block:: bash

    scp /root/.ssh/id_ecdsa.pub <IP-адрес нового хоста>:/root/.ssh/authorized_keys

После этого на новом хосте задайте нужные права на файл **authorized_keys**:

.. code-block:: bash

    chmod 600 /root/.ssh/authorized_keys

Теперь проверьте подключение со старого хоста на новый:

.. code-block:: bash

    ssh <IP-адрес нового хоста>

Подключение должно осуществиться без запроса пароля. Для завершения подключения введите команду :bash:`exit`

Для просмотра игр, установленных на старом хосте, дайте команду :bash:`zfs list -t snapshot`. Вывод будет примерно таким:

.. code-block:: bash

    # zfs list -t snapshot
    NAME                                                                USED  AVAIL  REFER  MOUNTPOINT
    data/kvm/desktop/csgo@1134                                         2.15M      -  21.5G  -
    data/kvm/desktop/csgo@1182                                            0B      -  21.5G  -
    data/kvm/desktop/dota2@2742                                         325M      -  28.4G  -
    data/kvm/desktop/dota2@2787                                           0B      -  28.4G  -
    data/kvm/desktop/fortnite@2474                                     3.78M      -  83.5G  -
    data/kvm/desktop/fortnite@2504                                        0B      -  83.5G  -
    data/kvm/desktop/gta5@2649                                         3.41M      -  90.2G  -
    data/kvm/desktop/gta5@2664                                            0B      -  90.2G  -
    data/kvm/desktop/launchers@2793                                    25.8M      -  3.29G  -
    data/kvm/desktop/launchers@2823                                       0B      -  3.29G  -
    data/kvm/desktop/overwatch@2665                                    2.62M      -  24.2G  -
    data/kvm/desktop/overwatch@2680                                       0B      -  24.2G  -
    data/kvm/desktop/pubg@2066                                         1.59G      -  28.5G  -
    data/kvm/desktop/pubg@2775                                            0B      -  28.9G  -
    data/kvm/desktop/rdr2@125                                          3.58G      -   117G  -
    data/kvm/desktop/rdr2@592                                             0B      -   117G  -
    data/kvm/desktop/tarkov@1373                                          0B      -  17.9G  -
    data/kvm/desktop/thestore@2070                                     1.74G      -  1.74G  -
    data/kvm/desktop/thestore@2084                                        0B      -  13.1G  -
    data/kvm/desktop/twwarhammer2@400                                  56.0G      -  56.2G  -
    data/kvm/desktop/twwarhammer2@2227                                    0B      -  57.5G  -
    data/kvm/desktop/windows@139                                       7.83G      -  36.8G  -
    data/kvm/desktop/windows@231                                        966M      -  36.8G  -
    data/kvm/desktop/windows@270                                          0B      -  36.8G  -
    data/kvm/desktop/windows-vm1-270@d35b669fefa7f4255adaa804abf6895d    16K      -  36.8G  -
    data/kvm/desktop/witcher3@230                                         0B      -  55.6G  -
    data/kvm/desktop/wow@2681                                           203M      -  73.9G  -
    data/kvm/desktop/wow@2801                                             0B      -  74.0G  -

Данные выводятся в формате <dataset>@<snapshot>, т.е. :bash:`data/kvm/desktop/rdr2@125` означает датасет с именем **data/kvm/desktop/rdr2**, снимок **125**. Как можно заметить, снимков несколько, т.к. игры периодически обновляются. Нас интересуют только последние снимки.

Очень полезным будет установить утилиту **pv**, которая позволит ограничить скорость передачи данных с хоста. Это необходимо, если Вы планируете копировать игры с хоста, на котором в данный момент играют пользователи.

.. code-block:: bash

    yum -y install pv

В первую очередь нужно передать на новый хост данные системного диска виртуальной машины. Имя датасета - **data/kvm/desktop/windows**
Определите имя последнего снимка этого датасета, в примере это 270. Так же, для первоначального запуска понадобится датасет **data/kvm/desktop/launchers** и **data/kvm/desktop/gta5**

Передача осуществляется командой :bash:`zfs send -v <dataset@snapshot> | pv -L <максимальная скорость> | ssh <IP address> zfs recv <dataset>`
Например, для того чтобы скопировать системный диск виртуальной машины с ограничением максимальной скорости 50МБайт/сек на хост с адресом 192.168.50.10:

.. code-block:: bash

    zfs send -v data/kvm/desktop/windows@270 | pv -L 50M | ssh 192.168.50.10 zfs recv data/kvm/desktop/windows

Точно таким же образом необходимо скопировать нужные игры:

.. code-block:: bash

    zfs send -v data/kvm/desktop/csgo@1182 | pv -L 50M | ssh 192.168.50.10 zfs recv data/kvm/desktop/csgo

Настройка сети
==============

Для работы GameServer необходимо чтобы Ваш роутер поддерживал технологию UPnP, т.к. GameServer открывает необходимые порты автоматически.
Настройка UPnP выходит за рамки данного руководства и я советую обратиться к документации Вашего роутера. Обычно, настройка UPnP достаточно проста.
Сложности могут быть, если Ваш компьютер подключен к роутеру не напрямую, а через управляемый коммутатор. Дело в том, что на управляемых коммутаторах, зачастую, Multicast-трафик заблокирован. В этом случае, опять таки обратитесь к документации по настройке Вашего сетевого обрудования.

Установка GameServer
********************

**Дистрибутив GameServer не распространяется открыто!** Вам необходимо зарегистрироваться как участник PlayKey Pro и получить официальный образ!

После получения официального образа (это файл с расширением .img) откройте его при помощи *7-zip*. В корне архива найдите скрипт с именем *startup.py* и откройте его в любом текстовом редакторе.
Найдите функцию **Image** и посмотрите значение переменной *url*. По этой ссылке находится непосредственно сам образ системы. Скачайте его, запишите на USB-флэшку и подключите ее к компьютеру, на котором Вы настраивете PlayKey Pro.

Создайте каталог командой :bash:`mkdir /mnt/playkey`

Дайте команду :bash:`fdisk -l` и найдите имя устройства и раздела на флэшке.
Пример вывода команды:

.. image:: /images/pk-usb-flash.png

В данном случае, флэшка определилась как устройство */dev/sda*, нужный нам раздел - */dev/sda3*

Смонтируйте раздел в директорию, которую создали ранее:

.. code-block:: bash

    mount /dev/sda3 /mnt/playkey

Скопируйте файл */mnt/playkey/usr/local/etc/gameserver/template.xml* в папку */root*

Просмотрите содержимое файла */mnt/playkey/usr/local/bin/updater_main.sh*. В конце файла вы увидите ссылку. Откройте любой браузер и вставьте в адресную строку эту ссылку и допишите к ней знак вопроса и *software=GameServer*. На открывшейся странице посмотрите значения параметров url, filename и version. Скомпонуйте это в одну строку вида url/version/filename и вставьте ее адресную строку новой вкладки браузера и у Вас начнется скачивание установочного файла GameServer.

Скопируйте файл, который Вы скачали в домашнюю папку пользователя root - **/root** и выполните следующую команду:

.. code-block:: bash

    yum -y install /root/<имяфайла>

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

Обратите внимание на параметры **UserID**, **TemplateFile** и раздел **VmAutoconf**. Первый параметр - это Ваш идентификатор в PlayKey и посмотреть его значение можно в личном кабинете по адресу https://playkey.net/en/account. Второй параметр - это путь к шаблону виртуальной машины. Если у Вас компьютер с процессором AMD, то необходимо это значение изменить на :bash:`/usr/local/etc/gameserver/template_amd.xml`, этот шаблон доступен после установки GameServer. В случае с процессором Intel, используйте файл *template.xml*, который Вы скопировали из официального образа.

Теперь оцените ресурсы Вашего компьютера для запуска игр. Количество одновременно запускаемых игр ограничено тремя параметрами - количество дискретных видеокарт (видеокарта встроенная в процессор или материнскую плату не учитывается), количество ядер и количество оперативной памяти. Минимальные требования для виртуальной машины - 4 ядра, 8ГБ оперативной памяти и отдельная видеокарта. Таким образом, если у вас всего одна дискретная видеокарта, Вы сможете запускать всего одну виртуальную машину. Что касается оперативной памяти, то 8ГБ на одну виртуальную машину - это необходимый минимум, но некоторые игры требуют значительно большего объема. Например, Red Dead Redemption 2 требует 16Гб. Также, не забывайте про ресурсы потребляемые непосредственно операционной системой, в которой работает виртуальная машина. Стабильная работа обеспечивается на 6ГБ. Перейдем к процессорным ядрам. Большинство игр потребуют 4 ядра, Red Dead Redemption 2 и Warzone - по 6 ядер. Два ядра необходимо операционной системе. 
Предположим, что Ваша система имеет следущую конфигурацию - 12 физических ядер/24 логических , 32ГБ оперативной памяти и 2 видеокарты. Вы сможете запустить 2 виртуальных машины (ограничение - количество видеокарт), каждую с (32-6)/2=13ГБ оперативной памяти. 

Запуск GameServer
*****************

После внесения необходимых изменений в конфигурационные файлы необходимо включить и запустить GameServer.

.. code-block:: bash

    systemctl enable gameserver --now

Скорее всего, Ваш компьютер сразу же перезагрузится, т.к. GameServer вносит некоторые изменения в конфигурацию системы.

После перезагрузки необходимо подождать 2-3 минуты, возможно дольше и проверить роутер, открылись ли порты для GameServer. После этого нужно посмотреть, начался ли процесс загрузки данных для виртуальных машин.

.. code-block:: bash

    journalctl -fn1000 -tgameserver/downloader




