# Documentation technique

## Installation de la solution

### Serveur

Voici les étapes à suivre pour installer la solution sur votre serveur.

#### Installation des prérequis : 

Python & pip : 

```
$ dnf install python3
$ apt install python-pip
```

Pygame : 

```
$ pip install pygame
```

#### Mise en place du firewall : 

Tout d'abord, on réinitialise le firewall :

```
iptables -F
```
Autoriser le trafic local :
```
iptables -I INPUT -i lo -j ACCEPT
```
On autorise les ports nécessaires à notre configuration serveur :
```
iptables -A INPUT -i eth0 -p tcp --dport 1234 -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 12121 -j ACCEPT
```
On autorise les pings entrants :
```
iptables -A INPUT -p icmp -j ACCEPT
```
Autoriser les connexions déjà établies :
```
iptables -A INPUT -i eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
```
Enfin, on bloque tout le reste :
```
iptables -A INPUT -i eth0 -j DROP
```
#### Installation des fichiers de jeu sur le serveur : 

Afin d'effectuer des vérifications sur les mouvements des joueurs, le serveur à besoin des mêmes scripts présents sur le client.

Il vous faudra donc cloner le repo, et installer les fichiers sur le serveur.

Lien du repo : https://github.com/ItsGibbs/ProjetFinalUX-PERRIN-BERTIN

#### Mise en place d'un service pour le serveur

Afin que le serveur reste opérationnel et se redémarre automatiquement en cas de problème, ce service doit être créé. Il est également disponible sur le repo, il vous suffit de le transférer dans `/etc/systemd/system/`
```
[Unit]
Description=server service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=on-failure
RestartSec=10
User=sacha
ExecStart=/bin/sh -c "/usr/bin/python3 /home/sacha/checkers/server.py"
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```

Une fois le service créé : 

```
$ sudo systemctl start server.service
$ sudo systemctl enable server.service
```

## Accéder à la solution

#### Installation des prérequis : 

Python & pip 

##### Windows : 
https://www.python.org/downloads/

##### Linux : 
```
$ dnf install python3
$ apt install python-pip
```

Pygame : 

```
$ pip install pygame
```

#### Installation des fichiers de jeu sur le client : 

Pour accéder à la solution, clonez le repo sur votre machine locale. (https://github.com/ItsGibbs/ProjetFinalUX-PERRIN-BERTIN)

## Jouer
Pour jouer au jeu, accédez à l'emplacement du dossier grâce à la commande `cd`, ici par exemple : 

```
C:\> cd .\Users\Admin\Repo
C:\Users\Admin\Repo>
```
D'ici vous pourrez lancer l'application avec la commande : 
```
$ python3 main.py
```

Le jeu est lancé ! Il ne vous reste plus qu'à jouer !