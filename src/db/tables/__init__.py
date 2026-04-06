# It's important to preserve right modules import order
# SQLite3 does not support "use_alter=True"
# Entities with FK must point on already imported table
from src.db.tables.main_base import MainBase
from src.db.tables.table_source_providers import SourceProviderDBEntity
from src.db.tables.table_parsers import ParserDBEntity
from src.db.tables.table_news_items import NewsItemDBEntity
from src.db.tables.table_sources import SourceDBEntity
from src.db.tables.table_scanning_history import ScanningHistoryDBEntity
