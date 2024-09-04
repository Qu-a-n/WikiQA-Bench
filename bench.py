from core.models import llm_gen, close_session
from core.utils import extract_json, check_json
from prompt import WikiQA
import asyncio
import pandas as pd
from datetime import datetime


def check_stage(result: dict) -> bool :
    if not check_json(result, ["answer"]):
        return False
    return True

def write_list_to_tsv(path, data):
    with open(path, "w", encoding="utf8") as fout:
        for row in data:
            fout.write('\t'.join(map(str, row)) + '\n')

async def stage(question, table, id):
    prompt = WikiQA().prompt_for_bsl(question=question, table=table)
    response = await llm_gen(prompt=prompt, format='json')
    result = extract_json(response)
    if not check_stage(result=result):
        return await stage(question=question, table=table, id=id)
    print(id)
    return [id, result["answer"]]


async def main(start, end):
    dateset = "data/training.tsv"
    fin = open(dateset, "r", encoding="utf8")
    header = fin.readline().rstrip("\n").split("\t")
    qs, ts_path, idx = [], [], []
    for id, line in enumerate(fin):
        if start <= id < end:
            stuff = dict(zip(header, line.rstrip("\n").split("\t")))
            qs.append(stuff["utterance"])
            ts_path.append(stuff["context"])
            idx.append(stuff["id"])
    callings = [
        stage(
            question=qs[id], 
            table=pd.read_csv(ts_path[id]).to_string(index=False),
            id=idx[id]
        ) 
    for id in range(len(qs))
    ]
    responses = await asyncio.gather(*callings)
    await close_session()
    await asyncio.sleep(0.25)
    current_time = datetime.now().strftime("%m-%d-%H-%M")
    out_path = f"log/train/{current_time}_{start}_{end}.tsv"
    write_list_to_tsv(out_path, responses)
    return

if __name__ == "__main__":
    asyncio.run(main(0,50))


    
    

