#!/usr/bin/env bash
#title           :setup_stations.sh
#description     :Execute ansible playbook to configuration setup
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210901
#version         :0.6    
#usage		     :bash setup_stations.sh
#notes           :Install ansible to use this script
#bash_version    :4.3.48(1)-release
#==============================================================================

clear
echo "CONFIGURACIÒN DE LA PLATAFORMA - MAZINGER-D CORE SETUP     "
echo "==========================================================="
echo "Configuración/Actualización de Estación de Desarrollo"
echo -e "Become Password: \c"
read -s PASS
echo ""
echo -e "Roles Update (y/n): \c"
read ROLES
# Run configuration setup playbook
ansible-playbook -i inventory/base.ini install/setup_stations.yml -e "ansible_become_password=$PASS ansible_user=$USER"
# Update ansible roles from galaxy
case $ROLES in
  y)
   ansible-playbook -i inventory/base.ini install/update_roles.yml -e "ansible_become_password=$PASS ansible_user=$USER"
esac
