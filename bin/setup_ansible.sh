#!/usr/bin/env bash
#title           :setup_ansible.sh
#description     :Install ansible and local station
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210901
#version         :0.6    
#usage		     :bash setup_ansible.sh
#notes           :
#bash_version    :4.3.48(1)-release
#==============================================================================

clear
echo "CONFIGURACIÒN DE LA PLATAFORMA - MAZINGER-D CORE SETUP     "
echo "==========================================================="
echo "Instalación de Ansible para Estación de Desarrollo"
echo ""
# Install pip if python installed
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
python3 -m pip install --user ansible
python3 -m pip install --user paramiko
rm get-pip.py

