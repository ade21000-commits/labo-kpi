import plotly.graph_objects as go
import streamlit as st

from labo_common import COULEUR_ACHAT, degrade, entete, euros, fmt, init_page, style

init_page("Taux de marque et de marge")
entete("Taux de marque et taux de marge : à quoi ça sert ?")

# Repères de couleur : le taux de marque passe du rouge (20 %) au vert (70 %)
BAS, HAUT = 20, 70

with st.sidebar:
    st.header("📊 Paramètres")
    prix_achat = st.slider("Prix d'achat HT du produit (€)", 2, 80, 18)
    mode = st.radio("Je règle…", ["le prix de vente", "le taux de marque visé"], horizontal=True)
    if mode == "le prix de vente":
        prix_vente = st.slider("Prix de vente HT (€)", float(prix_achat + 1), float(prix_achat * 5),
                               float(min(max(40, prix_achat + 1), prix_achat * 5)), step=0.5)
        taux_marque_vise = (prix_vente - prix_achat) / prix_vente * 100
    else:
        taux_marque_vise = st.slider("Taux de marque visé (%)", 10, 80, 55)
        prix_vente = prix_achat / (1 - taux_marque_vise / 100)
    ca_produits = st.slider("Ventes de produits du mois (€)", 500, 10000, 4000, step=250)

m = taux_marque_vise / 100
tm = fmt(taux_marque_vise)  # taux affiché à la française

# Bon calcul : on vise un taux de MARQUE
marge = prix_vente - prix_achat
taux_marge = marge / prix_achat * 100
coefficient = prix_vente / prix_achat

# Erreur classique : on applique ce même pourcentage comme taux de MARGE
prix_vente_erreur = prix_achat * (1 + m)
marge_erreur = prix_vente_erreur - prix_achat
marque_reelle = marge_erreur / prix_vente_erreur * 100
manque = prix_vente - prix_vente_erreur

couleur_visee = degrade(taux_marque_vise, BAS, HAUT)
couleur_reelle = degrade(marque_reelle, BAS, HAUT)

if taux_marque_vise < 40:
    repere = "faible : il restera peu pour payer loyer et salaires"
elif taux_marque_vise < 55:
    repere = "correct"
else:
    repere = "confortable"

if mode == "le prix de vente":
    st.markdown(
        f"> Emma, gérante d'un institut de 3 personnes, rachète une crème {euros(prix_achat, 0)} HT et la vend "
        f"{euros(prix_vente, 2)} HT. Il lui reste "
        f"<span style='color:{couleur_visee};font-weight:700'>{tm} %</span> du prix de vente pour payer ses "
        f"charges ({repere}). **Est-ce assez ?**",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"> Emma, gérante d'un institut de 3 personnes, rachète une crème {euros(prix_achat, 0)} HT. "
        f"Elle veut garder <span style='color:{couleur_visee};font-weight:700'>{tm} %</span> du prix "
        f"de vente pour payer ses charges ({repere}). **À quel prix la vend-elle ?**",
        unsafe_allow_html=True,
    )

# ---- Chiffres clés sur une seule ligne
c1, c2, c3, c4 = st.columns(4)
c1.metric("Prix de vente HT", euros(prix_vente, 2), help="Prix d'achat ÷ (1 − taux de marque)")
c2.metric("Coefficient", f"× {fmt(coefficient, 2)}", help="Prix de vente ÷ prix d'achat")
c3.metric("Taux de marge équivalent", f"{fmt(taux_marge)} %", help="Marge ÷ prix d'achat × 100")
c4.metric("Reste à Emma par produit", euros(marge, 2), help="Prix de vente − prix d'achat")

# ---- Trois graphiques verticaux : ce qu'on déduit, étape par étape
def deduction(titre_bas, vente, achat, couleur_reste, hauteur_max):
    """Colonne « prix de vente − achat = reste », avec les montants écrits sur chaque barre."""
    reste = vente - achat
    fig = go.Figure(go.Waterfall(
        x=["Prix de vente", "− Achat", "= Reste"],
        measure=["absolute", "relative", "total"],
        y=[vente, -achat, 0],
        text=[euros(vente, 2), "− " + euros(achat, 2), "= " + euros(reste, 2)],
        textposition="outside", connector=dict(line=dict(color="#999", dash="dot")),
        increasing=dict(marker=dict(color="#9aa3ad")), decreasing=dict(marker=dict(color=COULEUR_ACHAT)),
        totals=dict(marker=dict(color=couleur_reste)), hoverinfo="skip",
    ))
    style(fig, 330, showlegend=False,
          yaxis=dict(range=[0, hauteur_max], showgrid=True, gridcolor="#e4e4dd", showticklabels=False),
          xaxis=dict(showgrid=False))
    return fig


g1, g2, g3 = st.columns(3, gap="large")

with g1:
    st.markdown(f"#### Bon : {tm} % de marque")
    st.plotly_chart(deduction("", prix_vente, prix_achat, couleur_visee, prix_vente * 1.2), width="stretch")
    st.markdown(
        f"Le reste est {euros(marge, 2)} sur un prix de {euros(prix_vente, 2)} : "
        f"{fmt(marge, 2)} ÷ {fmt(prix_vente, 2)} = "
        f"<span style='color:{couleur_visee};font-weight:700'>{tm} %</span> de marque.",
        unsafe_allow_html=True,
    )

with g2:
    st.markdown(f"#### Piège : {tm} % de marge")
    st.plotly_chart(deduction("", prix_vente_erreur, prix_achat, couleur_reelle, prix_vente * 1.2),
                    width="stretch")
    st.markdown(
        f"Prix = {fmt(prix_achat)} × {fmt(1 + m, 2)} = {euros(prix_vente_erreur, 2)}. "
        f"Le reste est {euros(marge_erreur, 2)} : {fmt(marge_erreur, 2)} ÷ {fmt(prix_vente_erreur, 2)} = "
        f"<span style='color:{couleur_reelle};font-weight:700'>{fmt(marque_reelle)} %</span> de marque, "
        f"pas {tm} %. **{euros(manque, 2)} perdus** par produit.",
        unsafe_allow_html=True,
    )

with g3:
    st.markdown(f"#### À la caisse : {euros(ca_produits)}")
    achats = ca_produits * (1 - m)
    marge_commerciale = ca_produits * m
    st.plotly_chart(deduction("", ca_produits, achats, couleur_visee, ca_produits * 1.2), width="stretch")
    st.markdown(
        f"Sur chaque 100 € encaissés, **{tm} € restent** à Emma. Sur {euros(ca_produits)} : "
        f"**{euros(marge_commerciale)}** pour payer loyer, salaires et le reste (marge commerciale, KPI 9)."
    )

# ---- Mémo replié
with st.expander("Quel taux utiliser, et pour quoi ? Formules"):
    st.markdown(
        "| | Taux de marque | Taux de marge (ou coefficient) |\n"
        "| --- | --- | --- |\n"
        "| **Il dit** | Part du prix de vente qui reste à l'institut | De combien on multiplie le prix d'achat |\n"
        "| **Je l'utilise pour** | Comparer, suivre la rentabilité, viser un objectif | Fixer un prix rapidement |\n"
        "| **Limite** | Ne dépasse jamais 100 % | Peut dépasser 100 % |\n\n"
        "- **Taux de marque** = (vente − achat) ÷ **vente** × 100\n"
        "- **Taux de marge** = (vente − achat) ÷ **achat** × 100\n"
        "- **Prix de vente** = achat ÷ (1 − taux de marque)\n\n"
        "Pour ne pas confondre : **marge → je pars de l'achat**, **marque → je pars de la vente**."
    )
