import streamlit as st
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- UI STYLE ----------------
st.set_page_config(page_title="Smart SEO AI", layout="centered")

st.markdown("""
<style>
body { background-color: #0e1117; }
h1 { color: #00ffcc; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Smart SEO AI SaaS Tool")

# ---------------- AI SUGGESTIONS ----------------
def ai_suggestions(issues):
    suggestions = []

    for issue in issues:
        if "Title" in issue:
            suggestions.append("Add SEO optimized title (50-60 chars).")
        elif "Meta" in issue:
            suggestions.append("Add proper meta description (150-160 chars).")
        elif "H1" in issue:
            suggestions.append("Add one clear H1 tag.")
        elif "Content" in issue:
            suggestions.append("Increase high-quality content (300+ words).")
        elif "Images" in issue:
            suggestions.append("Add ALT text for images.")
        elif "Links" in issue:
            suggestions.append("Add internal linking structure.")

    if not suggestions:
        suggestions.append("SEO is excellent. Focus on backlinks & updates.")

    return suggestions


# ---------------- ANALYZER ----------------
def analyze_site(soup, text, url=""):
    issues = []

    title = soup.title.get_text() if soup.title else ""
    if not title:
        issues.append("Missing Title")

    meta = soup.find("meta", attrs={"name": "description"})
    if not meta:
        issues.append("Missing Meta Description")

    h1 = soup.find_all("h1")
    if len(h1) == 0:
        issues.append("Missing H1")

    word_count = len(text.split())
    if word_count < 300:
        issues.append("Low Content")

    images = soup.find_all("img")
    missing_alt = sum(1 for img in images if not img.get("alt"))

    if missing_alt > 0:
        issues.append("Images Missing ALT Text")

    links = soup.find_all("a")
    if len(links) < 5:
        issues.append("Too Few Internal Links")

    score = max(0, 100 - len(issues) * 10)

    return {
        "score": score,
        "issues": issues,
        "suggestions": ai_suggestions(issues),
        "word_count": word_count,
        "images": len(images),
        "links": len(links)
    }


# ---------------- PDF REPORT ----------------
def generate_pdf(data):
    file = "seo_report.pdf"
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SMART SEO AI REPORT", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"SEO Score: {data['score']}/100", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Issues:", styles["Heading2"]))
    for i in data["issues"]:
        story.append(Paragraph(f"- {i}", styles["Normal"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("AI Suggestions:", styles["Heading2"]))
    for s in data["suggestions"]:
        story.append(Paragraph(f"- {s}", styles["Normal"]))

    doc.build(story)
    return file


# ---------------- URL FIX ----------------
def fix_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url


# ---------------- INPUT ----------------
url = st.text_input("Enter Website URL")

if st.button("Analyze"):

    if url:
        url = fix_url(url)
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            data = analyze_site(soup, soup.get_text(), url)

            # ---------------- SCORE ----------------
            st.subheader(f"🎯 SEO Score: {data['score']}/100")

            st.write("## ⚠️ Issues")
            for i in data["issues"]:
                st.write("•", i)

            st.write("## 🤖 AI Suggestions")
            for s in data["suggestions"]:
                st.write("👉", s)

            # ---------------- GRAPH ----------------
            st.write("## 📊 SEO Dashboard")

            fig, ax = plt.subplots()
            ax.bar(["SEO Score", "Issues"], [data["score"], len(data["issues"])])
            ax.set_title("SEO Performance Overview")
            ax.set_ylabel("Value")
            st.pyplot(fig)

            # ---------------- PDF ----------------
            st.write("## 📄 Download Report")

            pdf_file = generate_pdf(data)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📥 Download SEO Report",
                    data=f,
                    file_name="seo_report.pdf",
                    mime="application/pdf"
                )

        except:
            st.error("Error loading website")

    else:
        st.warning("Enter URL first")
