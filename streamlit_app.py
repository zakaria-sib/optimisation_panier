"""
Application Streamlit — Optimisation du panier alimentaire étudiant.

Interface interactive permettant d'ajuster les paramètres du problème
de programmation linéaire et de visualiser la solution optimale.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st
from pulp import (
    LpProblem,
    LpVariable,
    LpMinimize,
    PULP_CBC_CMD,
    LpStatus,
    value,
)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Optimisation Panier Riz & Poulet",
    page_icon="🍚",
    layout="wide",
)


# ─────────────────────────────────────────────────────────────────────────────
# Fonctions utilitaires
# ─────────────────────────────────────────────────────────────────────────────

def resoudre_pl(
    prix_riz: float,
    prix_poulet: float,
    energie_min: float,
    proteines_min: float,
    poulet_min: float,
) -> dict:
    """
    Construit et résout le problème de programmation linéaire avec PuLP.

    Retourne un dictionnaire contenant le statut, les valeurs optimales
    et les informations de vérification des contraintes.
    """
    prob = LpProblem("Optimisation_Panier", LpMinimize)

    x_riz    = LpVariable("x_riz",    lowBound=0)
    x_poulet = LpVariable("x_poulet", lowBound=0)

    # Fonction objectif
    prob += prix_riz * x_riz + prix_poulet * x_poulet

    # Contraintes
    prob += 1300 * x_riz + 1650 * x_poulet >= energie_min,   "Energie"
    prob +=   70 * x_riz +  310 * x_poulet >= proteines_min, "Proteines"
    prob += x_poulet >= poulet_min,                           "Poulet_min"

    prob.solve(PULP_CBC_CMD(msg=False))

    statut = LpStatus[prob.status]

    if prob.status != 1:
        return {"statut": statut, "optimal": False}

    riz_opt    = value(x_riz)
    poulet_opt = value(x_poulet)
    cout_opt   = value(prob.objective)

    energie_reel   = 1300 * riz_opt + 1650 * poulet_opt
    proteines_reel =   70 * riz_opt +  310 * poulet_opt

    return {
        "statut":         statut,
        "optimal":        True,
        "x_riz":          riz_opt,
        "x_poulet":       poulet_opt,
        "cout":           cout_opt,
        "energie_reel":   energie_reel,
        "proteines_reel": proteines_reel,
        "energie_min":    energie_min,
        "proteines_min":  proteines_min,
        "poulet_min":     poulet_min,
    }


def creer_graphique(res: dict) -> plt.Figure:
    """
    Génère le graphique de la région réalisable et du point optimal.

    Affiche les trois droites frontières des contraintes, l'ombre de la
    région réalisable et l'étoile rouge du point optimal.
    """
    x_max = max(res["x_riz"] * 1.6, 15.0)
    y_max = max(res["x_poulet"] * 3.0, 6.0)

    x = np.linspace(0, x_max, 800)

    fig, ax = plt.subplots(figsize=(8, 6))

    # ── Droites frontières ────────────────────────────────────────
    energie_min   = res["energie_min"]
    proteines_min = res["proteines_min"]
    poulet_min    = res["poulet_min"]

    # Contrainte Énergie : 1300x + 1650y = energie_min  →  y = (energie_min - 1300x)/1650
    y_energie = (energie_min - 1300 * x) / 1650
    ax.plot(x, y_energie, color="steelblue",  lw=2, label="Énergie (≥ {:,.0f} kcal)".format(energie_min))

    # Contrainte Protéines : 70x + 310y = proteines_min  →  y = (proteines_min - 70x)/310
    y_proteines = (proteines_min - 70 * x) / 310
    ax.plot(x, y_proteines, color="seagreen", lw=2, label="Protéines (≥ {:,.0f} g)".format(proteines_min))

    # Contrainte Poulet minimum
    ax.axhline(y=poulet_min, color="darkorange", lw=2, linestyle="--",
               label=f"Poulet min (≥ {poulet_min} kg)")

    # ── Région réalisable (ombrage) ───────────────────────────────
    X, Y = np.meshgrid(np.linspace(0, x_max, 400), np.linspace(0, y_max, 400))

    faisable = (
        (1300 * X + 1650 * Y >= energie_min) &
        (70   * X +  310 * Y >= proteines_min) &
        (Y >= poulet_min) &
        (X >= 0) & (Y >= 0)
    )
    ax.contourf(X, Y, faisable.astype(float), levels=[0.5, 1.5],
                colors=["lightblue"], alpha=0.4)

    region_patch = mpatches.Patch(color="lightblue", alpha=0.6, label="Région réalisable")

    # ── Point optimal ─────────────────────────────────────────────
    ax.plot(res["x_riz"], res["x_poulet"], "r*", markersize=18, zorder=5,
            label=f"Optimal ({res['x_riz']:.2f} kg, {res['x_poulet']:.2f} kg)")
    ax.annotate(
        f"  Z* = {res['cout']:.2f} €",
        xy=(res["x_riz"], res["x_poulet"]),
        fontsize=11,
        color="darkred",
        fontweight="bold",
    )

    # ── Mise en forme ─────────────────────────────────────────────
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_xlabel("x_riz (kg/semaine)", fontsize=12)
    ax.set_ylabel("x_poulet (kg/semaine)", fontsize=12)
    ax.set_title("Région réalisable et solution optimale", fontsize=13, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.5)

    handles, labels = ax.get_legend_handles_labels()
    handles.append(region_patch)
    labels.append("Région réalisable")
    ax.legend(handles, labels, loc="upper right", fontsize=9)

    fig.tight_layout()
    return fig


def creer_tableau_verification(res: dict) -> pd.DataFrame:
    """Construit le DataFrame de vérification des contraintes."""
    data = {
        "Contrainte": ["Énergie (kcal)", "Protéines (g)", "Poulet min (kg)"],
        "Valeur réelle": [
            f"{res['energie_reel']:.1f}",
            f"{res['proteines_reel']:.1f}",
            f"{res['x_poulet']:.4f}",
        ],
        "Limite min": [
            f"{res['energie_min']:.0f}",
            f"{res['proteines_min']:.0f}",
            f"{res['poulet_min']:.1f}",
        ],
        "Statut": [
            "✅ Respectée" if res["energie_reel"]   >= res["energie_min"]   else "❌ Violée",
            "✅ Respectée" if res["proteines_reel"] >= res["proteines_min"] else "❌ Violée",
            "✅ Respectée" if res["x_poulet"]       >= res["poulet_min"]    else "❌ Violée",
        ],
    }
    return pd.DataFrame(data)


# ─────────────────────────────────────────────────────────────────────────────
# En-tête principal
# ─────────────────────────────────────────────────────────────────────────────
st.title("🍚🐔 Optimisation du Panier Alimentaire")
st.markdown("**Projet EMSI — Programmation Linéaire avec PuLP**")
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Barre latérale — paramètres éditables
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Paramètres du problème")

    st.subheader("💰 Prix (€/kg)")
    prix_riz    = st.number_input("Prix du riz (€/kg)",    min_value=0.1, max_value=50.0,
                                   value=2.0,  step=0.1, format="%.2f")
    prix_poulet = st.number_input("Prix du poulet (€/kg)", min_value=0.1, max_value=100.0,
                                   value=10.0, step=0.5, format="%.2f")

    st.subheader("🎯 Contraintes nutritionnelles")
    energie_min   = st.number_input("Énergie minimale (kcal/sem)", min_value=1000, max_value=50000,
                                     value=14000, step=500)
    proteines_min = st.number_input("Protéines minimales (g/sem)", min_value=50,   max_value=2000,
                                     value=500,   step=10)
    poulet_min    = st.number_input("Poulet minimum (kg/sem)",      min_value=0.0,  max_value=10.0,
                                     value=1.0,   step=0.1, format="%.1f")

    st.divider()
    st.caption("Les paramètres modifient le modèle en temps réel.")

# ─────────────────────────────────────────────────────────────────────────────
# Corps principal — modèle mathématique + données nutritionnelles
# ─────────────────────────────────────────────────────────────────────────────
col_modele, col_donnees = st.columns(2)

with col_modele:
    st.markdown("### 📐 Modèle mathématique")

    st.markdown("**Minimiser :**")
    st.latex(r"Z = " + f"{prix_riz:.2f}" + r"\, x_{riz} + " + f"{prix_poulet:.2f}" + r"\, x_{poulet}")

    st.markdown("**Sous les contraintes :**")
    st.latex(r"1300\, x_{riz} + 1650\, x_{poulet} \geq " + f"{energie_min}" + r"\quad \text{(énergie, kcal/sem)}")
    st.latex(r"70\, x_{riz} + 310\, x_{poulet} \geq " + f"{proteines_min}" + r"\quad \text{(protéines, g/sem)}")
    st.latex(r"x_{poulet} \geq " + f"{poulet_min}" + r"\quad \text{(poulet minimum, kg/sem)}")
    st.latex(r"x_{riz},\; x_{poulet} \geq 0")

with col_donnees:
    st.subheader("🥗 Données nutritionnelles")
    df_nutrition = pd.DataFrame(
        {
            "Aliment":         ["🍚 Riz",   "🐔 Poulet"],
            "Prix (€/kg)":     [prix_riz,    prix_poulet],
            "Énergie (kcal/kg)": [1300,      1650],
            "Protéines (g/kg)":  [70,         310],
        }
    )
    st.dataframe(df_nutrition, use_container_width=True, hide_index=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Bouton de résolution
# ─────────────────────────────────────────────────────────────────────────────
if st.button("🚀 Résoudre avec PuLP", type="primary", use_container_width=True):

    with st.spinner("Résolution en cours…"):
        res = resoudre_pl(prix_riz, prix_poulet, energie_min, proteines_min, poulet_min)

    if not res["optimal"]:
        st.error(f"❌ Le solveur n'a pas trouvé de solution optimale. Statut : {res['statut']}")
    else:
        # ── Bannière de succès ─────────────────────────────────────
        st.success(
            f"✅ Solution optimale trouvée — Coût minimal : **{res['cout']:.2f} €/semaine**"
        )

        # ── Métriques ─────────────────────────────────────────────
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("🍚 Riz",    f"{res['x_riz']:.4f} kg",    "kg/semaine")
        col_m2.metric("🐔 Poulet", f"{res['x_poulet']:.4f} kg", "kg/semaine")
        col_m3.metric("💰 Coût",   f"{res['cout']:.2f} €",      "€/semaine")

        st.divider()

        # ── Graphique + tableau ───────────────────────────────────
        col_graph, col_table = st.columns([3, 2])

        with col_graph:
            st.subheader("📈 Région réalisable")
            fig = creer_graphique(res)
            st.pyplot(fig)

        with col_table:
            st.subheader("📋 Vérification des contraintes")
            df_verif = creer_tableau_verification(res)
            st.dataframe(df_verif, use_container_width=True, hide_index=True)

            st.info(
                f"""
**Interprétation de la solution :**

- Acheter **{res['x_riz']:.2f} kg de riz** à {prix_riz:.2f} €/kg
  → coût riz : **{res['x_riz'] * prix_riz:.2f} €**
- Acheter **{res['x_poulet']:.2f} kg de poulet** à {prix_poulet:.2f} €/kg
  → coût poulet : **{res['x_poulet'] * prix_poulet:.2f} €**

**Coût total minimal : {res['cout']:.2f} €/semaine**

Énergie apportée : {res['energie_reel']:.0f} kcal/sem
Protéines apportées : {res['proteines_reel']:.1f} g/sem
"""
            )

# ─────────────────────────────────────────────────────────────────────────────
# Pied de page
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "🎓 Projet EMSI — Recherche Opérationnelle | "
    "Programmation Linéaire avec PuLP & Streamlit | "
    "2025-2026"
)
