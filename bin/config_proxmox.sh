#!/usr/bin/env bash
#title           :config_proxmox.sh
#description     :Execute task to setup proxmox configuration
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :bash config_proxmox.sh
#notes           :Install ansible to use this script
#bash_version    :4.3.48(1)-release
#==============================================================================

function message_main {
  clear
  echo "CONFIGURACIÒN DE LA PLATAFORMA - VIRTUALIZACIÓN PROXMOX    "
  echo "==========================================================="
  echo "Mediante este proceso vamos a configurar los servidores de "
  echo "virtualización PROXMOX con los que cuenta la plataforma.   "
  echo "Nota: solo es requerido si la plataforma se desplegará en  "
  echo "infraestructura de virtualización PROXMOX administrada."
  echo "los servidores serán enunciados prmx[n].[domainname], donde"
  echo "[n] corresponde a un número etre 0 y 9 y[0] es el          "
  echo "controlador principal."
  echo ""
}

while :; do
  message_main
  read -p "¿ Cuántos servidores de virtualización va a registrar [0-9] ? " number
  [[ $number =~ ^[0-9]+$ ]] || { echo "Entre un número válido.."; continue; }
  if ((number >= 0 && number <= 9)); then
    break
  else
    echo "Número fuera de rango, intente nuevamente"
  fi
done

#echo -e "Become Password: \c"
#read -s PASS
#echo ""
# Run configuration setup playbook
#ansible-playbook -i inventory/base.ini install/setup_configs.yml --extra-vars "ansible_become_pass=$PASS"

