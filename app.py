import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---------------- AI SUGGESTIONS ----------------
def ai_suggestions(issues):
    suggestions = []

    for issue in issues:
        if "Title" in issue:
            suggestions.append("Add a unique, keyword-rich title (50–60 characters).")

        elif "Meta Description" in issue:
            suggestions.append("Write a compelling meta description (150–160 characters).")

        elif "H1" in issue:
            suggestions.append("Add one clear H1 tag describing main topic.")

        elif "Headings" in issue:
            suggestions.append("Use proper H2/H3 structure for better SEO.")

        elif "Content" in issue:
            suggestions.append("Increase content length (300–800+ words).")

        elif "Images" in issue:
            suggestions.append("Add ALT text to images.")

        elif "Links" in issue:
            suggestions.append("Add internal links for better structure.")

    if not suggestions:
        suggestions.append("Great SEO! Keep maintaining content & backlinks.")

    return suggestions


# ---------------- SMART ANALYZER ----------------
def analyze_site(soup, text, url=""):
    issues = []
    priority = []

    strong_sites = ["google.com", "youtube.com", "facebook.com", "wikipedia.org"]
    is_strong_site = any(site in url.lower() for site in strong_sites)

    title = soup.title.get_text().strip() if soup.title else ""
    if not title and not is_strong_site:
        issues.append("Missing Title")
        priority.append(("Title", "HIGH"))

    meta = soup.find("meta", attrs={"name": "description"})
    og = soup.find("meta", attrs={"property": "og:description"})

    description = ""
    if meta and meta.get("content"):
        description = meta["content"].strip()
    elif og and og.get("content"):
        description = og["content"].strip()

    if not description and not is_strong_site:
        issues.append("Missing Meta Description")
        priority.append(("Meta Description", "HIGH"))

    h1 = soup.find_all("h1")
    h2 = soup.find_all("h2")

    if len(h1) == 0 and not is_strong_site:
        issues.append("Missing H1")
        priority.append(("H1", "HIGH"))

    if len(h2) == 0 and not is_strong_site:
        issues.append("Missing Headings Structure")
        priority.append(("Headings", "MEDIUM"))

    clean_text = soup.get_text(separator=" ")
    word_count = len(clean_text.split())

    if word_count < 300 and not is_strong_site:
        issues.append("Low Content")
        priority.append(("Content", "HIGH"))

    images = soup.find_all("img")
    missing_alt = sum(1 for img in images if not img.get("alt"))

    if missing_alt > 0:
        issues.append(f"{missing_alt} Images Missing Alt Text")
        priority.append(("Images SEO", "MEDIUM"))

    links = soup.find_all("a")

    if len(links) < 5:
        issues.append("Too Few Internal Links")
        priority.append(("Internal Links", "MEDIUM"))

    score = 100
    score -= len(issues) * 10
    score -= missing_alt

    if word_count < 300:
        score -= 10

    if score < 0:
        score = 0

    return {
        "score": score,
        "issues": issues,
        "priority": priority,
        "word_count": word_count,
        "images": len(images),
        "links": len(links),
        "suggestions": ai_suggestions(issues)
    }


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="SEO AI Tool", layout="centered")

st.title("🚀 Smart SEO AI Tool")

url = st.text_input("Enter Website URL")

def fix_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url


if st.button("Analyze"):

    if url:
        url = fix_url(url)

        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            result = analyze_site(soup, soup.get_text(), url)

            st.subheader(f"🎯 SEO Score: {result['score']}/100")

            st.error(f"🚨 You may be losing {100 - result['score']}% traffic!")

            st.subheader("⚠️ Issues")
            for i in result["issues"]:
                st.write("•", i)

            st.subheader("🎯 Priority")
            for item, level in result["priority"]:
                st.write(f"{item} → {level}")

            st.subheader("🤖 AI Suggestions")
            for s in result["suggestions"]:
                st.write("👉", s)

        except:
            st.error("Error loading website")

    else:
        st.warning("Enter URL")
