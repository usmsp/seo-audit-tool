import streamlit as st
import requests
from bs4 import BeautifulSoup

from utils.seo_analyzer import analyze_site

st.set_page_config(page_title="SEO Tool", layout="centered")

st.title("🚀 SEO Audit Tool")

url = st.text_input("Enter Website URL")

def fix_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url

def traffic_loss(score):
    return 100 - score

def action_plan(priority):
    plan = []
    for item, level in priority:
        if level == "HIGH":
            plan.append(f"Fix {item} immediately")
        elif level == "MEDIUM":
            plan.append(f"Improve {item} next")
        else:
            plan.append(f"Optimize {item} later")
    return plan

if st.button("Analyze"):

    if url:
        url = fix_url(url)

        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()

            result = analyze_site(soup, text)

            score = result["score"]

            st.subheader(f"🎯 SEO Score: {score}/100")

            loss = traffic_loss(score)
            st.error(f"🚨 You may be losing {loss}% traffic!")

            st.subheader("⚠️ Issues")
            for i in result["issues"]:
                st.write("•", i)

            st.subheader("🎯 Priority")
            for item, level in result["priority"]:
                st.write(f"{item} → {level}")

            st.subheader("📅 Action Plan")
            plan = action_plan(result["priority"])
            for p in plan[:3]:
                st.write("👉", p)

            # WhatsApp Button
            phone = "923075384668"
            message = f"Hi, my website score is {score}/100. Help me fix it: {url}"
            wa = f"https://wa.me/{phone}?text={message}"

            st.markdown("### 💰 Want us to fix your SEO?")
            st.markdown(f"[👉 Contact on WhatsApp]({wa})")

        except:
            st.error("Error loading website")

    else:
        st.warning("Enter URL")
