def analyze_site(soup, text):
    issues = []
    priority = []

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    if not title:
        issues.append("Missing Title")
        priority.append(("Title", "HIGH"))

    meta = soup.find("meta", attrs={"name": "description"})
    description = meta["content"].strip() if meta and meta.get("content") else ""
    if not description:
        issues.append("Missing Meta Description")
        priority.append(("Meta Description", "HIGH"))

    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0:
        issues.append("Missing H1")
        priority.append(("H1", "MEDIUM"))

    word_count = len(text.split())
    if word_count < 300:
        issues.append("Low Content")
        priority.append(("Content", "HIGH"))

    h2_tags = soup.find_all("h2")
    if len(h2_tags) == 0:
        issues.append("Weak Structure")
        priority.append(("Headings", "MEDIUM"))

    score = 100 - (len(issues) * 15)
    if score < 0:
        score = 0

    return {
        "score": score,
        "issues": issues,
        "priority": priority
    }
