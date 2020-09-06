import asyncio
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from time import sleep
import pandas as pd
from ..app_settings import MAPPING_OUTPUT_FOLDER, CLEANED_FILE_FOLDER

def long_task(t):
    logging.info("2. t: %s", t)
    sleep(3)
    logging.info("4. t: %s", t)
    return t ** 2


async def generate_mapping_pairs() -> dict:
    loop = asyncio.get_running_loop()
    # executor = ThreadPoolExecutor(max_workers=4)
    with ThreadPoolExecutor() as pool:
        # result = await asyncio.gather(loop.run_in_executor(executor, long_task, 10))
        # TODO substitute with actual library call
        result = await loop.run_in_executor(pool, long_task, 10)
        print(f"Mapping results: [{result}]")

    # TODO pass results to cleaner function
    path = Path.cwd().joinpath(MAPPING_OUTPUT_FOLDER, CLEANED_FILE_FOLDER, "cleaned_input.csv")
    df = pd.read_csv(path, usecols=["source_term", "mapped_term"])
    gb = df.groupby('source_term')['mapped_term'].apply(list).to_dict()
    return gb