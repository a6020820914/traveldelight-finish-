import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from members.models import User, Tour

def collaborative_filtering(user_id):
    # 基於用戶行為的協同過濾推薦邏輯
    pass

def content_based_filtering(tour_id):
    # 基於行程內容的推薦邏輯
    pass

def hybrid_recommendation(user_id):
    # 混合協同過濾與內容過濾的結果
    cf_result = collaborative_filtering(user_id)
    cb_result = content_based_filtering(user_id)

    # 混合推薦結果，例如加權平均
    final_recommendation = 0.5 * np.array(cf_result) + 0.5 * np.array(cb_result)
    return final_recommendation


from sklearn.feature_extraction.text import TfidfVectorizer

def extract_features(tours):
    descriptions = [tour.description for tour in tours]
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(descriptions)
    return feature_matrix