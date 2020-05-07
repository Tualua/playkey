
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

Выберите *Install CentOS7*

На экране выбора языков выберите любой подходящий Вам язык и нажмите кнопку продолжения (Continue). Здесь и далее все снимки экрана будутс сделаны с англоязычного установщика.

.. image:: /images/install-language-sel.png


Разметка диска
==============
Стандартная разметка LVM, предлагаемая установщиком не подойдет, поэтому ее необходимо изменить. 
На экране Installation Summary выберите пункт INSTALLATION DESTINATION

.. image:: /images/install-summary.png

Проверьте, что на этом экране Вы выделили нужный диск. ВНИМАНИЕ! Дальнейшие шаги приведут к БЕЗВОЗВРАТНОМУ УНИЧТОЖЕНИЮ ВСЕХ ДАННЫХ НА ВЫБРАННОМ ДИСКЕ!
Так же необходимо в разделе Other Storage Options выбрать пункт I will configure partitioning, после чего нужно нажать Done.

.. image:: /images/install-dev-sel.png

Если на выбранном диске уже есть разделы от предыдущих установок, необходимо их удалить кнопкой -.
В пункте New mount points will use the following partitioning scheme выберите Standard Partitioning и нажмите Click here to create them automatically

.. image:: /images/install-part-step1.png

У Вас должная появится такая таблица разделов. В случае, если установщик создал отдельный раздел /home, его нужно удалить, а раздел / удалить и затем заново создать.
Для создания раздела возпользуйтесь кнопкой +. Обязательно проверьте, что разделы / и /boot созданы с файловой системой XFS.

.. image:: /images/install-part-step2.png

После окончания операций по разметке диска нажмите Done и подтвердите изменения кнопкой Accept Changes. 

.. image:: /images/install-part-accept.png

Возвращаемся на экран INSTALLATION SUMMARY. В раздеде DATE & TIME выставьте нужный часовой пояс, в разделе LANGUAGE SUPPORT добавьте необходимые языки (необязательно).
После этого выберите NETWORK & HOST NAME

.. image:: /images/install-net1.png

В поле  Host name задайте полное доменное имя Вашего компьютера (необязательно) и включите сетевое подключение.

.. image:: /images/install-net1.png

После завершения настройки сети нажмите кнопку Done, что в очередной раз вернет Вас на экран INSTALLATION SUMMARY и в правом нижем углу нажмите Begin Installation

.. image:: /images/install-begin.png









