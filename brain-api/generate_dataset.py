"""
🧠 SYNTHETIC PHISHING DATASET GENERATOR

Generates a realistic phishing URL dataset for local training.
Can be replaced with actual Kaggle dataset later.
"""

import csv
import random
import os

# Legitimate domain patterns
LEGITIMATE_DOMAINS = [
    "google.com", "facebook.com", "twitter.com", "amazon.com", "netflix.com",
    "github.com", "stackoverflow.com", "linkedin.com", "reddit.com", "youtube.com",
    "wikipedia.org", "medium.com", "dev.to", "notion.so", "slack.com",
    "microsoft.com", "apple.com", "adobe.com", "atlassian.com", "jira.com",
    "trello.com", "asana.com", "figma.com", "sketch.com", "invision.com",
    "mailchimp.com", "stripe.com", "paypal.com", "twilio.com", "sendgrid.com",
    "heroku.com", "vercel.com", "netlify.com", "firebase.com", "aws.amazon.com",
    "cloud.google.com", "azure.microsoft.com", "ibm.com", "oracle.com", "salesforce.com"
]

# Suspicious domains (phishing patterns)
PHISHING_DOMAINS = [
    "gogle.com", "facbook.com", "twtter.com", "amazn.com", "netflix-secure.com",
    "github-verify.com", "stackoverflow-confirm.com", "linkedin-login.com",
    "paypa1.com", "g00gle.com", "facebookl.com", "amaz0n.com",
    "login-google.ru", "verify-amazon.tk", "confirm-facebook.ga",
    "secure-paypal.top", "update-twitter.info", "validate-netflix.xyz",
    "support-steam.pw", "authenticate-apple.cf", "verify-apple-id.gq",
    "account-update-microsoft.ml", "security-confirm-bank.tk",
    "urgent-verify-account.ga", "click-here-now.top", "limited-time-offer.tk",
    "congratulations-winner.ml", "claim-reward-now.ga", "verify-identity.cf"
]

# URL paths for legitimate sites
LEGITIMATE_PATHS = [
    "/", "/home", "/about", "/contact", "/products", "/services", "/pricing",
    "/docs", "/api", "/blog", "/help", "/support", "/faq", "/login",
    "/register", "/dashboard", "/settings", "/profile", "/account",
]

# URL paths for phishing sites
PHISHING_PATHS = [
    "/verify", "/confirm", "/update", "/action", "/secure", "/validate",
    "/authenticate", "/signin", "/login", "/account-recovery", "/verify-account",
    "/confirm-identity", "/urgent-action", "/required-update", "/security-check",
    "/claim-reward", "/verify-payment", "/update-billing",
]

def generate_legitimate_urls(count=2000):
    """Generate realistic legitimate URLs"""
    urls = []
    for _ in range(count):
        domain = random.choice(LEGITIMATE_DOMAINS)
        path = random.choice(LEGITIMATE_PATHS)
        subdomain = random.choice(["", "www.", "mail.", "api.", "dev.", "staging."])
        
        # Mix of HTTPS and HTTP
        protocol = "https://" if random.random() > 0.1 else "http://"
        
        # Add query params occasionally
        if random.random() > 0.7:
            param = f"?id={random.randint(100, 99999)}"
        else:
            param = ""
        
        url = f"{protocol}{subdomain}{domain}{path}{param}"
        urls.append((url, 0))  # Label 0 = Legitimate
    
    return urls

def generate_phishing_urls(count=2000):
    """Generate realistic phishing URLs"""
    urls = []
    phishing_techniques = [
        "ip_address",
        "misspelled_domain",
        "suspicious_tld",
        "suspicious_chars",
        "long_url",
        "at_symbol",
        "multiple_redirects"
    ]
    
    for _ in range(count):
        technique = random.choice(phishing_techniques)
        
        if technique == "ip_address":
            # IP-based URLs (common phishing indicator)
            ip = f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
            url = f"http://{ip}/login"
        
        elif technique == "misspelled_domain":
            # Misspelled legitimate domains
            domain = random.choice(PHISHING_DOMAINS)
            protocol = "https://"
            path = random.choice(PHISHING_PATHS)
            url = f"{protocol}{domain}{path}"
        
        elif technique == "suspicious_tld":
            # Suspicious top-level domains
            suspicious_tlds = [".ru", ".tk", ".ml", ".ga", ".cf", ".top", ".xyz", ".gq"]
            domain = random.choice(PHISHING_DOMAINS)
            tld = random.choice(suspicious_tlds)
            url = f"https://{domain.split('.')[0]}{tld}/login"
        
        elif technique == "at_symbol":
            # URLs with @ symbol (redirect to real URL)
            real_domain = random.choice(LEGITIMATE_DOMAINS)
            fake_domain = random.choice(PHISHING_DOMAINS)
            url = f"https://{fake_domain}@{real_domain}/verify"
        
        elif technique == "long_url":
            # Excessively long URLs
            domain = random.choice(PHISHING_DOMAINS)
            padding = "x" * random.randint(100, 200)
            url = f"https://{domain}/verify/{padding}/confirm"
        
        elif technique == "multiple_redirects":
            # URLs with multiple slashes/paths
            domain = random.choice(PHISHING_DOMAINS)
            paths = "/".join([random.choice(PHISHING_PATHS).strip("/") for _ in range(3)])
            url = f"https://{domain}/{paths}/login"
        
        else:
            domain = random.choice(PHISHING_DOMAINS)
            url = f"https://{domain}/verify"
        
        urls.append((url, 1))  # Label 1 = Phishing
    
    return urls

def generate_dataset(output_path="data/phishing_dataset.csv", total_samples=10000):
    """Generate and save the synthetic dataset"""
    
    print(f"🔨 Generating synthetic phishing dataset ({total_samples} samples)...")
    
    # Generate equal balanced classes
    legit_count = total_samples // 2
    phishing_count = total_samples // 2
    
    legitimate_urls = generate_legitimate_urls(legit_count)
    phishing_urls = generate_phishing_urls(phishing_count)
    
    # Combine and shuffle
    all_urls = legitimate_urls + phishing_urls
    random.shuffle(all_urls)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to CSV
    print(f"💾 Writing to {output_path}...")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'label'])  # Header
        writer.writerows(all_urls)
    
    print(f"✅ Dataset generated!")
    print(f"   📊 Total samples: {len(all_urls)}")
    print(f"   ✅ Legitimate URLs: {legit_count}")
    print(f"   ⚠️  Phishing URLs: {phishing_count}")
    print(f"   📁 Saved to: {output_path}")
    print(f"\n💡 Note: This is synthetic data for development. Replace with Kaggle dataset for production.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
        total_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
        generate_dataset(output_path, total_samples)
    else:
        generate_dataset()
