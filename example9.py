#!/usr/bin/env python3
import scripthelper

logger = scripthelper.bootstrap()
state = scripthelper.PersistedState(processed_id=0, to_remember=[])

state.processed_id += 1
state.to_remember.append(f"Element {state.processed_id}")
while len(state.to_remember) > 2:
    state.to_remember.pop(0)

logger.info(f"Processing item #{state.processed_id}")
for item in state.to_remember:
    logger.info(f"- {item}")
