
    yum -y install nginx-module-njs
    
    mkdir /etc/aria2
    mkdir /var/aria2
    mkdir /var/log/aria2
    mkdir /etc/nginx/js
    mkdir -p /data/nginx/downloads
    
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2.conf -O /etc/aria2/aria2.conf
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2-hook-move.sh -O /usr/local/bin/aria2-hook-move.sh
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2.js -O /etc/nginx/js/aria2.js
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/pk.conf -O /etc/nginx/conf.d/pk.conf
    wget https://raw.githubusercontent.com/Tualua/playkey/master/aria2/aria2.service -O /lib/systemd/system/aria2.service
    
    chown nginx:nginx /usr/local/bin/aria2-hook-move.sh
    chmod +x /usr/local/bin/aria2-hook-move.sh
    chown nginx:nginx /var/aria2
    chown nginx:nginx /var/log/aria2
    chown -R nginx:nginx /etc/nginx/js
    
    semanage fcontext -a -t httpd_sys_rw_content_t "/data/nginx/downloads(/.*)?"
    chcon -R -t httpd_sys_rw_content_t /data/nginx/downloads
    
    systemctl daemon-reload
    systemctl enable aria2 --now
    
    nginx -t
    systemctl reload nginx
    
  
    
    
    
