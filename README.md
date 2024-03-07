# Simulation d'Écosystèmes 2

### Description du Projet
Ce projet vise à simuler les interactions dynamiques au sein d'un écosystème impliquant des lapins, des renards, des carottes, et des terriers. Utilisant un modèle de simulation basé sur des règles précises, le système explore comment les populations de ces entités changent en réponse à des facteurs environnementaux et à leurs interactions mutuelles. Les lapins consomment des carottes pour survivre et utilisent des terriers pour se protéger des renards, qui, à leur tour, chassent les lapins comme source de nourriture. Le projet offre un aperçu des concepts écologiques tels que les chaînes alimentaires, la prédation, et la reproduction, tout en fournissant une plateforme pour étudier l'impact des différentes stratégies de survie et de reproduction sur la dynamique des populations au fil du temps.

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
