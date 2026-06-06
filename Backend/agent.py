from playwright.sync_api import sync_playwright

def search_tasks(query):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(f"https://www.bing.com/search?q={query}")

        page.wait_for_timeout(4000)

        links = page.locator("a").evaluate_all("""
        elements => elements.map(el => ({
            text: el.innerText,
            href: el.href
        }))
        """)

        for item in links:

            text = item["text"]
            href = item["href"]

            if text and href.startswith("http"):

                results.append({
                    "title": text,
                    "link": href
                })

            if len(results) == 5:
                break

        detailed_info = []

        for result in results[:3]:

            try:

                detail_page = browser.new_page()

                detail_page.goto(result["link"])

                detail_page.wait_for_timeout(3000)

                content = detail_page.locator("body").inner_text()

                short_content = content[:700]

                skills = []

                keywords = [
                    "Java",
                    "Python",
                    "React",
                    "SQL",
                    "JavaScript",
                    "HTML",
                    "CSS"
                ]

                for word in keywords:

                    if word.lower() in content.lower():

                        skills.append(word)

                detailed_info.append({

                    "title": result["title"],

                    "link": result["link"],

                    "description": short_content,

                    "skills": skills
                })

                detail_page.close()

            except:

                pass

        browser.close()

    best_result = ""

    if len(detailed_info) > 0:

        best_result = detailed_info[0]["title"]

    summary = f"""
Hello! I searched the web for '{query}'.

I explored multiple websites automatically and found the most relevant opportunities for you.

Recommended Result:
{best_result}

You can check the links below for more details.
"""

    return {

        "results": detailed_info,

        "summary": summary
    }