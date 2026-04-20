def analyze_site(soup, text):

    score = 0
    issues = []
    priority = []

    title = soup.title.string if soup.title else ""
    meta = soup.find("meta", attrs={"name": "description"})
    meta = meta["content"] if meta else ""

    h1 = soup.find("h1")
    h2 = len(soup.find_all("h2"))
    words = len(text.split())

    if not title:
        issues.append("Missing Title")
        priority.append(("Title", "HIGH"))
    else:
        score += 20

    if not meta:
        issues.append("Missing Meta Description")
        priority.append(("Meta", "HIGH"))
    else:
        score += 20

    if not h1:
        issues.append("Missing H1")
        priority.append(("H1", "MEDIUM"))
    else:
        score += 15

    if words < 800:
        issues.append("Low Content")
        priority.append(("Content", "HIGH"))
    else:
        score += 15

    if h2 < 2:
        issues.append("Weak Structure")
        priority.append(("Headings", "MEDIUM"))
    else:
        score += 10

    return {
        "score": score,
        "issues": issues,
        "priority": priority
    }
