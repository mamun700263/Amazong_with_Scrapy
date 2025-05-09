from logger import get_logger
from amazon.items import AmazonItem
logger = get_logger('amazon')
def list_items(response):
    try:
        logger.info("🔍 Locating product list items...")
        items = response.css('div[role="listitem"]')
        if not items:
            logger.warning("⚠️ No product list items found")
            return []
        logger.info(f"✅ Found {len(items)} product items")
        return items
    except Exception as e:
        logger.error(f"❌ Error locating list items: {e}")
        return []

def extract_text(item, selector, attr=None):
    try:
        el = item.css(selector)
        if not el:
            return ""
        return el.attrib[attr] if attr else el.css(selector).get(default="").strip()
    except Exception as e:
        logger.warning(f"⚠️ Extraction failed for {selector}: {e}")
        return ""

def title_extractor(item):
    title = item.css("h2 span::text").get()
    if title:
        logger.debug(f"📝 Title: {title.strip()}")
    return title.strip() if title else ""

def image_extractor(item):
    return item.css("img::attr(src)").get(default="")

def link_extractor(item, response):
    link = item.css("a::attr(href)").get()
    return response.urljoin(link) if link else ""

def extractor(response):
    items = list_items(response)
    count = 0

    for item in items:
        title = title_extractor(item)
        print(title)
        if not title:
            continue  # skip items with no title
        product = AmazonItem()
        product['name'] = title
        product['image_url'] = image_extractor(item)
        product['product_url'] = link_extractor(item, response)
        count += 1
        print(count)
        yield product
    logger.info(f"✅ Extracted {count} products successfully")

def pagination(response, base_url="https://www.amazon.com"):
    logger.debug("📄 Checking for pagination...")
    try:
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if not next_page:
            logger.warning("⚠️ No next page link found")
            return None
        next_url = f"{base_url}{next_page}"
        logger.info(f"➡️ Found next page URL: {next_url}")
        return next_url
    except Exception as e:
        logger.error(f"❌ Pagination error: {e}")
        return None
