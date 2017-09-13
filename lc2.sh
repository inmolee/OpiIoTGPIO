#!/bin/bash


# Bucle que verifica si hay instancia de python en memoria, si no la hay se ejecuta
if [ ! "$(pidof python)" ] 
 then
   cd /opt/python
   echo "No hay inst. en memoria"
   set -x
   #   ipaddr=`ifconfig wlan0 |grep "inet addr" |awk {'print $2'} |cut -f2 -d:`
   ipaddr=`hostname -I`
   if [ -n "$ipaddr" ]; then
   sudo python /opt/python/lcd2.py "My IP" $ipaddr
   fi
   cd /
fi

