#!/bin/bash


# Bucle que verifica si hay instancia de python en memoria, si no la hay se eje$
if [ ! "$(pidof python)" ] 
 then
   cd /opt/python
   up=`uptime -p`
   ipaddr=`hostname -I`
   set -x
     if [ -n "$ipaddr" ]; then
      sudo python /opt/python/lcd2.py "$up" $ipaddr
     fi
    else 
     killall python
   cd /
    
fi

