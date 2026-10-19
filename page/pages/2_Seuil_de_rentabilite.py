import plotly.graph_objects as go
import streamlit as st

from labo_common import (COULEUR_ACHAT, COULEUR_ERREUR, COULEUR_MARGE, COULEUR_OK, ENCRE, entete, euros, fmt,
                         init_page, style)

init_page("Seuil de rentabilité")
entete("Seuil de rentabilité : à partir de quand Emma gagne-t-elle de l'argent ?")

with st.sidebar:
    st.header("📊 Paramètres")
    charges_fixes = st.slider("Charges fixes du mois (€)", 500, 8000, 2800, step=100)
    pct_cv = st.slider("Charges variables (% du CA)", 1, 60, 25)
    ca = st.slider("CA du mois (€)", 0, 15000, 7200, step=100)

tmcv = 1 - pct_cv / 100                      # taux de marge sur coûts variables
seuil = charges_fixes / tmcv
mcv = ca * tmcv
resultat = mcv - charges_fixes
seuil_faux = charges_fixes / (pct_cv / 100)  # erreur classique
jour = seuil / ca * 30 if ca > 0 else None

st.markdown(
    f"> **Emma paie {euros(charges_fixes)} de charges fixes par mois (loyer, assurance, abonnements). "
    f"Sur chaque euro encaissé, {pct_cv} centimes partent en consommables. "
    f"Combien doit-elle encaisser avant de commencer à gagner de l'argent ?**"
)
st.write("Déplace les curseurs à gauche : le seuil et les graphiques se recalculent.")

# ---- 1. Le seuil
st.markdown("## 1. Le seuil de rentabilité")
c1, c2, c3 = st.columns(3)
c1.metric("Taux de marge sur coûts variables", f"{fmt(tmcv * 100)} %", help="100 % − taux de charges variables")
c2.metric("Seuil de rentabilité", euros(seuil), help="Charges fixes ÷ taux de marge sur coûts variables")
c3.metric("Résultat du mois", euros(resultat), help="Marge sur coûts variables − charges fixes")

st.info(
    f"Sur chaque euro encaissé, il reste {fmt(tmcv * 100)} centimes une fois les consommables payés : "
    f"c'est ce qui sert à payer les charges fixes. Pour payer {euros(charges_fixes)}, il faut donc encaisser "
    f"{euros(charges_fixes)} ÷ {fmt(tmcv, 2)} = **{euros(seuil)}**."
)

x_max = max(ca * 1.2, seuil * 1.6, 1000)
fig1 = go.Figure()
fig1.add_vrect(x0=0, x1=seuil, fillcolor=COULEUR_ERREUR, opacity=0.08, line_width=0,
               annotation_text="Zone de perte", annotation_position="bottom left",
               annotation_font=dict(size=13, color=COULEUR_ERREUR))
fig1.add_vrect(x0=seuil, x1=x_max, fillcolor=COULEUR_OK, opacity=0.08, line_width=0,
               annotation_text="Zone de gain", annotation_position="bottom right",
               annotation_font=dict(size=13, color=COULEUR_OK))
fig1.add_scatter(x=[0, x_max], y=[-charges_fixes, x_max * tmcv - charges_fixes], mode="lines",
                 line=dict(color=COULEUR_ACHAT, width=3), name="Résultat", showlegend=False,
                 hovertemplate="CA %{x:.0f} € → résultat %{y:.0f} €<extra></extra>")
fig1.add_hline(y=0, line_color="#888", line_width=1)
fig1.add_scatter(x=[seuil], y=[0], mode="markers+text", text=["Seuil"], textposition="top center",
                 marker=dict(color=COULEUR_MARGE, size=14, line=dict(color="white", width=2)),
                 showlegend=False, hoverinfo="skip")
fig1.add_scatter(x=[ca], y=[resultat], mode="markers+text", text=["Emma"], textposition="top center",
                 marker=dict(color=ENCRE, size=14, line=dict(color="white", width=2)),
                 showlegend=False, hoverinfo="skip")
style(fig1, 380, xaxis=dict(title="CA du mois (€)", gridcolor="#e4e4dd", range=[0, x_max]),
      yaxis=dict(title="Résultat (€)", gridcolor="#e4e4dd"))
st.plotly_chart(fig1, width="stretch")

if ca <= 0:
    st.warning("Emma n'encaisse rien ce mois-ci : elle perd l'équivalent de toutes ses charges fixes.")
elif ca < seuil:
    st.error(
        f"Avec {euros(ca)} de CA, Emma est **sous le seuil** : il lui manque {euros(seuil - ca)} de CA, "
        f"elle perd {euros(-resultat)} ce mois-ci."
    )
else:
    st.success(
        f"Avec {euros(ca)} de CA, Emma est **au-dessus du seuil** de {euros(ca - seuil)}. "
        f"Si ses ventes sont régulières, elle passe le seuil vers le **{int(round(jour))}e jour du mois** : "
        f"après, chaque euro encaissé lui reste (sauf les consommables)."
    )

# ---- 2. D'où vient le résultat
st.markdown("## 2. D'où vient le résultat")
fig2 = go.Figure(go.Waterfall(
    x=["CA", "Charges variables", "Marge sur coûts variables", "Charges fixes", "Résultat"],
    measure=["absolute", "relative", "total", "relative", "total"],
    y=[ca, -ca * pct_cv / 100, 0, -charges_fixes, 0],
    text=[euros(ca), euros(-ca * pct_cv / 100), euros(mcv), euros(-charges_fixes), euros(resultat)],
    textposition="outside", connector=dict(line=dict(color="#999")),
    increasing=dict(marker=dict(color=COULEUR_ACHAT)), decreasing=dict(marker=dict(color=COULEUR_ERREUR)),
    totals=dict(marker=dict(color=COULEUR_MARGE)), hoverinfo="skip",
))
style(fig2, 360, showlegend=False, yaxis=dict(title="€", gridcolor="#e4e4dd"), xaxis=dict(showgrid=False))
st.plotly_chart(fig2, width="stretch")

# ---- 3. Le piège
st.markdown("## 3. Le piège : diviser par le mauvais taux")
d1, d2 = st.columns(2)
d1.metric("Seuil correct (÷ taux de marge)", euros(seuil))
d2.metric(f"Seuil avec l'erreur (÷ {pct_cv} % de charges variables)", euros(seuil_faux))
st.warning(
    f"Si Emma divise ses charges fixes par le taux de **charges variables** ({pct_cv} %) au lieu du taux de "
    f"**marge sur coûts variables** ({fmt(tmcv * 100)} %), elle trouve {euros(seuil_faux)} au lieu de "
    f"{euros(seuil)}. Elle croirait qu'il faut {fmt(seuil_faux / seuil, 1)} fois plus de CA pour s'en sortir."
)

# ---- 4. À quoi ça sert
st.markdown("## 4. À quoi ça sert")
st.markdown(
    f"- **Fixer un objectif minimum** : le seuil est le CA en dessous duquel Emma perd de l'argent.\n"
    f"- **Mesurer une décision** : 100 € de charges fixes en plus (un abonnement, une embauche) obligent "
    f"Emma à encaisser **{euros(100 / tmcv)}** de plus chaque mois.\n"
    f"- **Savoir quand elle est tranquille** : plus elle passe le seuil tôt dans le mois, plus elle a de marge "
    f"de sécurité."
)
with st.expander("ℹ️ Rappel des formules"):
    st.markdown(
        "- **Taux de marge sur coûts variables** = 100 % − taux de charges variables\n"
        "- **Seuil de rentabilité** = charges fixes ÷ taux de marge sur coûts variables\n"
        "- **Résultat** = CA × taux de marge sur coûts variables − charges fixes\n\n"
        "Attention : dans le chapitre 2, le résultat de 400 € tient compte aussi des salaires et des autres "
        "charges (6 800 € de charges totales). Ici, on ne regarde que les charges fixes et les consommables, "
        "pour comprendre la mécanique du seuil."
    )
