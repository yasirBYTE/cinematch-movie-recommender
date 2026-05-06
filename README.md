# 🎬 CineMatch — AI Movie Recommendation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cinematch-movie-recommender-rgwn9ndqrw7kmrrgyapzcd.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.6.1-orange?logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

> **Tell us one movie you love. We'll find five more you'll obsess over.**

CineMatch is a content-based movie recommendation system that suggests 5 similar movies based on what you pick — no login, no ratings, no history needed. Just pure AI-driven content matching.

---

## 🚀 Live Demo

👉 **[Try CineMatch Live](https://cinematch-movie-recommender-rgwn9ndqrw7kmrrgyapzcd.streamlit.app/)**

![CineMatch UI Preview](https://image.tmdb.org/t/p/w500/qhPtAc1TKbMPqNvcdXSOn9Bn7hZ.jpg)

---

## ✨ Features

- 🎯 **Content-Based Filtering** — Recommends movies based on genres, cast, crew, keywords & overview
- 🖼️ **4,797 Real Movie Posters** — Fetched and cached from the TMDB API
- 🎨 **Cinematic UI** — Animated live background with floating particles and orbs
- ⚡ **Instant Results** — Pre-computed similarity matrix for zero-latency recommendations
- 📱 **Responsive Design** — Works on desktop and mobile
- 🌐 **Deployed on Streamlit Cloud** — Accessible anywhere, anytime

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| ML / NLP | Scikit-learn (CountVectorizer + Cosine Similarity) |
| Poster Fetching | TMDB API |
| Frontend / UI | Streamlit |
| Deployment | Streamlit Cloud |
| Version Control | Git + GitHub |

---

## 🧠 How It Works

```
Movie Title
    │
    ▼
Extract Features
(overview + genres + cast + crew + keywords)
    │
    ▼
Build Tag Vector
(CountVectorizer → 5000 features)
    │
    ▼
Compute Cosine Similarity
(4806 × 4806 matrix)
    │
    ▼
Return Top 5 Similar Movies
```

1. **Data Collection** — TMDB 5000 Movies dataset (Kaggle)
2. **Feature Engineering** — Each movie is converted into a unified "tag" string by combining its overview, genres, cast (top 3), director, and keywords
3. **Vectorization** — Tags are converted into numerical vectors using `CountVectorizer` with 5,000 max features
4. **Similarity** — Cosine Similarity is computed across all 4,806 movie vectors to build a similarity matrix
5. **Recommendation** — Given a movie, the top 5 most similar movies are returned by ranking similarity scores

---

## 📁 Project Structure

```
cinematch-movie-recommender/
│
├── app.py                  # Main Streamlit application
├── movie_list.pkl          # Processed movies dataframe (pickled)
├── similarity.pkl          # Precomputed cosine similarity matrix (pickled)
├── poster_dict.pkl         # Pre-cached TMDB poster URLs (pickled)
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Run Locally

### Prerequisites
- Python 3.10+
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/yasirBYTE/cinematch-movie-recommender.git
cd cinematch-movie-recommender
```

**2. Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

**5. Open in browser**
```
http://localhost:8501
```

---

## 📊 Dataset

- **Source:** [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle
- **Size:** 4,806 movies
- **Features used:** `title`, `overview`, `genres`, `keywords`, `cast`, `crew`

---

## 🔧 Key Challenges & Solutions

| Challenge | Solution |
|---|---|
| Stale `movie_id` values in dataset causing broken posters | Switched to title-based TMDB API search |
| TMDB API blocked on institutional networks | Pre-downloaded all 4,797 poster URLs into `poster_dict.pkl` |
| `similarity.pkl` too large for standard GitHub push | Used Git LFS for large file tracking |
| Pickle version mismatch on Streamlit Cloud | Pinned `scikit-learn==1.6.1` in `requirements.txt` |
| Deciding which features give best recommendations | Tested combinations of tags; overview + genres + cast + crew + keywords gave optimal results |

---

## 🙌 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie database and poster API
- [Kaggle](https://www.kaggle.com/) for the dataset
- [Streamlit](https://streamlit.io/) for the deployment platform
- [Google Fonts](https://fonts.google.com/) for Bebas Neue & Plus Jakarta Sans

---

## 👤 Author

**Md Yasir Junaid**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/yasir-junaid-890376294/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/yasirBYTE)

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify and distribute.

---

<p align="center">
  Made with ❤️ and Python &nbsp;·&nbsp; 
  <a href="https://cinematch-movie-recommender-rgwn9ndqrw7kmrrgyapzcd.streamlit.app/">Live Demo</a>
</p>