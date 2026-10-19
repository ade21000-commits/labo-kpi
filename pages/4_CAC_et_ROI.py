import math

import plotly.graph_objects as go
import streamlit as st

from labo_common import (COULEUR_ACHAT, COULEUR_ERREUR, COULEUR_MARGE, entete, euros, fmt, init_page, style)

init_page("CAC et ROI")
entete("Coût d'acquisition et ROI : cette publicité vaut-elle son coût ?")

with st.sidebar:
    st.header("📊 Paramètres")
    st.markdown("**Instagram Ads**")
    cout_insta = st.slider("Dépense (€)", 50, 1000, 300, step=10, key="ci")
    ca_insta = st.slider("CA attribué (€)", 0, 3000, 900, step=10, key="ai")
    st.markdown("**Flyers**")
    cout_flyers = st.slider("Dépense (€)", 20, 500, 80, step=5, key="cf")
    ca_flyers = st.slider("CA attribué (€)", 0, 1500, 120, step=10, key="af")
    st.markdown("**Email promotionnel**")
    cout_email = st.slider("Dépense (€)", 5, 200, 15, step=5, key="ce")
    ca_email = st.slider("CA attribué (€)", 0, 1500, 450, step=10, key="ae")
    st.markdown("**Autres données**")
    marge_pct = st.slider("Marge nette sur le panier (%)", 5, 80, 30)
    nouvelles = st.slider("Nouvelles clientes acquises", 1, 60, 20)
    panier = st.slider("Panier moyen (€)", 10, 150, 45)

actions = [
    ("Instagram Ads", cout_insta, ca_insta),
    ("Flyers", cout_flyers, ca_flyers),
    ("Email", cout_email, ca_email),
]
m = marge_pct / 100

st.markdown(
    "> **Emma a dépensé de l'argent en publicité Instagram, en flyers et en email. "
    "Quelle action garder, laquelle arrêter ?**"
)
st.write("Déplace les curseurs à gauche : chaque graphique se recalcule.")

# ---- 1. Le ROI
st.markdown("## 1. Ce que rapporte 1 € dépensé")
noms = [a[0] for a in actions]
ca_par_euro = [ca / cout for _, cout, ca in actions]
marge_par_euro = [ca * m / cout for _, cout, ca in actions]
roi_ca = [(ca - cout) / cout * 100 for _, cout, ca in actions]
roi_marge = [(ca * m - cout) / cout * 100 for _, cout, ca in actions]

fig1 = go.Figure()
fig1.add_bar(x=noms, y=ca_par_euro, name="CA rapporté pour 1 € dépensé", marker_color=COULEUR_ACHAT,
             text=[f"{fmt(v, 2)} €" for v in ca_par_euro], textposition="outside", hoverinfo="skip")
fig1.add_bar(x=noms, y=marge_par_euro, name="Marge rapportée pour 1 € dépensé", marker_color=COULEUR_MARGE,
             text=[f"{fmt(v, 2)} €" for v in marge_par_euro], textposition="outside", hoverinfo="skip")
fig1.add_hline(y=1, line_dash="dash", line_color=COULEUR_ERREUR,
               annotation_text="1 € rapporté = 1 € dépensé", annotation_position="top right",
               annotation_font=dict(size=12, color=COULEUR_ERREUR))
style(fig1, 380, barmode="group", yaxis=dict(title="€ pour 1 € dépensé", gridcolor="#e4e4dd"),
      xaxis=dict(showgrid=False), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
st.plotly_chart(fig1, width="stretch")

tableau = ["| Action | Dépense | CA attribué | ROI sur le CA | ROI sur la marge |", "| --- | --- | --- | --- | --- |"]
for (nom, cout, ca), r1, r2 in zip(actions, roi_ca, roi_marge):
    tableau.append(f"| {nom} | {euros(cout)} | {euros(ca)} | {fmt(r1, 0)} % | {fmt(r2, 0)} % |")
st.markdown("\n".join(tableau))

pertes = [(nom, cout - ca * m) for (nom, cout, ca), r in zip(actions, roi_marge) if r < 0]
trompeuses = [nom for (nom, cout, ca), r1, r2 in zip(actions, roi_ca, roi_marge) if r1 >= 0 and r2 < 0]
if trompeuses:
    st.warning(
        f"Attention : le ROI sur le CA paraît positif pour {', '.join(trompeuses)}, mais Emma ne garde que "
        f"{marge_pct} % du CA. Sur la **marge**, ces actions ne rapportent pas ce qu'elles coûtent."
    )
elif pertes:
    st.warning("Sur la marge, certaines actions ne rapportent pas ce qu'elles coûtent : "
               + ", ".join(f"{nom} ({euros(p)} perdus)" for nom, p in pertes) + ".")
else:
    st.success("Sur la marge, chaque action rapporte plus qu'elle ne coûte.")
st.caption("ROI sur le CA = (CA généré − coût) ÷ coût × 100. ROI sur la marge = (marge générée − coût) ÷ coût × 100.")

# ---- 2. Le CAC
st.markdown("## 2. Ce que coûte une nouvelle cliente")
depenses = cout_insta + cout_flyers
cac = depenses / nouvelles
marge_visite = panier * m
perte_premiere = cac - marge_visite
visites_pour_rentabiliser = math.ceil(cac / marge_visite) if marge_visite > 0 else None

c1, c2, c3 = st.columns(3)
c1.metric("Coût d'acquisition (CAC)", euros(cac, 1), help="(Instagram + flyers) ÷ nouvelles clientes")
c2.metric("Marge de son premier panier", euros(marge_visite, 1), help="Panier moyen × marge nette")
c3.metric("Perte avant son retour", euros(max(perte_premiere, 0), 1))

fig2 = go.Figure()
fig2.add_bar(y=[""], x=[cac], orientation="h", marker_color=COULEUR_ERREUR, name="CAC",
             text=[f"Ce qu'Emma a payé<br>{euros(cac, 1)}"], textposition="inside", insidetextanchor="middle",
             textfont=dict(color="white", size=14), hoverinfo="skip")
fig2.add_bar(y=["  "], x=[marge_visite], orientation="h", marker_color=COULEUR_MARGE, name="Marge",
             text=[f"Marge du 1er panier<br>{euros(marge_visite, 1)}"], textposition="inside",
             insidetextanchor="middle", textfont=dict(color="white", size=14), hoverinfo="skip")
style(fig2, 220, showlegend=False, barmode="group",
      xaxis=dict(range=[0, max(cac, marge_visite) * 1.1], title="€ par cliente", showgrid=False),
      yaxis=dict(showticklabels=False, showgrid=False))
st.plotly_chart(fig2, width="stretch")

if perte_premiere > 0:
    st.info(
        f"Emma paie {euros(cac, 1)} pour trouver une cliente qui lui laisse {euros(marge_visite, 1)} à sa "
        f"première visite : elle perd {euros(perte_premiere, 1)}. "
        f"Elle récupère sa mise à la **{visites_pour_rentabiliser}e visite**. "
        f"C'est pour ça qu'une cliente qui revient vaut plus qu'une cliente qui passe."
    )
else:
    st.success(
        f"Le premier panier ({euros(marge_visite, 1)} de marge) couvre déjà le coût d'acquisition ({euros(cac, 1)}) : "
        f"l'acquisition est rentable dès la première visite."
    )

# ---- 3. À quoi ça sert
st.markdown("## 3. À quoi ça sert")
st.markdown(
    "- **Choisir où mettre le budget** : on compare les actions entre elles, avec la même mesure.\n"
    "- **Ne pas se faire piéger par le CA** : un ROI calculé sur le CA est flatteur, la marge dit ce qui reste.\n"
    "- **Savoir combien de visites il faut** : le CAC dit à partir de quelle visite une nouvelle cliente "
    "rapporte de l'argent."
)
with st.expander("ℹ️ Rappel des formules"):
    st.markdown(
        "- **CAC** = dépenses marketing ÷ nombre de nouvelles clientes\n"
        "- **ROI** = (gain généré − coût de l'action) ÷ coût de l'action × 100\n"
        "- **Marge du premier panier** = panier moyen × marge nette\n\n"
        "Dans le cours, le ROI se calcule sur le CA. Ici, on le compare à celui calculé sur la marge, "
        "qui est plus prudent."
    )
