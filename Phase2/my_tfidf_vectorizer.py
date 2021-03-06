from sklearn.feature_extraction.text import TfidfVectorizer


class MyTfIdfVectorizer:

    def __init__(self, raw_docs, preprocessor):
        self.preprocessor = preprocessor
        train_docs = preprocessor.preprocess(raw_docs)
        self.vectorizer = TfidfVectorizer(max_df=0.85, max_features=1000)
        self.vectorizer.fit(train_docs)

    def get_tfidf_vector(self, raw_doc):
        doc = self.preprocessor.preprocess([raw_doc])
        return self.vectorizer.transform(doc)

    def get_tfidf_vector_of_docs(self, raw_docs):
        docs = self.preprocessor.preprocess(raw_docs)
        return self.vectorizer.transform(docs)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names()
