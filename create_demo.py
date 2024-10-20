import streamlit as st
import streamlit.components.v1 as components
import json

embedder = None
selected_reference = None
# Sample data
data_rncp, data_rome = {}, {}
references_rncp = list(data_rncp.keys())
references_rome = list(data_rome.keys())
parcours = ["Informatique: Expertise du développement web", "Marketing et Communication digitale: Communication et création de contenu", "Création et design: Direction Artistique et Brand Designer"]
MATIERES = ["Méthodologie de test et tests unitaires",
            "Integration et média continus",
            "Web Fullstack",
            "Accessibilité et qualité web",
            "Expert en techniques de production (Création et Design)",
            "Techniques de création (Création et Design)",
            "Brand design et stratégies de communication",
            "Marketing Mobile, User Acquisition et Modèles économiques CONNECT"]
mapping_matieres = {
    "Marketing Mobile, User Acquisition et Modèles économiques CONNECT": "Marketing_Mobile",
    "Méthodologie de test et tests unitaires": "Methodologie_de_test",
    "Integration et média continus": "Integration_et_media_continus",
    "Web Fullstack": "web_fullstack",
    "Accessibilité et qualité web": "Accessibilite_et_qualite_web",
    "Expert en techniques de production (Création et Design)": "Expert_en_techniques_de_production",
    "Techniques de création (Création et Design)": "Techniques_de_creation",
    "Brand design et stratégies de communication": "Brand_design_et_stategies_de_communication"
}

with open('data/mapping/mat_ref.json', 'r') as f:
    mapping_mat_ref = json.load(f)
with open('data/mapping/mat_ref_large.json', 'r') as f:
    mapping_mat_ref_large = json.load(f)

concept_keys = ["label", "definition"]
exercise_keys = ["id", "question", "query", "statement", "answers", "distractors", "veracity", "feedback"]
doc_keys = ["label"]

st.set_page_config(page_title="Demo Selector", layout="wide")

# Create a sidebar selector
st.sidebar.title("Navigation")
demo = st.sidebar.radio("Choix de la démo:", ("Résultats par matière", "Capsules de connaissance des référentiels"))

# # Initialize the session state for 'selected_reference' if it doesn't exist
# if 'selected_reference' not in st.session_state:
#     st.session_state.selected_reference = MATIERES[0]


# # Function to change the selected reference
# def change_reference(ref):
#     if ref in MATIERES:
#         st.session_state.selected_reference = ref
#     else:
#         st.error(f"The reference '{ref}' is not available.")

if demo == "Résultats par matière":
    # Streamlit app
    st.title("Ynov: résultat par matière")

    # Dropdown to select reference
    selected_reference = st.selectbox("Choix de la matière:", MATIERES, key="selected_reference")

    # Display selected reference data
    mapped_reference = mapping_matieres[selected_reference]
    competence_collection = mapping_mat_ref[selected_reference]
    if selected_reference in mapping_mat_ref_large:
        large_competence_collection = mapping_mat_ref_large[selected_reference]

    with open(f'data/matiere/knowledge_capsule_{mapped_reference}.json', 'r') as f:
        data = json.load(f)

    st.header("Compétences ROME associés")
    new_collection = []
    for competence, score in competence_collection:
        new_dic = {}
        new_dic["competence"] = competence["libelle_competence"]
        new_dic["macro competence associé"] = competence["libelle_macro_competence"]
        new_dic["code ROME"] = competence["code_rome"]
        new_dic["score"] = score
        new_collection.append(new_dic)
    st.write("Source: compétences des code ROME fournis - score de pertinence minimum 7/10")
    st.write(f"{len(new_collection)} compétences ROME liés")
    st.write(new_collection)

    if selected_reference in mapping_mat_ref_large:
        new_collection = []
        for competence, score in large_competence_collection:
            new_dic = {}
            new_dic["competence"] = competence["libelle_competence"]
            new_dic["macro competence associé"] = competence["libelle_macro_competence"]
            new_dic["code ROME"] = competence["code_rome"]
            new_dic["score"] = score
            new_collection.append(new_dic)
        st.write("Source: 900 compétences de domaine 'Communication, Création, Innovation, Nouvelles technologies' - score de pertinence minimum 7/10")
        st.write(f"{len(new_collection)} compétences ROME liés")
        st.write(new_collection)

    st.header("Capsule de connaissance générée")
    st.header("Introduction")
    st.write(data["introduction"])
    st.header("Synthèse d'information")
    st.write(data["synthesis"])

    st.header("Glossaire")
    concept_collection = data["concepts"]
    new_collection = []
    for concept_dict in concept_collection:
        new_dic = {}
        if concept_dict["score"] >= 8:
            new_dic["score"] = concept_dict["score"]
            new_concept = {}
            for key in concept_keys:
                if key in concept_dict["concept"]:
                    new_concept[key] = concept_dict["concept"][key]
            new_dic["concept"] = new_concept
            new_collection.append(new_dic)
    st.write(f"{len(new_collection)} concepts génératifs pertinents")
    st.write(new_collection)

    st.header("Je teste mes connaissances")
    exercise_collection = data["exercises"]
    new_collection = []
    for exercise_dict in exercise_collection:
        new_dic = {}
        if exercise_dict["score"] >= 7:
            new_dic["score"] = exercise_dict["score"]
            new_exercise = {}
            for key in exercise_keys:
                if key in exercise_dict["exercise"]:
                    new_exercise[key] = exercise_dict["exercise"][key]
            new_dic["exercise"] = new_exercise
            new_collection.append(new_dic)
    st.write(f"{len(new_collection)} exercices pertinents")
    st.write(new_collection)

    st.header("Sources")
    relevant_sources = data["sources"]
    new_collection = []
    for source_dict in relevant_sources:
        new_dic = {}
        for key in doc_keys:
            if key in source_dict["document"]:
                new_dic[key] = source_dict["document"][key]
        new_dic['AI generated title'] = source_dict["document"]["title"]
        new_dic["top_pages"] = source_dict["top_pages"]
        new_dic["score"] = source_dict["score"]
        new_collection.append(new_dic)
    st.write(f"{len(new_collection)} sources pertinentes")
    st.write(new_collection)

    st.header("Visualisation du sous-graphe")
    if st.button("Visualiser le sous-graphe de connaissance"):
        html_path = f"data/matiere/graph_{mapped_reference}.html"
        HtmlFile = open(html_path, 'r', encoding='utf-8')
        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1000, width=1000)

if demo == "Capsules de connaissance des référentiels":
    with open('data/competence/knowledge_capsule_mapping_marketing.json', 'r') as f:
        mapping_marketing = json.load(f)
    with open('data/competence/knowledge_capsule_mapping_design.json', 'r') as f:
        mapping_design = json.load(f)
    with open('data/competence/knowledge_capsule_mapping_informatique.json', 'r') as f:
        mapping_informatique = json.load(f)
    competences = list(mapping_marketing.keys()) + list(mapping_design.keys()) + list(mapping_informatique.keys())
    competences = list(set(competences))
    competences.sort()

    st.title("Ynov: Détail des référentiels")
    selected_competence = st.selectbox("Choix de la compétence:", competences, key="selected_competence")

    if selected_competence in mapping_marketing:
        competence_collection = mapping_marketing[selected_competence]
        competence_type = "Marketing"
        mapping = mapping_marketing
    elif selected_competence in mapping_design:
        competence_collection = mapping_design[selected_competence]
        competence_type = "Design"
        mapping = mapping_design
    elif selected_competence in mapping_informatique:
        competence_collection = mapping_informatique[selected_competence]
        competence_type = "Informatique"
        mapping = mapping_informatique

    data = mapping[selected_competence]

    st.header("Capsule de connaissance générée")
    st.header("Introduction")
    st.write(data["introduction"])
    st.header("Synthèse d'information")
    st.write(data["synthesis"])

    st.header("Glossaire")
    concept_collection = data["concepts"]
    new_collection = []
    for concept_dict in concept_collection:
        new_dic = {}
        if concept_dict["score"] >= 8:
            new_dic["score"] = concept_dict["score"]
            new_concept = {}
            for key in concept_keys:
                if key in concept_dict["concept"]:
                    new_concept[key] = concept_dict["concept"][key]
            new_dic["concept"] = new_concept
            new_collection.append(new_dic)
    st.write(f"{len(new_collection)} concepts génératifs pertinents")
    st.write(new_collection)

    st.header("Je teste mes connaissances")
    exercise_collection = data["exercises"]
    new_collection = []
    for exercise_dict in exercise_collection:
        new_dic = {}
        if exercise_dict["score"] >= 7:
            new_dic["score"] = exercise_dict["score"]
            new_exercise = {}
            for key in exercise_keys:
                if key in exercise_dict["exercise"]:
                    new_exercise[key] = exercise_dict["exercise"][key]
            new_dic["exercise"] = new_exercise
            new_collection.append(new_dic)
    st.write(f"{len(new_collection)} exercices pertinents")
    st.write(new_collection)

    st.header("Sources")
    relevant_sources = data["sources"]
    new_collection = []
    for source_dict in relevant_sources:
        new_dic = {}
        for key in doc_keys:
            if key in source_dict["document"]:
                new_dic[key] = source_dict["document"][key]
        new_dic['AI generated title'] = source_dict["document"]["title"]
        new_dic["top_pages"] = source_dict["top_pages"]
        new_dic["score"] = source_dict["score"]
        new_collection.append(new_dic)
    st.write(f"{len(new_collection)} sources pertinentes")
    st.write(new_collection)

    st.header("Visualisation du sous-graphe")
    if st.button("Visualiser le sous-graphe de connaissance"):
        html_path = f"data/competence/graph_{'_'.join(selected_competence.split())}.html"
        HtmlFile = open(html_path, 'r', encoding='utf-8')
        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1000, width=1000)
