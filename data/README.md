# Kaggle Phishing Dataset

## 📥 Setup Instructions

### Step 1: Download Dataset from Kaggle

**Recommended Dataset (Most Popular):**
🔗 **[Phishing Website Detection](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detection)**
- **Author**: Eswar Chandt
- **Size**: ~88,000 samples
- **Columns**: `url`, `label` (0 = legitimate, 1 = phishing)
- **Best for**: Production-grade model training

**Alternative Datasets:**
- [URL Phishing Detection](https://www.kaggle.com/datasets/shayneobrien/url-phishing-detection) - 11,000 URLs
- [Phishing Domain Detection Dataset](https://www.kaggle.com/datasets/zhijin33/phishing-detection) - Various features
- Search Kaggle for more recent datasets

### Step 2: Place Dataset File
1. Download the CSV file from Kaggle
2. Extract if compressed
3. Place it in this directory (`brain-api/data/`)
4. Name it `phishing_dataset.csv` (or use a custom path)

### Step 3: Expected CSV Format
Your dataset CSV should contain at least these two columns:

| Column | Values | Description |
|--------|--------|-------------|
| `url` (or `link`, `website`) | string | The URL to classify |
| `label` (or `class`, `classification`) | 0 or 1 | 0 = Legitimate, 1 = Phishing |

**Example:**
```
url,label
https://www.google.com,0
https://www.amazon.com,0
https://phishing-example.tk,1
https://fake-bank.ml,1
```

### Step 4: Run Training
```bash
cd brain-api
python train_model.py
```

Or with custom dataset path:
```bash
python train_model.py "data/my_dataset.csv"
```

The script will automatically:
- Load your real dataset
- Extract features from each URL
- Train the Random Forest model
- Save the trained model to `models/` directory

## 🎯 Recommended Datasets (Ranked by Quality)

| Dataset | Link | Samples | Best For |
|---------|------|---------|----------|
| **Phishing Website Detection** | [Eswar Chandt](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detection) | ~88,000 | Production model ⭐⭐⭐ |
| URL Phishing Detection | [Shayne O'Brien](https://www.kaggle.com/datasets/shayneobrien/url-phishing-detection) | ~11,000 | Good balance |
| Phishing Domain Detection | [Zhijin](https://www.kaggle.com/datasets/zhijin33/phishing-detection) | ~6,000 | Testing |

## 📚 Dataset Attribution & Citations

### Primary Dataset Used:
**Phishing Website Detection Dataset** by Eswar Chandt

**Citation Format (APA):**
```
Chandt, E. (2022). Phishing Website Detection [Dataset]. 
Kaggle. Retrieved from https://www.kaggle.com/datasets/eswarchandt/phishing-website-detection
```

**Citation Format (BibTeX):**
```bibtex
@dataset{phishing_website_detection,
  author = {Chandt, Eswar},
  title = {Phishing Website Detection},
  year = {2022},
  publisher = {Kaggle},
  howpublished = {\url{https://www.kaggle.com/datasets/eswarchandt/phishing-website-detection}}
}
```

**License**: The dataset is typically provided under the CC0 1.0 Universal (Public Domain) license.

## ✅ Important Notes
- ✔️ The more data you have, the better the model performance
- ✔️ Aim for at least 10,000 samples minimum
- ✔️ Ensure your CSV is properly formatted before training
- ✔️ Column names are automatically detected (case-insensitive)
- ✔️ Always review the dataset's license and usage terms on Kaggle
- ✔️ If you use this in academic/professional work, cite the original dataset authors

