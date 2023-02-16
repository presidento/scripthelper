#!/usr/bin/env python3
import scripthelper

logger = scripthelper.bootstrap()
state = scripthelper.PersistedState(processed_id=0)

state.processed_id += 1
logger.info(f"Processing item #{state.processed_id}")
