import json
from multiprocessing import Pool
import iterate
if __name__ == "__main__":
    state = json.load(open(iterate.POP))
    with Pool(5) as p:
        out = p.map(iterate._eval, state["pop"], chunksize=1)
    pop = []
    for chain, summary, results, err in out:
        if err:
            print("ERR", err[-300:]); continue
        chain["summary"], chain["results"] = summary, iterate.compact_full(results)
        iterate.log({"round": state["round"], "id": chain["id"], "name": chain["name"], "category": chain["category"], "parent": chain.get("parent"),
                     "mutation": "rescore (M7 implementation fix)", "steps": chain["steps"], "summary": summary, "renders": iterate.compact(results)})
        pop.append(chain)
        print(chain["category"], chain["id"], summary)
    state["pop"] = pop
    json.dump(state, open(iterate.POP, "w"), default=str)
