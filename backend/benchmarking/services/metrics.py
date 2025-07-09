# metrics.py

import nltk
import logging
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import textstat

logger = logging.getLogger(__name__)

# Asegura recursos NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextMetrics:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        """Tokeniza y filtra stopwords"""
        try:
            words = word_tokenize(text.lower())
            return [w for w in words if w.isalpha() and w not in self.stop_words]
        except Exception as e:
            logger.error(f"Preprocessing error: {str(e)}")
            return []

    def jaccard_similarity(self, str1, str2):
        """Jaccard [0-1]"""
        try:
            a = set(self.preprocess(str1))
            b = set(self.preprocess(str2))
            intersection = len(a & b)
            union = len(a | b)
            return intersection / union if union else 0
        except Exception as e:
            logger.error(f"Jaccard error: {str(e)}")
            return 0

    def cosine_similarity(self, text1, text2):
        """Coseno [0-1]"""
        try:
            vect = CountVectorizer().fit_transform([text1, text2])
            vectors = vect.toarray()
            csim = cosine_similarity(vectors)
            return csim[0, 1]
        except Exception as e:
            logger.error(f"Cosine error: {str(e)}")
            return 0

    def levenshtein_distance(self, s1, s2):
        """Distancia Levenshtein [>=0]"""
        try:
            if len(s1) < len(s2):
                return self.levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]
        except Exception as e:
            logger.error(f"Levenshtein error: {str(e)}")
            return 0

    def unieval(self, text):
        """Promedio de palabras por oración"""
        try:
            sentences = sent_tokenize(text)
            words = self.preprocess(text)
            total_words = len(words)
            total_sentences = len(sentences)
            return total_words / total_sentences if total_sentences > 0 else 0
        except Exception as e:
            logger.error(f"UniEval error: {str(e)}")
            return 0

    def flesch_reading_ease(self, text):
        """Flesch Reading Ease [0-100]"""
        try:
            return textstat.flesch_reading_ease(text)
        except Exception as e:
            logger.error(f"Flesch error: {str(e)}")
            return 0

    def smog_index(self, text):
        """SMOG index"""
        try:
            return textstat.smog_index(text)
        except Exception as e:
            logger.error(f"SMOG error: {str(e)}")
            return 0

    def calculate_all_metrics(self, chatgpt_text, deepseek_text):
        # === SIMILITUD ===
        jaccard = self.jaccard_similarity(chatgpt_text, deepseek_text)
        cosine = self.cosine_similarity(chatgpt_text, deepseek_text)
        levenshtein_dist = self.levenshtein_distance(chatgpt_text, deepseek_text)
        max_len = max(len(chatgpt_text), len(deepseek_text), 1)
        levenshtein_sim = 1 - (levenshtein_dist / max_len)

        similarity = (jaccard + cosine + levenshtein_sim) / 3

        # === COMPLEJIDAD CHATGPT ===
        fre_chatgpt = max(0, min(self.flesch_reading_ease(chatgpt_text), 100)) / 100
        smog_chatgpt = min(self.smog_index(chatgpt_text), 20) / 20
        unieval_chatgpt = min(self.unieval(chatgpt_text), 5) / 5
        complexity_chatgpt = ((fre_chatgpt + smog_chatgpt + unieval_chatgpt) / 3) * 100

        # === COMPLEJIDAD DEEPSEEK ===
        fre_deepseek = max(0, min(self.flesch_reading_ease(deepseek_text), 100)) / 100
        smog_deepseek = min(self.smog_index(deepseek_text), 20) / 20
        unieval_deepseek = min(self.unieval(deepseek_text), 5) / 5
        complexity_deepseek = ((fre_deepseek + smog_deepseek + unieval_deepseek) / 3) * 100

        return {
            'similarity': similarity,
            'similarity_details': {
                'jaccard': jaccard,
                'cosine': cosine,
                'levenshtein': levenshtein_sim
            },
            'complexity_chatgpt': complexity_chatgpt,
            'complexity_deepseek': complexity_deepseek,
            'details_chatgpt': {
                'fre': fre_chatgpt,
                'smog': smog_chatgpt,
                'unieval': unieval_chatgpt
            },
            'details_deepseek': {
                'fre': fre_deepseek,
                'smog': smog_deepseek,
                'unieval': unieval_deepseek
            }
        }
