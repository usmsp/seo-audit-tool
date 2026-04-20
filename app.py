import streamlit as st
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- AI SUGGESTIONS ----------------
def ai_suggestions(issues):
    suggestions = []
    for issue in issues:
        if "Title" in issue:
            suggestions.append("Add SEO-friendly title (50-60 chars).")
        elif "Meta" in issue:
            suggestions.append("Add meta description (150-160 chars).")
        elif "H1" in issue:
            suggestions.append("Add proper H1 tag.")
        elif "Content" in issue:
            suggestions.append("Increase high-quality content (300+ words).")
    if not suggestions:
        suggestions.append("SEO is good. Focus on backlinks & content updates.")
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

    score = max(0, 100 - len(issues) * 15)

    return {
        "score": score,
        "issues": issues,
        "suggestions": ai_suggestions(issues),
        "word_count": word_count
    }

# ---------------- PDF REPORT ----------------
def generate_pdf(data):
    file = "seo_report.pdf"
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SEO REPORT", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Score: {data['score']}", styles["Normal"]))
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

# ---------------- CHATBOT ----------------
def chatbot_response(msg, data):
    msg = msg.lower()

    if "score" in msg:
        return f"Your SEO score is {data['score']}"

    if "fix" in msg:
        return "Fix: " + ", ".join(data["issues"])

    if "help" in msg:
        return "Improve title, meta description and content."

    return "Ask about score, fixes, or SEO tips."

# ---------------- STREAMLIT UI ----------------
st.title("🚀 Smart SEO AI PRO Tool")

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

            data = analyze_site(soup, soup.get_text(), url)

            st.subheader(f"🎯 Score: {data['score']}/100")

            st.write("## Issues")
            for i in data["issues"]:
                st.write("•", i)

            st.write("## AI Suggestions")
            for s in data["suggestions"]:
                st.write("👉", s)

            # ---------------- DASHBOARD ----------------
            st.write("## 📊 Dashboard")

            labels = ["Good", "Issues"]
            values = [data["score"], 100 - data["score"]]

            fig, ax = plt.subplots()
            ax.bar(labels, values)
            st.pyplot(fig)

            # ---------------- PDF ----------------
            if st.button("Download PDF Report"):
                file = generate_pdf(data)
                with open(file, "rb") as f:
                    st.download_button("Download Report", f, file_name="seo_report.pdf")

            # ---------------- CHATBOT ----------------
            st.write("## 🤖 SEO Chatbot")

            user_msg = st.text_input("Ask SEO question")

            if user_msg:
                reply = chatbot_response(user_msg, data)
                st.write("🤖", reply)

        except:
            st.error("Error loading website")

    else:
        st.warning("Enter URL")
