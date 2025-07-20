import aiohttp

from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.models.product_model import ProductModel


class WildberriesParser:
    BASE_URL = "https://www.wildberries.ru"

    @staticmethod
    async def parse_products(category: str, session: AsyncSession) -> None:
        """Парсинг товаров с Wildberries по категории."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        try:
            async with aiohttp.ClientSession() as client:
                search_url = f"{WildberriesParser.BASE_URL}/catalog/0/search.aspx?search={category}"
                async with client.get(search_url, headers=headers) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch {search_url}: {response.status}")
                        return
                    html = await response.text()

                soup = BeautifulSoup(html, "html.parser")
                # Обновленные селекторы для Wildberries
                products = soup.find_all("div", class_="product-card__wrapper")

                for product in products[:10]:  # Ограничиваем 10 товарами для теста
                    try:
                        name_elem = product.find("span", class_="product-card__name")
                        price_elem = product.find("span", class_="price__lower-price")
                        discount_price_elem = product.find("span", class_="price__old-price")
                        rating_elem = product.find("span", class_="product-card__rating")
                        reviews_elem = product.find("span", class_="product-card__count")

                        name = name_elem.text.strip() if name_elem else ""
                        price = (
                            int(price_elem.text.replace("₽", "").replace(" ", "").strip())
                            if price_elem
                            else 0
                        )
                        discount_price = (
                            int(discount_price_elem.text.replace("₽", "").replace(" ", "").strip())
                            if discount_price_elem
                            else None
                        )
                        rating = float(rating_elem.text.strip()) if rating_elem else None
                        reviews_count = (
                            int(reviews_elem.text.strip()) if reviews_elem else 0
                        )

                        if not name or not price:
                            continue

                        product_data = {
                            "name": name,
                            "price": price,
                            "discount_price": discount_price,
                            "rating": rating,
                            "reviews_count": reviews_count,
                            "category": category,
                        }
                        db_product = ProductModel(**product_data)
                        session.add(db_product)
                        await session.commit()
                        logger.info(f"Saved product: {name}")
                    except Exception as e:
                        logger.error(f"Error parsing product: {e}")
        except Exception as e:
            logger.error(f"Error fetching category {category}: {e}")
