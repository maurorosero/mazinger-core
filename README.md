# ![image](images/mazinger-black-24x24.jpg) MAZINGER CORE (mazinger-core)
###PLATAFORMA DEVOPS PARA DESPLIEGUE AUTOMATIZADO DE INFRAESTRUCTURA

Este proyecto tiene la intención de desarrollar una plataforma automatizada de displiegue de servidores y servicios, de fácil uso utilizando herramientas como: Ansible, Ansible AWX, Terraform, Vagrant Docker, Vault, Boundary, entre otras.

![image](images/mazinger-components.png)

## INFRAESTRUCTURA

Para el Core de la plataforma de despliegue utilizaremos Ansible y Ansible AWX, por lo que necesitaremos instalar algunos servidores o servicios de soporte a la plataforma:

#### DEVELOPER STATION
Es la computadora de desarrollo (estación o servidor) utilizada por el/los desarrolladores de la plataforma. Requiere que el usuario tenga la capacidad de escalar sus privilegios a nivel de superusuario.  Se requiere que al momento de lanzar el proceso de instalación inicial, el usuario se encuentre registrado con su usuario de desarrollo; el mismo será utilizado para configurar las credenciales como desarrollador/propietario de la plataforma o proyecto.

Nota: A la fecha (Ago 12, 2021), solo soportamos como estación de desarrollo Debian 10, Ubuntu 20 o Linux Mint.

#### GIT CONTROLLER SERVER
##### GITLAB CI/CD
Aunque la integración con **GITHUB** nos hubiera ahorrado el despliegue de uno o más servidores para este servicio, preferimos la instalación de un servidor que ofrezca las prestaciones de repositorio de proyectos, control de versiones y de despliegue/integración continua.  Por sus prestaciones de servicio, **GITLAB**, no solo nos sirve de repositorio para la gestión de proyectos; si no que se convierte en uno de los componentes principales de **MAZINGER DEVOPS**.

##### GITHUB SERVICES
Para esta integración se debiera contratar una cuenta comercial del servicio para cubrir la mayoría de las prestaciones de integración con **MAZINGER DEVOPS**. No obstante, en esta etapa inicial no contaremos con integración hacia **GITHUB** como nuestro **GIT CONTROLLER SERVER**.

#### AWX CONTROLLER SERVER
Este es un servidor basado en la versión libre de [RED HAT ANSIBLE AUTOMATION PLATFORM](https://www.ansible.com/products/automation-platform) conocida como [ANSIBLE AWX](https://github.com/ansible/awx) que eleva la automatización en toda su organización, ampliando sus posibilidades. Es una base más segura y flexible para construir e implementar la automatización que ayuda a su negocio a acelerar, orquestar e innovar.  

**AWX** proporciona una interfaz de usuario basada en web, una API REST y un motor de tareas construido sobre Ansible. Es uno de los proyectos iniciales de Red Hat Ansible Automation Platform. Para ambiente de producción (minimo), se requiere una maquina física o virtual con 4 cores/vcores, 8GB RAM y 100GB de almacenamiento.

## INSTALACIÓN

#### CONFIGURANDO PRE-REQUISITOS
Primero debe descargarse el proyecto desde nuestro repositorio en [GITHUB: maurorosero/mazinger-core](https://github.com/maurorosero/mazinger-core). Desde una sesión de consola (preferiblemente ambiente linux) en la computadora que vamos a usar como el **DEVELOPER STATION**, haciendo lo siguiente:

```bash
$ git clone https://github.com/maurorosero/mazinger-core.git
```
Asegurarse de tener python3 instalado en su versión más reciente e instalar/configurar ansible:

Para derivados de Debian (Debian, Ubuntu, Linux Mint, etc):
```bash
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install python3
```
Para CentOS, Redhat, Fedora y derivados
```bash
$ sudo yum update -y
$ sudo yum install python3
```
Ahora, es el momento de instalar la versión más reciente de ansible
```bash
$ bin/setup_ansible.sh
```
Debes configurar la variable de ambiente DS_ROOT_FORWARD, para indicar a donde se redirigiran los correos de root, donde **root_forward** corresponde a la dirección de correo electrónico para el redireccionamiento **(ejemplo: user@example.com)**
```bash
$ export DS_ROOT_FORWARD='root_forward'
```
Una vez completado el paso anterior, debemos instalar las aplicaciones y librerias requeridas para el ambiente de desarrollo
```bash
$ bin/setup_stations.sh
```
Este proceso debe ser ejecutado antes de hacer cualquier otra cosa; ya que el mismo configura las variables necesarios que servirán de insumo a las demás tareas. Previo, se deben configurar los parametros generales y los archivos de inventario, ejecutando:
```bash
$ bin/setup_configs.sh
```
#### INSTALANDO EL GIT CONTROLLER (GITLAB)
El **AWX CONTROLLER** requiere de un repositorio de proyectos git para gestionar los cambios de proyectos y funcionalidades ansible. Debemos instalar el servidor git (GITLAB) ejecutando el siguiente script:
```
$ bin/setup_gitlab.sh
```
Ahora vamos a cambiar la configuración del repositorio del proyecto y configurarlo para que sea el GITLAB SERVER sea el repositorio principal (debe cambiar **company** y **devops@mycompany.com** por los definidos en su configuración:
```bash
$ git config --local user.name "sysop ([company])"
$ git config --local user.email "[devops@mycompany.com]"
$ git remote -v
```
Esto nos mostrará la lista de los repositorios configurados, a este punto solo deberíamos tener configurado el **origin** apuntando al repositorio original de github, para removerlo hacemos lo siguiente:
```bash
$ git remote remove origin
```
A este punto no deberíamos tener ningun repositorio configurado, para confirmarlo ejecutamos nuevamente:
```bash
$ git remote -v
```
Si todo va bien, debería aparecenerno el resultado en blanco. Ahora vamos a configurar el nuevo repositorio (reemplazar git-server-url por la url del git server en su configuración):
```bash
$ git remote add origin git@[git-server-url]:devops/mazinger-core.git
```
A este punto debemos poder hacer el push inical al proyecto, ejecutando:
```bash
$ push --set-upstream origin core
```
Si todo está debidamente instalado y configurado a este punto debe tener el proyecto base cargado en el GITLAB SERVER. Solo se cargará el proyecto base, ya que el archivo **.gitignore** impide que se carguen las configuraciones generadas: por lo cual deberemos borrar o mover el archivo **.gitignore** a otra carpeta como sigue:
```bash
$ mv .gitignore defaults/gitignore.cnf
```
Volvemos a actualizar nuestro proyecto al repositorio en el gitlab server.  Esta vez, incorporará las configuraciones generadas.
```bash 
$ git add .
$ git commit -m "[CORE]New mazinger company installation"
$ git push
```
#### CONFIGURANDO EL PERFIL DE USUARIO DEVOPS
Antes de empezar a trabajar debemos crear las credenciales como usuario devops de la plataforma. Este proceso usará la configuración de usuario de la sesión qu esta conectada en la **DEVELOPER STATION**.  Si este no es el usuario que se definirá como **USUARIO DEVOPS**, terminé la sesión y registrese como el usuario correspondiente.
```
$ bin/setup_developer.sh
```
#### CARGANDO EL PROYECTO MAZINGER DEVOPS AL GIT SERVER

#### INSTALANDO AWX CONTROLLER
Ahora vamos a instalar nuestro servidor de orquestación y controlador principal, que nos proveerá un interface gráfico y centralizdo para la gestión de nuestros procesos de autoatización, haciendo lo siguiente:
```bash
$ bin/setup_awx.sh
```
