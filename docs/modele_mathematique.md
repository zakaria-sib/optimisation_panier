# 📐 Modèle Mathématique — Optimisation du Panier Alimentaire

## 1. Contexte

Un étudiant souhaite composer son panier alimentaire hebdomadaire avec du **riz**
et du **poulet** au coût le plus bas possible, tout en couvrant ses besoins
énergétiques et protéiques minimaux.

---

## 2. Variables de décision

| Variable   | Signification                           | Unité      |
|------------|-----------------------------------------|------------|
| `x_riz`    | Quantité de riz achetée par semaine     | kg/semaine |
| `x_poulet` | Quantité de poulet achetée par semaine  | kg/semaine |

Ces variables sont **continues** et **non-négatives** (`x ≥ 0`).

---

## 3. Fonction objectif

L'objectif est de **minimiser** le coût total hebdomadaire du panier :

$$\min\; Z = 2{,}00\cdot x_{riz} + 10{,}00\cdot x_{poulet}$$

Où 2,00 €/kg et 10,00 €/kg représentent les prix unitaires du riz et du poulet.

---

## 4. Contraintes

### 4.1 Contrainte énergétique

Un étudiant a besoin d'au moins **14 000 kcal par semaine** (environ 2 000 kcal/jour).

| Aliment | Apport énergétique |
|---------|-------------------|
| Riz     | 1 300 kcal/kg     |
| Poulet  | 1 650 kcal/kg     |

$$1300\,x_{riz} + 1650\,x_{poulet} \geq 14\,000$$

### 4.2 Contrainte protéique

Apport protéique minimal de **500 g de protéines par semaine**.

| Aliment | Apport protéique |
|---------|-----------------|
| Riz     | 70 g/kg         |
| Poulet  | 310 g/kg        |

$$70\,x_{riz} + 310\,x_{poulet} \geq 500$$

### 4.3 Contrainte de diversité alimentaire

Pour assurer un apport protéique de qualité, le régime doit inclure au
minimum **1 kg de poulet par semaine** :

$$x_{poulet} \geq 1$$

### 4.4 Non-négativité

Les quantités achetées ne peuvent pas être négatives :

$$x_{riz} \geq 0, \quad x_{poulet} \geq 0$$

---

## 5. Résolution algébrique par la méthode des sommets (dualité)

### Pourquoi la méthode des sommets (dualité) ?

En programmation linéaire, le **théorème fondamental** garantit que la solution
optimale, si elle existe, se trouve en un **sommet (vertex) de la région
réalisable** (polyèdre convexe). La méthode des sommets (aussi appelée méthode
graphique en 2D ou approche duale) consiste à :

1. **Identifier les hyperplans frontières** (droites en 2D) issus des contraintes.
2. **Calculer les points d'intersection** de ces droites (sommets candidats).
3. **Évaluer la fonction objectif** en chaque sommet réalisable.
4. **Sélectionner** le sommet qui minimise (ou maximise) Z.

Cette méthode exploite la **structure duale** du problème : chaque contrainte
primale correspond à une variable duale (prix fantôme) qui quantifie l'impact
marginal du relâchement de cette contrainte sur Z*. La solution optimale se
situe là où les contraintes actives (saturées) définissent un sommet unique.

### Calcul des sommets candidats

Les droites frontières actives sont :

- **(D1)** : 1300 x_riz + 1650 x_poulet = 14 000
- **(D2)** :   70 x_riz +  310 x_poulet =    500
- **(D3)** :              x_poulet = 1

**Intersection D1 ∩ D3** (candidat principal) :

Poser x_poulet = 1 dans D1 :

$$1300\,x_{riz} + 1650 \times 1 = 14\,000$$
$$1300\,x_{riz} = 12\,350$$
$$x_{riz} = \frac{12\,350}{1\,300} = 9{,}5 \text{ kg}$$

Vérification dans D2 :

$$70 \times 9{,}5 + 310 \times 1 = 665 + 310 = 975 \geq 500 \;\checkmark$$

**Évaluation de Z en ce sommet :**

$$Z = 2{,}00 \times 9{,}5 + 10{,}00 \times 1{,}0 = 19{,}00 + 10{,}00 = \mathbf{29{,}00\,€}$$

### Solution optimale

$$\boxed{x_{riz}^* = 9{,}5\text{ kg},\quad x_{poulet}^* = 1{,}0\text{ kg},\quad Z^* = 29{,}00\text{ €}}$$

---

## 6. Interprétation économique

Le panier optimal est **contraint par l'énergie et le poulet minimum** :
les deux contraintes D1 et D3 sont **actives** (saturées) à l'optimum.
La contrainte protéique D2 est **inactive** (marge de 475 g/sem), ce qui
signifie qu'on pourrait réduire la quantité de poulet si la contrainte
minimale de poulet n'existait pas — mais cela ferait augmenter le riz pour
compenser l'énergie, et le coût resterait identique ou supérieur.

Le **prix fantôme** de la contrainte énergie est positif : chaque kcal
supplémentaire requise augmente légèrement le coût optimal — information
utile pour négocier les normes nutritionnelles.
