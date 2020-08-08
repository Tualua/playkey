
    mkdir /etc/aria2
    mkdir /var/aria2
    mkdir /var/log/aria2
    mkdir -p /data/nginx/downloads
    
    wget -O /etc/aria2/aria2.conf
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2-hook-move.sh -O /usr/local/bin/aria2-hook-move.sh
    
    chown nginx:nginx /usr/local/bin/aria2-hook-move.sh
    chmod +x /usr/local/bin/aria2-hook-move.sh
    
    
