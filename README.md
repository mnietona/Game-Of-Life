# Simulation d'Écosystèmes 2

### Description du Projet
Ce projet consiste à créer une simulation interactive d'écosystèmes 2D, intégrant des éléments tels que la faune et flore.

## Prérequis

- Python 3.x
- [Poetry](https://python-poetry.org/)

## Installation

### Installer Poetry

- **Sur Windows** : Ouvrez PowerShell ou votre terminal de commande et exécutez :

  ```shell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```

- **Sur MacOS/Linux** : Ouvrez un terminal et exécutez :

  ```shell
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### Configurer le Projet

Clonez le dépôt Git :

```shell
git clone https://github.com/mnietona/Projet_3.git && cd Projet_3
```

Installez les dépendances du projet avec Poetry :

```shell
poetry install
```

## Utilisation

### Activer l'Environnement Virtuel

Pour activer l'environnement virtuel géré par Poetry :

```shell
poetry shell
```

Cela permet d'exécuter des commandes Python dans l'environnement virtuel spécifique à ce projet.


### Lancer le Projet

Pour exécuter le projet, utilisez la commande suivante :

```shell
make
```
