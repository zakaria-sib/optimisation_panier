"""
Optimisation du panier alimentaire étudiant — résolution par programmation linéaire.

Minimiser le coût hebdomadaire d'un panier composé de riz et de poulet
en respectant des contraintes nutritionnelles minimales.
"""

from pulp import (
    LpProblem,
    LpVariable,
    LpMinimize,
    PULP_CBC_CMD,
    LpStatus,
    value,
)


def construire_probleme(
    prix_riz: float = 2.0,
    prix_poulet: float = 10.0,
    energie_min: float = 14000.0,
    proteines_min: float = 500.0,
    poulet_min: float = 1.0,
) -> LpProblem:
    """
    Construit et renvoie le problème PL sans le résoudre.

    Paramètres
    ----------
    prix_riz       : coût du riz en €/kg
    prix_poulet    : coût du poulet en €/kg
    energie_min    : apport énergétique minimal en kcal/semaine
    proteines_min  : apport protéique minimal en g/semaine
    poulet_min     : quantité minimale de poulet en kg/semaine
    """
    prob = LpProblem("Optimisation_Panier_Alimentaire", LpMinimize)

    # Variables de décision (non-négatives par défaut dans PuLP)
    x_riz = LpVariable("x_riz", lowBound=0)
    x_poulet = LpVariable("x_poulet", lowBound=0)

    # Fonction objectif : minimiser le coût total
    prob += prix_riz * x_riz + prix_poulet * x_poulet, "Coût_total"

    # Contrainte 1 — apport énergétique (kcal/semaine)
    prob += 1300 * x_riz + 1650 * x_poulet >= energie_min, "Energie"

    # Contrainte 2 — apport protéique (g/semaine)
    prob += 70 * x_riz + 310 * x_poulet >= proteines_min, "Proteines"

    # Contrainte 3 — quantité minimale de poulet (kg/semaine)
    prob += x_poulet >= poulet_min, "Poulet_minimum"

    return prob, x_riz, x_poulet


def resoudre_et_afficher() -> None:
    """Résout le problème et affiche les résultats dans le terminal."""

    SEPARATEUR = "=" * 60

    print(f"\n{SEPARATEUR}")
    print("  🥗  OPTIMISATION DU PANIER ALIMENTAIRE ÉTUDIANT")
    print(f"{SEPARATEUR}\n")

    # ── Construction du problème ──────────────────────────────────
    prob, x_riz, x_poulet = construire_probleme()

    print("📋 Formulation du problème :")
    print(f"   Minimiser  Z = 2.00·x_riz + 10.00·x_poulet")
    print(f"   Sous contraintes :")
    print(f"     Énergie    : 1300·x_riz + 1650·x_poulet ≥ 14 000 kcal/sem")
    print(f"     Protéines  :   70·x_riz +  310·x_poulet ≥    500 g/sem")
    print(f"     Poulet min :                 x_poulet   ≥      1 kg/sem")
    print(f"     Non-négativité : x_riz, x_poulet ≥ 0\n")

    # ── Résolution ───────────────────────────────────────────────
    print("⚙️  Résolution avec CBC (PULP_CBC_CMD)…")
    prob.solve(PULP_CBC_CMD(msg=False))

    statut = LpStatus[prob.status]
    print(f"   Statut : {statut}\n")

    if prob.status != 1:
        print("❌ Aucune solution optimale trouvée.")
        return

    # ── Résultats ────────────────────────────────────────────────
    riz_opt    = value(x_riz)
    poulet_opt = value(x_poulet)
    cout_opt   = value(prob.objective)

    print(f"{SEPARATEUR}")
    print("  ✅  SOLUTION OPTIMALE")
    print(f"{SEPARATEUR}")
    print(f"   🍚 Riz        : {riz_opt:.4f} kg/semaine")
    print(f"   🐔 Poulet     : {poulet_opt:.4f} kg/semaine")
    print(f"   💰 Coût total : {cout_opt:.2f} €/semaine\n")

    # ── Vérification des contraintes ─────────────────────────────
    energie_reel   = 1300 * riz_opt + 1650 * poulet_opt
    proteines_reel = 70   * riz_opt +  310 * poulet_opt

    print(f"{SEPARATEUR}")
    print("  📊  VÉRIFICATION DES CONTRAINTES")
    print(f"{SEPARATEUR}")

    def statut_contrainte(valeur: float, limite: float, sens: str = ">=") -> str:
        ok = valeur >= limite if sens == ">=" else valeur <= limite
        return "✅ OK" if ok else "❌ VIOLÉE"

    print(
        f"   Énergie    : {energie_reel:>10.1f} kcal  "
        f"(min 14 000) {statut_contrainte(energie_reel, 14000)}"
    )
    print(
        f"   Protéines  : {proteines_reel:>10.1f} g     "
        f"(min    500) {statut_contrainte(proteines_reel, 500)}"
    )
    print(
        f"   Poulet min : {poulet_opt:>10.4f} kg    "
        f"(min      1) {statut_contrainte(poulet_opt, 1)}"
    )
    print(f"\n{SEPARATEUR}\n")


if __name__ == "__main__":
    resoudre_et_afficher()
