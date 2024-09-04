import random
from core.models import llm_gen, cosine_similarity, gen_embedding
from core.utils import extract_json, check_json


class Cluster:  # 记录任务的类
    def __init__(self, duplicate_wrapper):
        # similar question share the same key
        self.questions = dict()  # id -> [question]
        self.q_emb = dict()  # id -> [emb]
        self.q2id = dict()  # question -> [cluster_id, question_id]

        self.qa_pairs = dict()  # id -> [question, answer]
        self.cp_emb = dict()  # id -> [emb]
        self.cp2id = dict()  # question -> [cluster_id, question_id]

        self.duplicate_wrapper = duplicate_wrapper
        self.upstream_pointer = dict()  #  child_cluster_id -> parent_cluster_id

    # 记录带依赖标记的问题簇
    async def add_item(self, question, emb=None, hyperthres=0.9):
        randindex = [random.randint(0, len(q) - 1) for q in self.questions.values()]
        qsamples = [q[randindex[i]] for i, q in enumerate(self.questions.values())]
        saved_emb = [e[randindex[i]] for i, e in enumerate(self.q_emb.values())]

        emb = await gen_embedding(question) if emb is None else emb
        emb = emb[0] if len(emb) == 1 else emb

        similarities = [cosine_similarity(emb, e) for e in saved_emb]
        indices = [i for i, sim in enumerate(similarities) if sim > hyperthres]
        # print(question)
        # for s in similarities:
        #     print(s, "\t", qsamples[similarities.index(s)])

        if len(indices) == 0:  # 无相似问题，新建一个问题簇
            self.q_emb[len(self.questions)] = [emb]
            self.q2id[question] = [len(self.questions), 0]
            self.questions[len(self.questions)] = [question]
            return "new question"
        elif len(indices) == 1:  # 仅有一个相似问题，直接加入对应问题簇
            self.q_emb[indices[0]].append(emb)
            self.q2id[question] = [indices[0], len(self.questions[indices[0]])]
            self.questions[indices[0]].append(question)
            return similarities, indices, [qsamples[id] for id in indices]

        # 在余弦相似度粗筛的基础上判定是否存在重叠任务
        candidates = [qsamples[i] for i in indices]
        prompt = self.duplicate_wrapper(
            target=question, questions=candidates, n=len(candidates)
        )
        response = await llm_gen(
            prompt=prompt,
            format="json",
        )
        result = extract_json(response)
        if not check_json(result, ["duplicate_question"]):  # retry
            return await self.add_item(question=question, emb=emb)

        q = result["duplicate_question"]
        if q in candidates:
            idx = candidates.index(q)
            self.q_emb[indices[idx]].append(emb)
            self.q2id[question] = [indices[idx], len(self.questions[indices[idx]])]
            self.questions[indices[idx]].append(question)
        elif q is None:
            self.q_emb[len(self.questions)] = [emb]
            self.q2id[question] = [len(self.questions), 0]
            self.questions[len(self.questions)] = [question]
            return "new question"
        else:  # retry
            await self.add_item(question=question, emb=emb)
        return similarities, indices, [qsamples[id] for id in indices]

    # 记录完整的问题-答案对
    def add_qa_pair(self, question, answer, emb=None, hyperthres=0.9):
        randindex = [random.randint(0, len(q) - 1) for q in self.qa_pairs.values()]
        saved_emb = [e[randindex[i]] for i, e in enumerate(self.cp_emb.values())]

        emb = emb[0] if len(emb) == 1 else emb

        # 计算相似度
        similarities = [cosine_similarity(emb, e) for e in saved_emb]

        # 检查similarities是否为空
        if len(similarities) == 0:
            self.cp_emb[len(self.qa_pairs)] = [emb]
            self.cp2id[question] = [len(self.qa_pairs), 0]
            self.qa_pairs[len(self.qa_pairs)] = [[question, answer]]
            return "new question"

        # 找到最高的相似度及其索引
        max_similarity = max(similarities)
        index = similarities.index(max_similarity)

        # 检查最高相似度是否大于hyperthres
        if max_similarity <= hyperthres:
            self.cp_emb[len(self.qa_pairs)] = [emb]
            self.cp2id[question] = [len(self.qa_pairs), 0]
            self.qa_pairs[len(self.qa_pairs)] = [[question, answer]]
            return "new question"
        else:
            self.cp_emb[index].append(emb)
            self.cp2id[question] = [index, len(self.qa_pairs[index])]
            self.qa_pairs[index].append([question, answer])
            return similarities, index, self.qa_pairs[index]

        # 记录问题间的依赖关系

    # 记录带依赖标记的问题簇间的依赖关系
    def add_pointer(self, upstream_question, downstream_question):

        upstream_cluster_id = self.q2id[upstream_question][0]
        downstream_cluster_id = self.q2id[downstream_question][0]

        if downstream_cluster_id not in self.upstream_pointer:
            self.upstream_pointer[downstream_cluster_id] = []
        if upstream_cluster_id not in self.upstream_pointer[downstream_cluster_id]:
            self.upstream_pointer[downstream_cluster_id].append(upstream_cluster_id)
