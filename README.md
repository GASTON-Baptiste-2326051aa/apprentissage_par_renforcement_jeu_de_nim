# Apprentissage par renforcement — Jeu de Nim

Ce projet propose une **initiation à l’apprentissage par renforcement** à travers une implémentation du **jeu de Nim**, un jeu de stratégie à deux joueurs.  
L’objectif est d’entraîner une **intelligence artificielle** à jouer de manière optimale en apprenant par l’expérience, et un système de récompense et de punition.


## Fonctionnement du jeu de Nim

Le **jeu de Nim** se joue entre deux joueurs qui se relaient pour retirer des objets d’un tas, cela peut être des billes, ou des allumettes. 
À chaque tour, un joueur doit retirer **au moins un** objet d’un **seul tas**.  
Le joueur qui prend **le dernier objet** gagne la partie.

## Exemple
On lance une partie avec **8 allumettes**, chaque joueur peut en récupérer une ou deux. Ce sera la base de notre implémentation.


## Objectif du projet

L’objectif est d’implémenter une **IA qui apprend à jouer** au jeu de Nim via une approche d’**apprentissage par renforcement**, sans connaissance préalable des stratégies gagnantes.

L’agent apprend en jouant **contre lui-même** ou **contre un adversaire** (humain ou autre IA), et améliore progressivement sa stratégie grâce aux récompenses reçues après chaque partie.


## Technologies utilisées
- **Python 3.x**  

## Installation 

### Cloner le dépôt
```bash
https://github.com/<username>/apprentissage_par_renforcement_jeu_de_nim.git
```
### Executer le code
Lancer la partie entre un humain et une machine
```
py game_machine_human.py

```
Lancer la partie entre deux machines
```
py game_machine_machine.py
```

## Auteurs

- [@TAMINE-CYRIL](https://github.com/TAMINE-CYRIL)
- [@GASTON-Baptiste-2326051aa](https://github.com/GASTON-Baptiste-2326051aa)
- [@ALVARES-Titouan-2326003b](https://github.com/ALVARES-Titouan-2326003b)
- [@GRIMAUD-Estelle-2326056aa](https://github.com/GRIMAUD-Estelle-2326056aa)

## Sources
 - [Article de Culture Sciences Physique sur le jeu de Nim](https://culturesciencesphysique.ens-lyon.fr/ressource/IA-Nim-1.xml)
 - [Deuxième partie de l'article de Culture Sciences Physique sur le jeu de Nim](https://culturesciencesphysique.ens-lyon.fr/ressource/IA-Nim-2.xml)
 - [Vidéo explicative du fonctionnement du jeu contre une machine](https://www.youtube.com/watch?v=6Z72UuMYBQs)
