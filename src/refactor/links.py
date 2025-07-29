import datetime
import logging
from datetime import date
from typing import List, Tuple, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag  # type: ignore

# Настройка логирования
logger = logging.getLogger(__name__)

# Константы для парсинга
LINK_SELECTOR = "a.accordeon-inner__item-title.link.xls"
OIL_XLS_PATTERN = "/upload/reports/oil_xls/oil_xls_"
BASE_URL = "https://spimex.com"
DATE_FORMAT = "%Y%m%d"


def extract_date_from_href(href: str) -> Optional[date]:
    """
    Извлекает дату из ссылки на файл бюллетеня.

    Args:
        href: Ссылка на файл

    Returns:
        Дата из ссылки или None если не удалось извлечь
    """
    try:
        # Извлекаем дату из формата oil_xls_YYYYMMDD.xls
        date_str = href.split("oil_xls_")[1][:8]
        return datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    except (IndexError, ValueError) as e:
        logger.warning(f"Не удалось извлечь дату из ссылки {href}: {e}")
        return None


def is_valid_oil_xls_link(href: str) -> bool:
    """
    Проверяет, является ли ссылка валидной ссылкой на бюллетень.

    Args:
        href: Ссылка для проверки

    Returns:
        True если ссылка валидна
    """
    if not href:
        return False

    # Убираем query параметры
    href = href.split("?")[0]

    return OIL_XLS_PATTERN in href and href.endswith(".xls")


def normalize_url(href: str) -> str:
    """
    Нормализует URL, добавляя базовый домен если нужно.

    Args:
        href: Относительный или абсолютный URL

    Returns:
        Абсолютный URL
    """
    if href.startswith("http"):
        return href
    return urljoin(BASE_URL, href)


def filter_links_by_date_range(
    links: List[Tuple[str, date]], start_date: date, end_date: date
) -> List[Tuple[str, date]]:
    """
    Фильтрует ссылки по диапазону дат.

    Args:
        links: Список кортежей (url, date)
        start_date: Начальная дата
        end_date: Конечная дата

    Returns:
        Отфильтрованные ссылки
    """
    filtered_links = []

    for url, file_date in links:
        if start_date <= file_date <= end_date:
            filtered_links.append((url, file_date))
        else:
            logger.debug(
                f"Ссылка {url} вне диапазона дат " f"{start_date} - {end_date}"
            )

    return filtered_links


def parse_page_links(
    html: str, start_date: date, end_date: date, url: str
) -> List[Tuple[str, date]]:
    """
    Парсит ссылки на бюллетени с одной страницы.

    Функция извлекает ссылки на XLS файлы бюллетеней, извлекает даты
    из имен файлов и фильтрует по указанному диапазону дат.

    Args:
        html: HTML содержимое страницы
        start_date: Начальная дата для фильтрации
        end_date: Конечная дата для фильтрации
        url: URL страницы (используется для логирования)

    Returns:
        Список кортежей (url, date) для валидных ссылок в диапазоне дат

    Example:
        >>> parse_page_links(html, date(2024, 1, 1), date(2024, 1, 31),
        ...                  "https://example.com")
        [('https://spimex.com/upload/reports/oil_xls/oil_xls_20240101.xls',
        ...  datetime.date(2024, 1, 1))]
    """
    results: List[Tuple[str, date]] = []

    try:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

        logger.debug(f"Найдено {len(links)} ссылок на странице {url}")

    except Exception as e:
        logger.error(f"Ошибка при парсинге HTML: {e}")
        return results

    for link in links:
        if not isinstance(link, Tag):
            continue

        href = link.get("href")
        if not is_valid_oil_xls_link(href):
            continue

        # Очищаем href от query параметров
        href = href.split("?")[0]

        # Извлекаем дату
        file_date = extract_date_from_href(href)
        if file_date is None:
            continue

        # Нормализуем URL
        normalized_url = normalize_url(href)

        results.append((normalized_url, file_date))

    # Фильтруем по диапазону дат
    filtered_results = filter_links_by_date_range(results, start_date, end_date)

    logger.info(f"Найдено {len(filtered_results)} ссылок в диапазоне дат")

    return filtered_results
