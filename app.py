import streamlit as st
import pickle
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_resource
def load_data():
    movies     = pickle.load(open("movie_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    poster_dict = pickle.load(open("poster_dict.pkl", "rb")) if os.path.exists("poster_dict.pkl") else {}
    return movies, similarity, poster_dict

movies, similarity, poster_dict = load_data()

# ─────────────────────────────────────────────
# RECOMMENDATION LOGIC
# ─────────────────────────────────────────────
def recommend(movie_title):
    idx = movies[movies["title"] == movie_title].index[0]
    distances = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)
    names, posters = [], []
    for i in distances[1:6]:
        name = movies.iloc[i[0]]["title"]
        names.append(name)
        posters.append(poster_dict.get(name))
    return names, posters

# ─────────────────────────────────────────────
# CSS + ANIMATED BACKGROUND
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── LIVE ANIMATED BACKGROUND ── */
.stApp {
    background: #05050f;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f0f0f0;
    overflow-x: hidden;
}

/* Canvas sits behind everything */
#cinema-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
}

/* Floating orbs */
.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.18;
    animation: drift linear infinite;
    pointer-events: none;
    z-index: 0;
}
.orb1 { width: 500px; height: 500px; background: #dc143c; top: -100px; left: -100px; animation-duration: 18s; }
.orb2 { width: 400px; height: 400px; background: #7b00ff; top: 40%; right: -150px; animation-duration: 24s; animation-delay: -8s; }
.orb3 { width: 350px; height: 350px; background: #dc143c; bottom: -80px; left: 30%; animation-duration: 20s; animation-delay: -4s; }
.orb4 { width: 250px; height: 250px; background: #ff6b35; top: 60%; left: 10%; animation-duration: 15s; animation-delay: -12s; }

@keyframes drift {
    0%   { transform: translate(0, 0) scale(1); }
    25%  { transform: translate(60px, -40px) scale(1.05); }
    50%  { transform: translate(30px, 80px) scale(0.95); }
    75%  { transform: translate(-50px, 30px) scale(1.02); }
    100% { transform: translate(0, 0) scale(1); }
}

/* Film grain overlay */
.grain {
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='1'/%3E%3C/svg%3E");
    opacity: 0.025;
    animation: grain-shift 0.5s steps(1) infinite;
    pointer-events: none;
    z-index: 1;
}
@keyframes grain-shift {
    0%  { transform: translate(0,0); }
    20% { transform: translate(-3%, -5%); }
    40% { transform: translate(5%, 2%); }
    60% { transform: translate(-2%, 7%); }
    80% { transform: translate(4%, -3%); }
    100%{ transform: translate(0,0); }
}

/* Scanlines */
.scanlines {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.03) 2px,
        rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 1;
}

/* ── STREAMLIT OVERRIDES ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    position: relative;
    z-index: 2;
}

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 80px 20px 50px;
    position: relative;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(220,20,60,0.1);
    border: 1px solid rgba(220,20,60,0.3);
    color: #ff6b6b;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    padding: 7px 20px;
    border-radius: 100px;
    margin-bottom: 28px;
    animation: fadeInDown 0.8s ease forwards;
}
.dot-pulse {
    width: 6px; height: 6px;
    background: #dc143c;
    border-radius: 50%;
    animation: pulse 1.5s ease infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.6); }
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(72px, 14vw, 160px);
    line-height: 0.85;
    letter-spacing: 0.04em;
    color: #fff;
    position: relative;
    animation: fadeInUp 0.9s ease forwards;
}
.hero-title span {
    background: linear-gradient(135deg, #ff6b6b 0%, #dc143c 40%, #a00020 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-tagline {
    font-size: 16px;
    font-weight: 300;
    color: #666;
    margin-top: 20px;
    letter-spacing: 0.05em;
    animation: fadeInUp 1s ease 0.2s both;
}
.hero-tagline b { color: #999; font-weight: 500; }

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── TICKER TAPE ── */
.ticker-wrap {
    overflow: hidden;
    background: rgba(220,20,60,0.08);
    border-top: 1px solid rgba(220,20,60,0.15);
    border-bottom: 1px solid rgba(220,20,60,0.15);
    padding: 10px 0;
    margin: 20px 0 40px;
}
.ticker {
    display: flex;
    white-space: nowrap;
    animation: ticker 30s linear infinite;
    gap: 0;
}
.ticker-item {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #dc143c;
    padding: 0 40px;
    opacity: 0.7;
}
.ticker-item::before { content: '✦  '; }
@keyframes ticker {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}

/* ── SEARCH SECTION ── */
.search-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 0 30px 40px;
}
.search-heading {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.search-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    color: #f0f0f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 15px !important;
    transition: all 0.3s !important;
    backdrop-filter: blur(10px) !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: rgba(220,20,60,0.5) !important;
    background: rgba(220,20,60,0.05) !important;
    box-shadow: 0 0 0 3px rgba(220,20,60,0.1) !important;
}
.stSelectbox label { display: none !important; }

/* Button */
div.stButton > button {
    background: linear-gradient(135deg, #dc143c, #a00020) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 18px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 22px !important;
    letter-spacing: 0.15em !important;
    width: 100% !important;
    margin-top: 14px !important;
    box-shadow: 0 8px 30px rgba(220,20,60,0.4), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 16px 50px rgba(220,20,60,0.55) !important;
}
div.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* ── STATS ── */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 50px;
    padding: 20px 0 40px;
}
.stat {
    text-align: center;
    position: relative;
}
.stat::after {
    content: '';
    position: absolute;
    right: -25px;
    top: 50%;
    transform: translateY(-50%);
    width: 1px;
    height: 30px;
    background: rgba(255,255,255,0.07);
}
.stat:last-child::after { display: none; }
.stat-n {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 38px;
    background: linear-gradient(135deg, #fff, #dc143c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.stat-l {
    font-size: 9px;
    font-weight: 600;
    color: #333;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── RESULTS ── */
.results-section {
    max-width: 1280px;
    margin: 0 auto;
    padding: 20px 30px 80px;
}
.results-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #dc143c;
    margin-bottom: 6px;
}
.results-movie-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(28px, 5vw, 52px);
    letter-spacing: 0.05em;
    color: #fff;
    line-height: 1;
    margin-bottom: 30px;
}
.results-movie-name::after {
    content: '';
    display: block;
    width: 50px;
    height: 3px;
    background: linear-gradient(90deg, #dc143c, transparent);
    margin-top: 10px;
}

/* ── MOVIE CARDS ── */
.card-title {
    padding: 14px 12px 16px;
    text-align: center;
    font-size: 13px;
    font-weight: 600;
    color: #ccc;
    line-height: 1.4;
    min-height: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0e0e1c;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.no-poster {
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #0e0e1c, #1a1a2e);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    font-size: 40px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.no-poster-label {
    font-size: 10px;
    color: #2a2a2a;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 600;
}

/* Card wrapper styling via column */
div[data-testid="column"] {
    transition: transform 0.3s ease !important;
}

/* Image styling */
div[data-testid="stImage"] img {
    border-radius: 0 !important;
    display: block !important;
    width: 100% !important;
}

/* ── FOOTER ── */
.site-footer {
    text-align: center;
    padding: 30px 20px;
    border-top: 1px solid rgba(255,255,255,0.04);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #222;
    position: relative;
    z-index: 2;
}
.site-footer span { color: #dc143c; }

/* Spinner */
div[data-testid="stSpinner"] > div {
    border-top-color: #dc143c !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LIVE BACKGROUND ELEMENTS
# ─────────────────────────────────────────────
st.markdown("""
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>
<div class="orb orb4"></div>
<div class="grain"></div>
<div class="scanlines"></div>

<!-- Particle canvas -->
<canvas id="cinema-bg"></canvas>
<script>
(function() {
    const canvas = document.getElementById('cinema-bg');
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    function Particle() {
        this.reset();
    }
    Particle.prototype.reset = function() {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.r = Math.random() * 1.2 + 0.3;
        this.vx = (Math.random() - 0.5) * 0.3;
        this.vy = -Math.random() * 0.5 - 0.1;
        this.alpha = Math.random() * 0.5 + 0.1;
        this.color = Math.random() > 0.7 ? '#dc143c' : '#ffffff';
    };
    Particle.prototype.update = function() {
        this.x += this.vx;
        this.y += this.vy;
        this.alpha -= 0.0008;
        if (this.y < -10 || this.alpha <= 0) this.reset();
    };

    for (let i = 0; i < 120; i++) particles.push(new Particle());

    function draw() {
        ctx.clearRect(0, 0, W, H);
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;
            ctx.fill();
            p.update();
        });
        ctx.globalAlpha = 1;
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">
        <div class="dot-pulse"></div>
        AI-Powered · Content Based Filtering
    </div>
    <div class="hero-title">CINE<span>MATCH</span></div>
    <div class="hero-tagline">
        One movie you love &nbsp;→&nbsp; <b>Five you'll obsess over</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TICKER
# ─────────────────────────────────────────────
ticker_movies = "Avatar · Inception · The Dark Knight · Interstellar · Avengers · Iron Man · The Matrix · Titanic · Jurassic Park · Pulp Fiction · Fight Club · Forrest Gump · The Godfather · Gladiator · John Wick"
ticker_doubled = "  ".join([ticker_movies] * 4)
st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker">
        {''.join(f'<span class="ticker-item">{m.strip()}</span>' for m in ticker_doubled.split('·'))}
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
    <div class="stat">
        <div class="stat-n">{len(movies):,}</div>
        <div class="stat-l">Movies</div>
    </div>
    <div class="stat">
        <div class="stat-n">{len(poster_dict):,}</div>
        <div class="stat-l">Posters</div>
    </div>
    <div class="stat">
        <div class="stat-n">5</div>
        <div class="stat-l">Picks</div>
    </div>
    <div class="stat">
        <div class="stat-n">∞</div>
        <div class="stat-l">Discovery</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEARCH
# ─────────────────────────────────────────────
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown('<div class="search-heading">Choose your movie</div>', unsafe_allow_html=True)

selected_movie = st.selectbox("", movies["title"].values)
show_btn = st.button("🎬  FIND MY MOVIES")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────
if show_btn:
    with st.spinner("Scanning the cinematic universe..."):
        names, posters = recommend(selected_movie)

    st.markdown(f"""
    <div class="results-section">
        <div class="results-eyebrow">Because you liked</div>
        <div class="results-movie-name">{selected_movie.upper()}</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5, gap="small")
    for col, name, poster in zip(cols, names, posters):
        with col:
            # Card wrapper
            st.markdown("""
            <div style="
                background:#0e0e1c;
                border-radius:16px;
                overflow:hidden;
                border:1px solid rgba(255,255,255,0.06);
                transition:all 0.3s ease;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            " onmouseover="this.style.transform='translateY(-8px)';this.style.boxShadow='0 20px 50px rgba(220,20,60,0.25)';this.style.borderColor='rgba(220,20,60,0.3)'"
              onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 20px rgba(0,0,0,0.5)';this.style.borderColor='rgba(255,255,255,0.06)'">
            """, unsafe_allow_html=True)

            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.markdown("""
                <div class="no-poster">
                    🎬
                    <div class="no-poster-label">No Poster</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card-title">{name}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    CineMatch &nbsp;·&nbsp; Powered by <span>TMDB</span> &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Content-Based Filtering
</div>
""", unsafe_allow_html=True)
