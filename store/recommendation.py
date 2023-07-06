from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Product

class RecommendationSystem:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.product_vectors = None

    def train(self):
        products = Product.objects.all()
        descriptions = [product.description for product in products]
        self.product_vectors = self.vectorizer.fit_transform(descriptions)

    def get_recommendations(self, product_id, num_recommendations=6):
        product_index = product_id - 1  # Assuming product IDs start from 1
        product_vector = self.product_vectors[product_index]
        similarity_scores = cosine_similarity(product_vector, self.product_vectors).flatten()
        top_indices = similarity_scores.argsort()[::-1][:num_recommendations]
        recommended_product_ids = []
        for index in top_indices:
            if index != product_index:
                recommended_product_ids.append(index + 1)
                if len(recommended_product_ids) == num_recommendations:
                    break
        return recommended_product_ids
