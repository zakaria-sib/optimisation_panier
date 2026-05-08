# 🍚🐔 Optimisation du Panier Alimentaire Étudiant

Projet de **Programmation Linéaire** développé dans le cadre du cours de
Recherche Opérationnelle à l'**EMSI**.

L'objectif est de minimiser le coût hebdomadaire d'un panier alimentaire
composé de riz et de poulet tout en respectant des contraintes nutritionnelles
minimales (calories et protéines).

---

## 📦 Structure du projet

```
optimisation-panier/
├── README.md
├── requirements.txt
├── .gitignore
├── solver_pulp.py        # Script console (résolution + affichage terminal)
├── streamlit_app.py      # Application web interactive
└── docs/
    └── modele_mathematique.md
```

---

## ⚙️ Installation

### 1. Cloner / télécharger le projet

```bash
git clone <url-du-repo>
cd optimisation-panier
```

### 2. Créer un environnement virtuel

```bash
# Créer l'environnement
python -m venv .venv

# Activer (Linux / macOS)
source .venv/bin/activate

# Activer (Windows PowerShell)
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### Version console

```bash
python solver_pulp.py
```

Affiche dans le terminal la formulation du problème, la solution optimale
et la vérification de chaque contrainte.

### Application web Streamlit

```bash
streamlit run streamlit_app.py
```

Ouvre automatiquement le navigateur sur `http://localhost:8501`.
L'interface permet de modifier les prix et les seuils nutritionnels en
temps réel et d'afficher la solution ainsi que le graphique de la région
réalisable.

---

## 📐 Modèle mathématique

**Variables de décision**

| Variable    | Description                  |
|-------------|------------------------------|
| `x_riz`     | Quantité de riz (kg/semaine) |
| `x_poulet`  | Quantité de poulet (kg/sem)  |

**Fonction objectif** (minimisation du coût) :

```
Min Z = 2,00·x_riz + 10,00·x_poulet
```

**Contraintes** :

| Contrainte      | Inégalité                                  |
|-----------------|--------------------------------------------|
| Énergie         | 1300·x_riz + 1650·x_poulet ≥ 14 000 kcal  |
| Protéines       |   70·x_riz +  310·x_poulet ≥    500 g     |
| Poulet minimum  |                  x_poulet  ≥      1 kg    |
| Non-négativité  | x_riz, x_poulet ≥ 0                        |

---

## ✅ Résultats attendus

| Grandeur        | Valeur        |
|-----------------|---------------|
| x_riz           | **9,5 kg**    |
| x_poulet        | **1,0 kg**    |
| Coût optimal Z* | **29,00 €**   |

---

## 🛠️ Technologies

- [PuLP](https://coin-or.github.io/pulp/) — modélisation et résolution LP (solveur CBC)
- [Streamlit](https://streamlit.io/) — interface web interactive
- [Matplotlib](https://matplotlib.org/) — visualisation graphique
- [Pandas](https://pandas.pydata.org/) — tableaux de données
- [NumPy](https://numpy.org/) — calcul numérique

---

## 📄 Licence

Projet pédagogique — EMSI 2025-2026.
