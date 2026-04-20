def analyze_site(soup, text, url=""):
    issues = []
    priority = []

    title_tag = soup.find("title")
    title = title_tag.get_text().strip() if title_tag else ""

    if not title:
        issues.append("Missing Title")
        priority.append(("Title", "HIGH"))

    meta_desc = soup.find("meta", attrs={"name": "description"})
    og_desc = soup.find("meta", attrs={"property": "og:description"})

    description = ""
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()
    elif og_desc and og_desc.get("content"):
        description = og_desc["content"].strip()

    if not description:
        issues.append("Missing Meta Description")
        priority.append(("Meta Description", "HIGH"))

    h1 = soup.find_all("h1")
    if len(h1) == 0:
        issues.append("Missing H1")
        priority.append(("H1", "HIGH"))

    h2 = soup.find_all("h2")
    if len(h2) == 0:
        issues.append("Missing Headings Structure")
        priority.append(("Headings", "MEDIUM"))

    word_count = len(text.split())
    if word_count < 300:
        issues.append("Low Content")
        priority.append(("Content", "HIGH"))

    images = soup.find_all("img")
    missing_alt = 0
    for img in images:
        if not img.get("alt"):
            missing_alt += 1

    if missing_alt > 0:
        issues.append("Images Missing Alt Text")
        priority.append(("Images SEO", "MEDIUM"))

    links = soup.find_all("a")

    if len(links) < 5:
        issues.append("Too Few Internal Links")
        priority.append(("Internal Links", "MEDIUM"))

    score = 100
    score -= len(issues) * 10

    if not title:
        score -= 15

    if not description:
        score -= 15

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
        "links": len(links)
    }
