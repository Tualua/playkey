
    mkdir /etc/aria2
    mkdir /var/aria2
    mkdir /var/log/aria2
    mkdir -p /data/nginx/downloads
    
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2.conf -O /etc/aria2/aria2.conf
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2-hook-move.sh -O /usr/local/bin/aria2-hook-move.sh
    
    chown nginx:nginx /usr/local/bin/aria2-hook-move.sh
    chmod +x /usr/local/bin/aria2-hook-move.sh
    chown nginx:nginx /var/aria2
    chown nginx:nginx /var/log/aria2
    
     semanage fcontext -a -t httpd_sys_rw_content_t "/data/nginx/downloads(/.*)?"
     chcon -R -t httpd_sys_rw_content_t /data/nginx/downloads
    
    
    
