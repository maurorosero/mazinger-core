#!/usr/bin/env bash
#title           :setup_developer.sh
#description     :Execute ansible playbook to configuration setup
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210901
#version         :0.6    
#usage		     :bash setup_developer.sh
#notes           :Install ansible to use this script
#bash_version    :4.3.48(1)-release
#==============================================================================

export GIT_USERNAME=`git config user.name`
export GIT_EMAIL=`git config user.email`
export GIT_CHANGE="NO"
change_me="N"
clear
echo "CONFIGURACIÒN DE LA PLATAFORMA - MAZINGER-D CORE SETUP     "
echo "==========================================================="
echo "Configuración de Usuario Desarrollador (DevOPS): $USER"
if [ -z "$GIT_USERNAME" ]
then
  echo -e "\c"
  export GIT_CHANGE="YES"
else
  echo -e "\tNombre Completo:    $GIT_USERNAME"
fi
if [ -z "$GIT_EMAIL" ]
then
  echo -e "\c"
  export GIT_CHANGE="YES"
else
  echo -e "\tCorreo Electrónico: $GIT_EMAIL"
fi
if [ "$GIT_CHANGE" == "NO" ]
then
  echo -e "Desea cambiar los datos (s/n)? \c"
  read CHANGE_ME
fi
# Run configuration setup playbook
if [ "$GIT_CHANGE" == "YES" ]
then
  echo -e "Become AWX Password: \c"
  read -s PASS
  echo ""
  ansible-playbook -i inventory/kvaas.ini install/setup_developer.yml -e "ansible_ssh_password=$PASS ansible_user=root input_developer_user=$USER"
elif [ "$CHANGE_ME" == "s" ]
then
  echo -e "Become AWX Password: \c"
  read -s PASS
  echo ""
  ansible-playbook -i inventory/kvaas.ini install/setup_developer.yml -e "ansible_ssh_password=$PASS ansible_user=root input_developer_user=$USER change_me=1"
fi
