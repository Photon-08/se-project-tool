import numpy as np
from sentence_transformers import SentenceTransformer
def calculate_similarity(embeddings_dict, embed_model='sentence-transformers/static-similarity-mrl-multilingual-v1'):
    model = SentenceTransformer(embed_model)
    similarity_dict = {}

    for current_team in embeddings_dict:
        for other_team in embeddings_dict:
            if current_team != other_team:
                team_string = f"Team {current_team} and Team {other_team}"
                if team_string not in similarity_dict and f"Team {other_team} and Team {current_team}" not in similarity_dict:
                    if len(embeddings_dict[current_team].shape) == 1:
                        embeddings_dict[current_team] = embeddings_dict[current_team].unsqueeze(0)
                    if len(embeddings_dict[other_team].shape) == 1:
                        embeddings_dict[other_team] = embeddings_dict[other_team].unsqueeze(0)
                    try:
                        similarity = model.similarity(embeddings_dict[current_team], embeddings_dict[other_team])
                        similarity_dict[team_string] = round(float(similarity[0]), 2)
                    except:
                        similarity = -1.00000
                        similarity_dict[team_string] = round(float(similarity), 2)
                    

    return similarity_dict
def calculate_tfidf_similarity(tfidf_embeddings_dict):
    similarity_dict = {}

    for current_team in tfidf_embeddings_dict:
        for other_team in tfidf_embeddings_dict:
            if current_team != other_team:
                team_string = f"Team {current_team} and Team {other_team}"
                if team_string not in similarity_dict and f"Team {other_team} and Team {current_team}" not in similarity_dict:
                    similarity = np.dot(tfidf_embeddings_dict[current_team], tfidf_embeddings_dict[other_team].T)
                    similarity_dict[team_string] = round(float(similarity[0][0]), 2)

    return similarity_dict


def calculate_similarity_paraphrase(embeddings_dict, embed_model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
    model = SentenceTransformer(embed_model)
    similarity_dict = {}

    for current_team in embeddings_dict:
        for other_team in embeddings_dict:
            if current_team != other_team:
                team_string = f"Team {current_team} and Team {other_team}"
                if team_string not in similarity_dict and f"Team {other_team} and Team {current_team}" not in similarity_dict:
                    try:
                        similarity = model.similarity(embeddings_dict[current_team], embeddings_dict[other_team])
                        similarity_dict[team_string] = round(float(similarity[0]), 2)
                    except:
                        similarity = -1.00000
                        similarity_dict[team_string] = round(float(similarity), 2)

    return similarity_dict

def calculate_composite_similarity(context_aware_embeddings, tfidf_embeddings,paraphrase_sim, alpha=0.5):
    composite_similarity_dict = {}

    tfidf_sim = np.array(list(tfidf_embeddings.values()))
    embed_sim = np.array(list(context_aware_embeddings.values()))
    paraphrased_sim = np.array(list(paraphrase_sim.values()))

    linear_comb = 0.2 * tfidf_sim + 0.4 * embed_sim + 0.4 * paraphrased_sim

    for i in range(len(linear_comb)):
        composite_similarity_dict[list(context_aware_embeddings.keys())[i]] = linear_comb[i]


    return composite_similarity_dict
