import logging

logging.basicConfig(
	filename="error.log",
	level=logging.ERROR,
	format="%(asctime)s - %(levelname)s - %(message)s",
	encoding="utf-8"
)

logger = logging.getLogger("atlas_backend")