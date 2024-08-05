from bs4 import BeautifulSoup


def extract_opengraph_metadata(html_content):

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")

    # Find all OpenGraph meta tags
    og_tags = soup.find_all(
        "meta", attrs={"property": lambda x: x and x.startswith("og:")}
    )

    # Extract the content of each OpenGraph meta tag
    og_metadata = {}
    for tag in og_tags:
        property_name = tag.get("property")
        content = tag.get("content")
        og_metadata[property_name] = content

    return og_metadata
