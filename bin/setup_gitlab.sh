#!/usr/bin/env bash
#title           :setup_gitlab.sh
#description     :Execute ansible playbook to configuration setup
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210901
#version         :0.6    
#usage		     :bash setup_gitlab.sh
#notes           :Install ansible to use this script
#bash_version    :4.3.48(1)-release
#==============================================================================

clear
echo "CONFIGURACIÒN DE LA PLATAFORMA - MAZINGER-D CORE SETUP     "
echo "==========================================================="
echo "Instalación y configuración deL Git Server (Gitlab)"
echo -e "Become Gitlab Password: \c"
read -s PASS
echo ""
# Remote server python installation if required
echo -e "Remote Python (y/n): \c"
read RPYTHON
case $RPYTHON in
  y)
   ansible-playbook -i inventory/kvaas.ini -l git install/bootstrap.yml -e "ansible_password=$PASS ansible_user=root"
esac
# Run configuration setup playbook
ansible-playbook -i inventory/kvaas.ini -l git install/git_install.yml -e "ansible_password=$PASS ansible_user=root"

