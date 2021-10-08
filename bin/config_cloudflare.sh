#!/usr/bin/env bash
#title           :dns_clouflare.sh
#description     :Execute task to setup cloudflare dns configuration
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :bash dns_cloudflare.sh
#notes           :Install ansible to use this script
#bash_version    :4.3.48(1)-release
#==============================================================================

function message_main {
  clear
  echo "CONFIGURACIÒN DE LA PLATAFORMA - DNS CLOUDFLARE            "
  echo "==========================================================="
  echo ""
}

message_main
read -p "Utilizas el servicio de Cloudflare para gestionar tus DNS (S/N)? " input_ok
if [[ "$input_ok" -eq "S" || "$input_ok" -eq "s" ]]; then
   echo -e "Become Password: \c"
   read -s PASS
   echo ""
   # Run configuration setup playbook
   ansible-playbook -i inventory/base.ini install/setup_cloudflare.yml --extra-vars "ansible_become_pass=$PASS cloudflare_domain=None"
fi

