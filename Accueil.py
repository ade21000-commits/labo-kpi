import streamlit as st

from labo_common import entete, init_page

init_page("Accueil")
entete("Laboratoire KPI")

st.write(
    "Ici, tu ne calcules pas : tu **comprends à quoi sert un KPI**. "
    "Chaque page pose une question à laquelle Emma doit répondre. "
    "Déplace les curseurs à gauche et regarde ce qui change."
)

st.markdown("### Les pages du laboratoire")
st.page_link("pages/1_Taux_de_marque_et_de_marge.py", label="Taux de marque et taux de marge (KPI 7)", icon="🏷️")
st.caption("À quel prix Emma doit-elle vendre un produit ? Pourquoi confondre les deux taux coûte cher.")
st.page_link("pages/2_Seuil_de_rentabilite.py", label="Seuil de rentabilité (KPI 8)", icon="⚖️")
st.caption("Combien Emma doit-elle encaisser avant de gagner de l'argent ?")
st.page_link("pages/3_Fidelisation_et_attrition.py", label="Fidélisation et attrition (KPI 12 et 14)", icon="🪣")
st.caption("Vaut-il mieux chercher de nouvelles clientes ou garder celles qu'on a ?")
st.page_link("pages/4_CAC_et_ROI.py", label="Coût d'acquisition et ROI (KPI 23 et 24)", icon="📣")
st.caption("Cette publicité vaut-elle son coût ?")

with st.expander("ℹ️ Mode d'emploi"):
    st.markdown(
        "1. Lis la question d'Emma en haut de la page.\n"
        "2. Déplace un curseur à la fois.\n"
        "3. Regarde les chiffres et les graphiques : qu'est-ce qui bouge, et pourquoi ?\n"
        "4. Lis le message : il te dit ce que le KPI aide à décider.\n\n"
        "Les chiffres de départ sont ceux de l'Institut d'Emma."
    )
