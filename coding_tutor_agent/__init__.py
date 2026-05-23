#!/usr/bin/env python3

import logging
import threading
from .memory.database import init_db_sync
from .pipeline.store import document_store, populate_store
from . import agent

logger = logging.getLogger(__name__)

init_db_sync()


def populate_in_background():
    if document_store.count_documents() == 0:
        logger.info("Populating document store in background (this takes a few minutes)...")
        populate_store()
        logger.info(f"Document store ready — {document_store.count_documents()} chunks loaded.")


threading.Thread(target=populate_in_background, daemon=True).start()
