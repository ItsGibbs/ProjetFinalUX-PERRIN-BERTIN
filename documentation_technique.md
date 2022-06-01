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

Ah

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
Restart=always
RestartSec=1
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