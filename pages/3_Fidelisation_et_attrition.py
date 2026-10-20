import math

import plotly.graph_objects as go
import streamlit as st

from labo_common import (COULEUR_ACHAT, COULEUR_ERREUR, COULEUR_MARGE, clientes, entete, euros, fmt,
                         init_page, segment, style)

init_page("Fidélisation et attrition")
entete("Fidélisation et attrition : garder ou chercher des clientes ?")

with st.sidebar:
    st.header("📊 Paramètres")
    debut = st.slider("Clientes de janvier", 20, 200, 80)
    revenues = st.slider("Clientes de janvier revenues en mars", 0, debut, min(58, debut))
    nouvelles = st.slider("Nouvelles clientes accueillies en mars", 0, 60, 20)
    panier = st.slider("Panier moyen (€)", 10, 150, 45)
    visites_an = st.slider("Visites par an d'une cliente régulière", 1, 24, 12)
    points = st.slider("Points de fidélisation gagnés (objectif)", 0, 30, 5)

fidelisation = revenues / debut * 100
attrition = 100 - fidelisation
perdues = debut - revenues
ca_cliente = panier * visites_an          # CA annuel d'une cliente régulière
ca_perdu = perdues * ca_cliente
gardees_en_plus = min(perdues, debut * points / 100)
ca_gagne = gardees_en_plus * ca_cliente
solde = nouvelles - perdues

st.markdown(
    f"> **Emma avait {debut} clientes en janvier. En mars, {revenues} sont revenues. "
    f"Doit-elle d'abord chercher de nouvelles clientes, ou garder celles qu'elle a ?**"
)
st.write("Déplace les curseurs à gauche : les chiffres et les graphiques se recalculent.")

# ---- 1. Le seau percé
st.markdown("## 1. Combien de clientes partent ?")
c1, c2, c3 = st.columns(3)
c1.metric("Taux de fidélisation", f"{fmt(fidelisation)} %", help="Clientes revenues ÷ clientes de janvier × 100")
c2.metric("Taux d'attrition", f"{fmt(attrition)} %", help="100 % − taux de fidélisation")
c3.metric("Clientes perdues", f"{perdues}", help="Clientes de janvier − clientes revenues")

fig1 = go.Figure()
segment(fig1, "", revenues, COULEUR_ACHAT, f"Revenues<br>{revenues}")
if perdues > 0:
    segment(fig1, "", perdues, COULEUR_ERREUR, f"Perdues<br>{perdues}")
style(fig1, 160, barmode="stack", xaxis=dict(range=[0, debut], title=f"Les {debut} clientes de janvier",
                                            showgrid=False),
      yaxis=dict(showticklabels=False, showgrid=False))
st.plotly_chart(fig1, width="stretch")

# ---- 2. En euros
st.markdown("## 2. Ce que ça coûte en euros")
d1, d2, d3 = st.columns(3)
d1.metric("CA annuel d'une cliente", euros(ca_cliente), help="Panier moyen × visites par an")
d2.metric("CA annuel perdu", euros(ca_perdu), help="Clientes perdues × CA annuel d'une cliente")
d3.metric("Solde (nouvelles − perdues)", f"{solde:+d}")
st.warning(
    f"Chaque cliente perdue représente **{euros(ca_cliente)}** de CA par an. "
    f"Avec {clientes(perdues)} perdue{'s' if perdues > 1 else ''}, Emma voit partir **{euros(ca_perdu)}** de CA annuel. "
    f"« {fmt(attrition)} % de clientes perdues » paraît peu, mais en euros c'est beaucoup."
)
if solde < 0:
    st.error(
        f"Emma perd {clientes(perdues)} et en gagne {nouvelles} : sa base **diminue** de {clientes(-solde)}. "
        f"Même en cherchant de nouvelles clientes, elle ne fait que remplacer celles qui partent."
    )
elif solde == 0:
    st.info(f"Emma perd {clientes(perdues)} et en gagne {nouvelles} : sa base ne grandit pas.")
else:
    st.success(f"Emma perd {clientes(perdues)} et en gagne {nouvelles} : sa base grandit de {clientes(solde)}.")

# ---- 3. Et si elle fidélisait mieux ?
st.markdown("## 3. Et si Emma fidélisait mieux ?")
fig2 = go.Figure()
fig2.add_bar(x=["Aujourd'hui", f"Avec +{points} points"], y=[ca_perdu, ca_perdu - ca_gagne],
             marker_color=[COULEUR_ERREUR, COULEUR_MARGE],
             text=[euros(ca_perdu), euros(ca_perdu - ca_gagne)], textposition="outside", hoverinfo="skip")
style(fig2, 320, showlegend=False, yaxis=dict(title="CA annuel perdu (€)", gridcolor="#e4e4dd",
                                              range=[0, max(ca_perdu * 1.2, 100)]),
      xaxis=dict(showgrid=False))
st.plotly_chart(fig2, width="stretch")
st.success(
    f"Gagner {points} points de fidélisation, c'est garder **{fmt(gardees_en_plus, 1)} cliente{'s' if gardees_en_plus > 1 else ''} de plus** : "
    f"**{euros(ca_gagne)}** de CA annuel sauvés, sans dépenser un euro de publicité."
)

# ---- 4. À quoi ça sert
st.markdown("## 4. À quoi ça sert")
st.markdown(
    "- **Choisir où mettre son énergie** : garder une cliente coûte moins cher que d'en trouver une nouvelle.\n"
    "- **Voir le trou dans le seau** : le taux de fidélisation dit si la base de clientes tient ou se vide.\n"
    "- **Chiffrer l'effort** : l'attrition en pourcentage est abstraite, en euros elle devient une décision."
)
with st.expander("ℹ️ Rappel des formules"):
    st.markdown(
        "- **Taux de fidélisation** = clientes de début de période revenues ÷ clientes de début de période × 100\n"
        "- **Taux d'attrition** = 100 % − taux de fidélisation\n"
        "- **Clientes perdues** = clientes de début de période − clientes revenues\n"
        "- **CA annuel d'une cliente** = panier moyen × visites par an\n\n"
        "Repère : un bon taux de fidélisation en institut se situe entre 65 % et 80 %. Alerte en dessous de 60 %."
    )
