import streamlit as st

FOND = "#f5f5f0"
COULEUR_ACHAT = "#566b82"   # bleu-gris : ce qu'Emma paie
COULEUR_MARGE = "#b8326a"   # rose : ce qui reste à Emma
COULEUR_ERREUR = "#c0392b"  # rouge : erreur, perte
COULEUR_OK = "#2e7d4f"      # vert : gain
ENCRE = "#2b2b2b"


def init_page(titre_onglet):
    st.set_page_config(page_title=f"L'appMandier - Labo - {titre_onglet}", page_icon="💄", layout="wide")
    st.markdown("<style>.stApp {background-color: #f5f5f0;}</style>", unsafe_allow_html=True)


def entete(sous_titre):
    st.title("💄🌺 L'appMandier - BTS 2 MECP")
    st.caption("by la team love")
    st.subheader(sous_titre)


def fmt(x, decimales=1):
    """Nombre à la française : virgule, sans zéro inutile."""
    texte = f"{x:.{decimales}f}"
    if "." in texte:
        texte = texte.rstrip("0").rstrip(".")
    return texte.replace(".", ",")


def euros(x, decimales=0):
    """Montant en euros avec espace pour les milliers."""
    texte = fmt(x, decimales)
    entier, _, reste = texte.partition(",")
    signe = "-" if entier.startswith("-") else ""
    entier = entier.lstrip("-")
    groupes = []
    while len(entier) > 3:
        groupes.insert(0, entier[-3:])
        entier = entier[:-3]
    groupes.insert(0, entier)
    resultat = signe + " ".join(groupes)
    return f"{resultat},{reste} €" if reste else f"{resultat} €"


def style(fig, hauteur=300, **extra):
    """Mise en forme commune à tous les graphiques."""
    fig.update_layout(
        height=hauteur, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor=FOND, paper_bgcolor=FOND,
        font=dict(color=ENCRE, size=14), **extra,
    )
    return fig


def segment(fig, y, x, couleur, texte):
    """Ajoute un segment de barre horizontale empilée avec son texte."""
    fig.add_bar(y=[y], x=[x], orientation="h", marker_color=couleur, text=[texte], textposition="inside",
                insidetextanchor="middle", textfont=dict(color="white", size=14), hoverinfo="skip",
                showlegend=False)


def degrade(valeur, bas, haut):
    """Couleur qui passe du rouge (valeur <= bas) à l'orange puis au vert (valeur >= haut)."""
    t = 0.0 if haut == bas else min(1.0, max(0.0, (valeur - bas) / (haut - bas)))
    rouge, orange, vert = (192, 57, 43), (224, 160, 48), (46, 125, 79)
    if t < 0.5:
        a, b, u = rouge, orange, t / 0.5
    else:
        a, b, u = orange, vert, (t - 0.5) / 0.5
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * u):02x}" for i in range(3))


def clientes(n):
    """« 1 cliente », « 0 cliente », « 22 clientes »."""
    n = int(round(n))
    return f"{n} cliente{'s' if n > 1 else ''}"
