import streamlit as st

FOND = "#f5f5f0"
COULEUR_ACHAT = "#566b82"   # bleu-gris : ce qu'Emma paie
COULEUR_MARGE = "#b8326a"   # rose : ce qui reste à Emma
COULEUR_ERREUR = "#c0392b"  # rouge : erreur, perte
COULEUR_OK = "#2e7d4f"      # vert : gain
ENCRE = "#1f1f1f"

# Contraste : thème clair forcé, même si le téléphone est en mode sombre
CSS = """
<style>
:root { color-scheme: light; }
.stApp { background-color: #f5f5f0; color: #1f1f1f; }
header[data-testid="stHeader"] { background-color: #f5f5f0; }
[data-testid="stSidebar"] { background-color: #ebebe4; }
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricLabel"], .stApp [data-testid="stWidgetLabel"] { color: #1f1f1f; }
.stApp blockquote { border-left: 4px solid #b8326a; opacity: 1; }
.stApp blockquote p { color: #1f1f1f; font-weight: 500; }
.stApp [data-testid="stCaptionContainer"] { opacity: 1; }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color: #3a3a3a; }
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] summary p { color: #1f1f1f; }
@media (max-width: 640px) {
    .stApp [data-testid="stMetricValue"], .stApp [data-testid="stMetricValue"] div { font-size: 2rem; }
}
</style>
"""


def init_page(titre_onglet):
    st.set_page_config(page_title=f"L'appMandier - Labo - {titre_onglet}", page_icon="💄", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)


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
        height=hauteur, margin=dict(l=10, r=10, t=10, b=40), plot_bgcolor=FOND, paper_bgcolor=FOND,
        font=dict(color=ENCRE, size=14), **extra,
    )
    fig.update_xaxes(tickfont=dict(size=13, color=ENCRE))
    fig.update_yaxes(tickfont=dict(size=13, color=ENCRE))
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


def texte_sur(couleur):
    """Texte blanc sur fond foncé, texte sombre sur fond clair (lisible partout)."""
    r, g, b = (int(couleur[i:i + 2], 16) for i in (1, 3, 5))
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "white" if luminance < 150 else ENCRE


def fonce(couleur, facteur=0.72):
    """Version assombrie d'une couleur, pour du texte coloré lisible sur fond clair."""
    r, g, b = (int(couleur[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02x}{:02x}{:02x}".format(int(r * facteur), int(g * facteur), int(b * facteur))
