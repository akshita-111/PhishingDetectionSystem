import re
from urllib.parse import urlparse
from typing import Dict


def extract_features(url: str) -> Dict[str, float]:
    """
    Extract numerical features from a URL for phishing detection.
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dictionary containing numerical features
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
        
        features = {
            # Basic URL features
            'url_length': float(len(url)),
            'domain_length': float(len(domain)),
            'path_length': float(len(path)),
            'query_length': float(len(query)),
            
            # Character-based features
            'has_at_symbol': float(1 if '@' in url else 0),
            'has_double_slash': float(1 if '//' in url.replace('://', '') else 0),
            'has_dash': float(1 if '-' in domain else 0),
            'has_underscore': float(1 if '_' in url else 0),
            'has_percent': float(1 if '%' in url else 0),
            'has_tilde': float(1 if '~' in url else 0),
            
            # Count-based features
            'dot_count': float(url.count('.')),
            'dash_count': float(url.count('-')),
            'underscore_count': float(url.count('_')),
            'percent_count': float(url.count('%')),
            'ampersand_count': float(url.count('&')),
            'equals_count': float(url.count('=')),
            'question_count': float(url.count('?')),
            'hash_count': float(url.count('#')),
            
            # Domain-specific features
            'subdomain_count': float(len(domain.split('.')) - 1) if domain else 0.0,
            'domain_digit_count': float(sum(c.isdigit() for c in domain)),
            'domain_letter_count': float(sum(c.isalpha() for c in domain)),
            
            # Path features
            'path_segment_count': float(len([seg for seg in path.split('/') if seg])),
            'path_digit_count': float(sum(c.isdigit() for c in path)),
            
            # Suspicious patterns
            'has_ip_address': float(1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain) else 0),
            'has_port': float(1 if ':' in domain and not domain.startswith('http') else 0),
            'has_https': float(1 if url.startswith('https://') else 0),
            'has_http': float(1 if url.startswith('http://') else 0),
            
            # TLD features
            'tld_length': float(len(domain.split('.')[-1])) if '.' in domain else 0.0,
            'has_suspicious_tld': float(1 if any(tld in domain.lower() for tld in ['.tk', '.ml', '.ga', '.cf']) else 0),
            
            # Special character ratio
            'special_char_ratio': float(len(re.findall(r'[^a-zA-Z0-9]', url)) / len(url)) if url else 0.0,
            'digit_ratio': float(sum(c.isdigit() for c in url) / len(url)) if url else 0.0,
        }
        
        return features
        
    except Exception as e:
        # Return default features if URL parsing fails
        return {
            'url_length': 0.0,
            'domain_length': 0.0,
            'path_length': 0.0,
            'query_length': 0.0,
            'has_at_symbol': 0.0,
            'has_double_slash': 0.0,
            'has_dash': 0.0,
            'has_underscore': 0.0,
            'has_percent': 0.0,
            'has_tilde': 0.0,
            'dot_count': 0.0,
            'dash_count': 0.0,
            'underscore_count': 0.0,
            'percent_count': 0.0,
            'ampersand_count': 0.0,
            'equals_count': 0.0,
            'question_count': 0.0,
            'hash_count': 0.0,
            'subdomain_count': 0.0,
            'domain_digit_count': 0.0,
            'domain_letter_count': 0.0,
            'path_segment_count': 0.0,
            'path_digit_count': 0.0,
            'has_ip_address': 0.0,
            'has_port': 0.0,
            'has_https': 0.0,
            'has_http': 0.0,
            'tld_length': 0.0,
            'has_suspicious_tld': 0.0,
            'special_char_ratio': 0.0,
            'digit_ratio': 0.0,
        }
