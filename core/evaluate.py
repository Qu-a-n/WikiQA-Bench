import re
import string
from collections import Counter
from core.models import llm_gen
from core.utils import extract_json
from core.prompt import MathPrompt


# 针对不同的数据集，定义不同的评价函数
def HotpotQAEval(prediction: str, groundtruth: str):
    em = exact_match_score(prediction, groundtruth)
    f1 = f1_score(prediction, groundtruth)[0]
    return em, f1


def Game24Eval(question: str, solution: str):
    if not isinstance(solution, str):
        return "No solution."
    if isinstance(solution, str):
        numbers_in_solution = re.findall(r"\d+", solution)
        counter1 = Counter(numbers_in_solution)
        counter2 = Counter(question.split(" "))
        if counter1 != counter2:
            return "The number of times using the digits is incorrect."
        try:
            solution = eval(solution)
        except:
            return "Illegal expression."
    if abs(solution - 24) < 1e-6:  # 考虑浮点数的精度问题
        return True
    return "The result is not 24."


async def MathEval(question: str, solution: str, prediction: str):
    prompt = MathPrompt().selfeval(question, solution, prediction)
    response = await llm_gen(prompt, format="json")
    result = extract_json(response)
    if isinstance(result, str):
        return await MathEval(question, solution, prediction)
    return result["judgement"]


def normalize_answer(s):

    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def exact_match_score(prediction, ground_truth):
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def f1_score(prediction, ground_truth):
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)

    ZERO_METRIC = (0, 0, 0)

    if (
        normalized_prediction in ["yes", "no", "noanswer"]
        and normalized_prediction != normalized_ground_truth
    ):
        return ZERO_METRIC
    if (
        normalized_ground_truth in ["yes", "no", "noanswer"]
        and normalized_prediction != normalized_ground_truth
    ):
        return ZERO_METRIC

    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return ZERO_METRIC
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall
