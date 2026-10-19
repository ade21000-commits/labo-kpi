import plotly.graph_objects as go
import streamlit as st

from labo_common import (COULEUR_ACHAT, COULEUR_ERREUR, COULEUR_MARGE, ENCRE, entete, fmt, init_page,
                         segment, style)

init_page("Taux de marque et de marge")
entete("Taux de marque et taux de marge : à quoi ça sert ?")

with st.sidebar:
    st.header("📊 Paramètres")
    prix_achat = st.slider("Prix d'achat HT du produit (€)", 1, 100, 24)
    taux_marque_vise = st.slider("Taux de marque visé (%)", 5, 90, 60)
    ca_produits = st.slider("Ventes de produits du mois (€)", 100, 3000, 800, step=50)

m = taux_marque_vise / 100

# Bon calcul : on vise un taux de MARQUE
prix_vente = prix_achat / (1 - m)
marge = prix_vente - prix_achat
taux_marge = marge / prix_achat * 100
coefficient = prix_vente / prix_achat

# Erreur classique : on applique ce même pourcentage comme taux de MARGE
prix_vente_erreur = prix_achat * (1 + m)
marge_erreur = prix_vente_erreur - prix_achat
marque_reelle = marge_erreur / prix_vente_erreur * 100
manque = prix_vente - prix_vente_erreur

st.markdown(
    f"> **Emma rachète un produit {fmt(prix_achat)} € HT. Elle veut garder {taux_marque_vise} % du prix de vente "
    f"pour payer ses charges. À quel prix doit-elle le vendre ?**"
)
st.write("Déplace les curseurs à gauche : le prix et les graphiques se recalculent.")

# ---- 1. Fixer le prix
st.markdown("## 1. Fixer le prix de vente")
c1, c2, c3 = st.columns(3)
c1.metric("Prix de vente", f"{fmt(prix_vente)} €", help="Prix d'achat ÷ (1 − taux de marque)")
c2.metric("Taux de marge équivalent", f"{fmt(taux_marge)} %", help="Marge ÷ prix d'achat × 100")
c3.metric("Coefficient multiplicateur", f"× {fmt(coefficient, 2)}", help="Prix de vente ÷ prix d'achat")
st.info(
    f"Pour garder {taux_marque_vise} % du prix de vente, Emma multiplie son prix d'achat par "
    f"**{fmt(coefficient, 2)}** : {fmt(prix_achat)} € × {fmt(coefficient, 2)} = **{fmt(prix_vente)} €**. "
    f"Dit autrement, son taux de marge est de {fmt(taux_marge)} %."
)

st.markdown("### Le piège : confondre les deux taux")
etiquette_bon = f"Je vise {taux_marque_vise} % de marque"
etiquette_faux = f"J'applique {taux_marque_vise} % de marge"
fig1 = go.Figure()
segment(fig1, etiquette_faux, prix_achat, COULEUR_ACHAT, f"Achat {fmt(prix_achat)} €")
segment(fig1, etiquette_faux, marge_erreur, COULEUR_ERREUR, f"Marge {fmt(marge_erreur)} €")
segment(fig1, etiquette_bon, prix_achat, COULEUR_ACHAT, f"Achat {fmt(prix_achat)} €")
segment(fig1, etiquette_bon, marge, COULEUR_MARGE, f"Marge {fmt(marge)} €")
fig1.add_annotation(x=prix_vente, y=etiquette_bon, text=f"  <b>{fmt(prix_vente)} €</b>", showarrow=False,
                    xanchor="left", font=dict(size=16, color=ENCRE))
fig1.add_annotation(x=prix_vente_erreur, y=etiquette_faux, text=f"  <b>{fmt(prix_vente_erreur)} €</b>",
                    showarrow=False, xanchor="left", font=dict(size=16, color=ENCRE))
style(fig1, 260, barmode="stack",
      xaxis=dict(range=[0, prix_vente * 1.18], title="Prix de vente HT (€)", showgrid=False),
      yaxis=dict(showgrid=False))
st.plotly_chart(fig1, width="stretch")

d1, d2, d3 = st.columns(3)
d1.metric("Prix avec l'erreur", f"{fmt(prix_vente_erreur)} €")
d2.metric("Taux de marque réellement obtenu", f"{fmt(marque_reelle)} %",
          delta=f"{fmt(marque_reelle - taux_marque_vise)} points")
d3.metric("Manque à gagner par produit", f"{fmt(manque)} €")
st.warning(
    f"Si Emma applique {taux_marque_vise} % de **marge** au lieu de {taux_marque_vise} % de **marque**, "
    f"elle vend à {fmt(prix_vente_erreur)} € au lieu de {fmt(prix_vente)} €. Elle ne garde que "
    f"{fmt(marque_reelle)} % du prix de vente, soit {fmt(manque)} € de moins sur chaque produit vendu."
)

# ---- 2. Sur 100 € encaissés
st.markdown("## 2. Ce que le taux de marque dit sur la caisse")
achats = ca_produits * (1 - m)
marge_commerciale = ca_produits * m
fig2 = go.Figure()
segment(fig2, "", achats, COULEUR_ACHAT, f"Payé au fournisseur<br>{fmt(achats, 0)} €")
segment(fig2, "", marge_commerciale, COULEUR_MARGE, f"Reste à Emma<br>{fmt(marge_commerciale, 0)} €")
style(fig2, 170, barmode="stack",
      xaxis=dict(range=[0, ca_produits], title=f"Ventes de produits : {fmt(ca_produits, 0)} €", showgrid=False),
      yaxis=dict(showticklabels=False, showgrid=False))
st.plotly_chart(fig2, width="stretch")
st.success(
    f"Sur chaque 100 € encaissés, **{taux_marque_vise} € restent** à Emma après avoir payé la marchandise. "
    f"Sur {fmt(ca_produits, 0)} € de ventes, cela fait **{fmt(marge_commerciale, 0)} €** pour payer le loyer, "
    f"les salaires et le reste : c'est la marge commerciale (KPI 9)."
)

# ---- 3. Quel taux pour quoi faire ?
st.markdown("## 3. Quel taux utiliser, et pour quoi ?")
st.markdown(
    "| | Taux de marque | Taux de marge (ou coefficient) |\n"
    "| --- | --- | --- |\n"
    "| **Ce qu'il dit** | Part du prix de vente qui reste à l'institut | De combien on multiplie le prix d'achat |\n"
    "| **Je l'utilise pour** | Comparer des produits, suivre la rentabilité, viser un objectif | Fixer un prix rapidement |\n"
    "| **Exemple d'Emma** | 60 % : sur 100 € encaissés, 60 € restent | 150 % ou × 2,5 : j'achète 24 €, je vends 60 € |\n"
    "| **Limite** | Ne dépasse jamais 100 % | Peut dépasser 100 % |"
)
with st.expander("ℹ️ Rappel des formules"):
    st.markdown(
        "- **Taux de marque** = (prix de vente − prix d'achat) ÷ **prix de vente** × 100\n"
        "- **Taux de marge** = (prix de vente − prix d'achat) ÷ **prix d'achat** × 100\n"
        "- **Prix de vente** = prix d'achat ÷ (1 − taux de marque)\n"
        "- **Coefficient** = prix de vente ÷ prix d'achat = 1 + taux de marge\n\n"
        "Pour ne pas confondre : **marge → je pars de l'achat**, **marque → je pars de la vente**."
    )
