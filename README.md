# ✦ Palette Generator pour Procreate

Un petit outil Python avec interface graphique pour générer des palettes de couleurs au format `.swatches`, directement importables dans **Procreate**.

![Aperçu de l'interface](assets/palette_generator_preview.png)

---

## À quoi ça sert ?

Tu as des codes couleurs hexadécimaux (ex : `#df265d`) et tu veux les transformer en palette Procreate sans passer par des manipulations fastidieuses ?

Lance l'appli, colle tes codes, donne un nom à ta palette, clique sur **Générer** — c'est tout.

---

## Fonctionnalités

- Interface graphique simple et agréable
- Saisie ou collage de codes hex (avec ou sans `#`)
- Aperçu visuel des couleurs en temps réel
- Génération du fichier `.swatches` en un clic
- Fichiers enregistrés automatiquement dans un dossier `Palettes_finales/`
- Icône personnalisée dans la barre des tâches Windows

---

## Installation

Aucune installation complexe. Il te faut juste **Python** sur ton ordinateur.

1. Télécharge ou clone ce dépôt
2. Place tous les fichiers dans un même dossier
3. Double-clique sur `palette_app.pyw`
4. La fenêtre s'ouvre 🎉

> **Note :** Les bibliothèques utilisées (`tkinter`, `json`, `zipfile`, `os`, `re`, `ctypes`) sont incluses par défaut avec Python. Rien à installer en plus.

---

## Utilisation

1. **Nom de la palette** : tape le nom que tu veux donner à ta palette
2. **Codes couleurs** : colle tes codes hex, un par ligne
3. L'aperçu se met à jour automatiquement
4. Clique sur **✦ Générer la palette ✦**
5. Ton fichier `.swatches` est créé dans le dossier `Palettes_finales/`

Tu n'as plus qu'à l'importer dans Procreate !

---

## Structure du projet

```
📁 ton-dossier/
├── palette_app.py      → le code source complet (logique + interface)
├── palette_app.pyw     → le lanceur sans fenêtre noire (double-clic)
├── favicon.ico         → icône de l'application
├── assets/             → images du projet (screenshots)
└── Palettes_finales/   → dossier créé automatiquement à la première génération
```

---

## Crédits

Ce projet est basé sur le travail original de [M4nw3l](https://github.com/M4nw3l/PyProcreatePalette), distribué sous licence MIT.

L'adaptation Windows et l'interface graphique ont été développées par [Kaellyana](https://github.com/kaellyana), avec l'aide de [Claude](https://claude.ai) (Anthropic).

---

## Licence

MIT — libre d'utilisation, de modification et de redistribution avec mention des auteurs originaux.
