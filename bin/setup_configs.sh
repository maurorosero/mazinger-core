#!/usr/bin/env bash
#title           :setup_configs.sh
#description     :Execute ansible playbook to configuration setup
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :bash setup_configs.sh
#notes           :Install ansible to use this script
#bash_version    :4.3.48(1)-release
#==============================================================================

clear
echo "CONFIGURACIÒN DE LA PLATAFORMA - MAZINGER-D CORE SETUP     "
echo "==========================================================="
echo "Recopilando parametros de configuración básica"
# Run configuration setup playbook
ansible-playbook -i inventory/base.ini install/setup_configs.yml

