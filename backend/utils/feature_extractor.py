import re
from urllib.parse import urlparse
import tldextract

class FeatureExtractor:
    def __init__(self):
        self.suspicious_keywords = ['login', 'verify', 'secure', 'bank', 'update', 'account', 'signin', 'ebayisapi', 'webscr']

    def extract_features(self, url):
        """
        Extract features from a URL for phishing detection.
        Returns a dictionary of features.
        """
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        try:
            parsed_url = urlparse(url)
            domain_info = tldextract.extract(url)
        except Exception:
            return None

        features = {}

        # 1. URL Length
        features['url_length'] = len(url)

        # 2. Having IP Address (IPv4 or IPv6)
        ip_pattern = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
        features['have_ip'] = 1 if re.search(ip_pattern, url) else 0

        # 3. Number of dots
        features['count_dots'] = url.count('.')

        # 4. Number of hyphens
        features['count_hyphens'] = url.count('-')

        # 5. Number of @ symbol
        features['count_at'] = url.count('@')

        # 6. Number of double slashes (redirection)
        features['count_double_slash'] = url.count('//') - 1 if url.count('//') > 0 else 0

        # 7. Number of subdirectories
        features['count_dir'] = parsed_url.path.count('/')

        # 8. Number of queries
        features['count_query'] = parsed_url.query.count('&') + (1 if parsed_url.query else 0)

        # 9. Presence of HTTPS
        features['use_https'] = 1 if parsed_url.scheme == 'https' else 0

        # 10. URL shortening services
        shortening_services = r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|' \
                              r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|' \
                              r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|' \
                              r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|' \
                              r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|' \
                              r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|' \
                              r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net'
        features['is_shortened'] = 1 if re.search(shortening_services, url) else 0

        # 11. Count sensitive words
        features['count_sensitive_words'] = sum(1 for word in self.suspicious_keywords if word in url.lower())

        # 12. Domain components
        features['domain_length'] = len(domain_info.domain)
        features['subdomain_count'] = len(domain_info.subdomain.split('.')) if domain_info.subdomain else 0

        return features

if __name__ == "__main__":
    extractor = FeatureExtractor()
    test_url = "https://www.google.com/search?q=phishing"
    print(extractor.extract_features(test_url))
