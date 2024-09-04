import re
import json
from typing import Union
import pickle
import logging
import itertools
import asyncio
from sklearn.cluster import DBSCAN
from collections import Counter
from collections import defaultdict
from core.models import gen_embedding


class TaskMemory(dict):  # default: None
    # 记录子任务的结果，结果有三种情况，False表示不可解决，None表示还没有解决但也没有被验证为不可解决，str表示表达式（解决结果）
    def __init__(self):
        self.successor = defaultdict(list)
        self.predecessor = defaultdict(list)
        self.successed = list()
        for i in range(1, 14):  # game24涉及到的数
            self.__setitem__((i, i), str(i))

    def validate_key(self, key):
        if isinstance(key, list):
            key = tuple(key)
        if not isinstance(key, tuple) or len(key) not in [2, 3, 4, 5]:
            return KeyError("Key must be a tuple of two, three, four or five elements.")
        return tuple(sorted(key[:-1]) + [key[-1]])

    def __setitem__(self, key, value):
        key = self.validate_key(key)
        if isinstance(key, Exception):
            return key
        if self[key] is not None:
            return
        if isinstance(value, str):
            self.successed.append(key)
            if len(key) == 3:  # 找前缀
                for task in self.successed:
                    if task[-1] not in key[:-1]:
                        continue
                    if self.predecessor.get(key, None) is None:
                        self.predecessor[key] = list()
                    if self.successor.get(task, None) is None:
                        self.successor[task] = list()
                    self.successor[task].append(key)
                    self.predecessor[key].append(task)
            for task in self.successed:  # 找后缀
                if len(task) != 3:
                    continue
                if key[-1] not in task[:-1]:
                    continue
                if self.predecessor.get(task, None) is None:
                    self.predecessor[task] = list()
                if self.successor.get(key, None) is None:
                    self.successor[key] = list()
                self.successor[key].append(task)
                self.predecessor[task].append(key)
        super(TaskMemory, self).__setitem__(key, value)

    def __getitem__(self, key):
        key = self.validate_key(key)
        if isinstance(key, Exception):
            return key
        try:
            if len(key) == 2:
                if key[0] != key[1]:
                    return False
            return super(TaskMemory, self).__getitem__(key)
        except KeyError:
            return None

    def get_successor(self, key):
        key = self.validate_key(key)
        if isinstance(key, Exception):
            return key
        return self.successor[key]

    def get_predecessor(self, key):
        key = self.validate_key(key)
        if isinstance(key, Exception):
            return key
        return self.predecessor[key]


class PlanMemory(dict):  # default: None
    # Record the results of decomposition
    def validate_key(self, key):
        if isinstance(key, list) and all(
            isinstance(item, list) or isinstance(item, tuple) for item in key
        ):
            key = tuple(tuple(item) for item in key)
        if not isinstance(key, tuple) or len(key) != 3:
            return KeyError("Key must be a tuple of three elements.")
        # Ensure each element of the key is a tuple
        if not all(isinstance(item, tuple) for item in key):
            return KeyError("Each element of the key must be a tuple.")
        # Sort the first two elements of each sub-tuple
        return tuple(tuple(sorted(item[:-1])) + (item[-1],) for item in key)

    def __setitem__(self, key, value: Union[None, bool, str] = None):
        key = self.validate_key(key)
        if not isinstance(key, tuple):
            return key
        super(PlanMemory, self).__setitem__(key, value)

    def __getitem__(self, key):
        key = self.validate_key(key)
        if not isinstance(key, tuple):
            return key
        try:
            return super(PlanMemory, self).__getitem__(key)
        except KeyError:
            return None


class Memory:
    def __init__(self):
        self.task_memory = TaskMemory()
        self.plan_memory = PlanMemory()

    def validate_key(self, key):
        if not isinstance(key, tuple) or len(key) == 1:
            return KeyError("Key must be a tuple of more than one element.")
        return tuple(sorted(key[:-1]) + [key[-1]])


def unsorted_equal(tuple1, tuple2):
    if isinstance(tuple1, list):
        tuple1 = tuple(tuple1)
    if isinstance(tuple2, list):
        tuple2 = tuple(tuple2)
    result = sorted(tuple1) == sorted(tuple2)
    return result


def extract_json(string):  # 从response中提取json数据，提取失败则返回错误信息
    try:  # json mode的output
        string = string.strip()
        json_data = json.loads(string)
        return json_data
    except Exception as e:
        return str(e)


def check_json(json_obj, keys: list):
    if not isinstance(json_obj, dict):
        return False
    for key in keys:
        if key not in json_obj.keys():
            return False
    return True


def remove_redundancy(expr: str):
    # 用栈来处理括号匹配
    stack = []
    for i, c in enumerate(expr):
        if c == "(":
            stack.append(i)
        elif c == ")":
            right = i
            left = stack.pop()
            # 如果删除这两个括号没有改变运算结果，说明这个括号是冗余的
            try:
                temp_expr = expr[:left] + expr[left + 1 : right] + expr[right + 1 :]
                if eval(temp_expr) == eval(expr):
                    return remove_redundancy(temp_expr)
            except ZeroDivisionError:
                continue
    return expr


def calculate(expression, mem):
    used_numbers = []

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        flag = []
        intermidiate = []
        if right[-1] == 0:
            used_numbers.append(right[0])
            flag.append(left[0])
        else:
            intermidiate = right[0]
        if left[-1] == 0:
            used_numbers.append(left[0])
            flag.append(right[0])
        else:
            intermidiate = left[0]
        right = right[0]
        left = left[0]
        value = eval(f"{left}{operator}{right}")
        if abs(right - int(right)) < 1e-6:
            right = int(right)
        if abs(left - int(left)) < 1e-6:
            left = int(left)
        if abs(value - int(value)) < 1e-6:
            value = int(value)
        values.append([value, 1])
        mem.task_memory[(left, right, value)] = get_valid_expression(
            f"{left}{operator}{right}"
        )
        if len(flag) == 0:  # 说明四个数字都用过了
            mem.task_memory[[used_numbers] + [value]] = get_valid_expression(
                f"{left}{operator}{right}"
            )
        elif len(flag) == 1:  # 说明至少有两个数字用过了
            final_expr = get_valid_expression(f"{left}{operator}{right}")
            log = []
            for task, expr in mem.task_memory.items():
                if task[-1] == intermidiate and all(
                    [num in used_numbers for num in task[:-1]]
                ):
                    replaced_num = task[-1]
                    expr_to_replace = expr
                    # 使用正则表达式确保只替换完整的数字
                    final_expr = re.sub(
                        rf"\b{replaced_num}\b", expr_to_replace, final_expr, count=1
                    )
                    log.append([task[:-1] + None, final_expr])  # TODO: so hard!
            for task, expr in log:
                mem.task_memory[task] = expr
        elif len(flag) == 2:  # 不用理
            pass

    def greater_precedence(op1, op2):
        precedences = {"+": 1, "-": 1, "*": 2, "/": 2, "(": 0, ")": 0}
        return precedences[op1] >= precedences[op2]

    def tokenize(expression):
        tokens = []
        number = ""
        for char in expression:
            if char in "0123456789.":
                number += char
            else:
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append(char)
        if number:
            tokens.append(number)
        return tokens

    operators = []
    values = []
    tokens = tokenize(expression)
    for i, token in enumerate(tokens):
        if all([t in "0123456789." for t in token]):
            tokens[i] = [token, 0]  # 0表示是表达式里本身就有的数字
        else:
            tokens[i] = [token, -1]  # -1表示是表达式里的运算符
    for token in tokens:
        if token[0] == "(":
            operators.append(token[0])
        elif token[0] == ")":
            while operators and operators[-1] != "(":
                apply_operator(operators, values)
            operators.pop()  # Pop the '('
        elif token[0] in "*/+-":
            while (
                operators
                and operators[-1] in "*/+-"
                and greater_precedence(operators[-1], token[0])
            ):
                apply_operator(operators, values)
            operators.append(token[0])
        else:
            values.append(
                [int(token[0]), token[1]]
            )  # Use float to handle decimal numbers
    while operators:
        apply_operator(operators, values)
    if abs(values[0][0] - 24) > 1e-6:
        print(expression, values[0][0])


def get_valid_expression(expression):  # 如果expression==""则会返回False
    try:
        expression = expression.split("=")[0]
        expression = re.sub(r"[^0-9+\-*/().]", "", expression)
        expression.replace("+-", "-")
        expression.replace("--", "+")
        expression = remove_redundancy(expression)
        return expression if expression != "" else False
    except:
        return False


def list_sub(lst, elements_to_remove):
    for elem in elements_to_remove:
        if elem in lst:
            lst.remove(elem)
    return lst


def get_majority(lst: list):
    if not lst:
        return None
    count = Counter(lst)
    max_count = max(count.values())
    most_frequent = [elem for elem, freq in count.items() if freq == max_count]
    return most_frequent[0]


def get_distribution(lst: list):
    if not lst:
        return None
    count = Counter(lst)
    return count


def find_pos(lst, target):
    return [i for i, x in enumerate(lst) if x == target]


async def get_embedding_distribution(lst: list, verbose=False):  # 效果一般
    if not lst:
        return None
    if len(lst) > 20:
        task = [gen_embedding(l) for l in lst]
        results = await asyncio.gather(*task)
        lst = [result[0] for result in results]
    else:
        lst = await gen_embedding(lst)
    clusterer = DBSCAN(eps=0.4, min_samples=1)
    clusterer.fit(lst)
    if verbose:
        print(clusterer.labels_)
    return clusterer.labels_


def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02d}h:{int(minutes):02d}m:{int(seconds):02d}s"


def save_memory(memory, file_path="log/game24/memory.pkl"):
    with open(file_path, "wb") as file:
        pickle.dump(memory, file)


def load_memory(file_path="log/game24/memory.pkl"):
    with open(file_path, "rb") as file:
        memory = pickle.load(file)
    return memory


def get_logger(mode="a+"):
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG

    file_handler = logging.FileHandler("log/running/game24.log", mode=mode)
    file_handler.setLevel(logging.DEBUG)  # 设置文件处理器的日志级别为DEBUG

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 设置控制台处理器的日志级别为INFO

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def nonNegInt(expr):  # 检测负数和小数
    value = eval(expr)
    if value > 0 and abs(value - int(value)) < 1e-6:
        return True


def trainset_memory():
    mem = Memory()

    def add_to_memory(a, b, operator):
        expression = f"{a}{operator}{b}"
        if operator == "/" and b == 0:
            return
        if nonNegInt(expression):
            result = int(eval(expression))
            mem.task_memory[(a, b, result)] = expression

    for a, b in itertools.product(range(1, 14), repeat=2):
        add_to_memory(a, b, "+")
        add_to_memory(a, b, "-")
        add_to_memory(b, a, "-")
        add_to_memory(a, b, "*")
        add_to_memory(a, b, "/")
        add_to_memory(b, a, "/")

    def add_complex_to_memory(a, b, c, expr, operator):
        if operator in ("+", "*"):
            newexpr = get_valid_expression(f"({expr}){operator}{c}")
            if not nonNegInt(newexpr):
                return
            result = int(eval(newexpr))
            mem.task_memory[(a, b, c, result)] = newexpr
            add_to_memory(c, result, operator)
        elif operator == "-":
            newexpr = get_valid_expression(f"{c}-({expr})")
            if nonNegInt(newexpr):
                result = int(eval(newexpr))
                mem.task_memory[(a, b, c, result)] = newexpr
                add_to_memory(c, result, operator)

            if nonNegInt(newexpr):
                newexpr = get_valid_expression(f"({expr})-{c}")
                result = int(eval(newexpr))
                mem.task_memory[(a, b, c, result)] = newexpr
                add_to_memory(result, c, operator)

        elif operator == "/":
            if c != 0:
                newexpr = get_valid_expression(f"({expr})/{c}")
                if nonNegInt(newexpr):
                    result = int(eval(newexpr))
                    mem.task_memory[(a, b, c, result)] = newexpr
                    add_to_memory(result, c, "/")
            if eval(expr) != 0:
                newexpr = get_valid_expression(f"{c}/({expr})")
                if nonNegInt(newexpr):
                    result = int(eval(newexpr))
                    mem.task_memory[(a, b, c, result)] = newexpr
                    add_to_memory(c, result, "/")

    for a, b, c in itertools.product(range(1, 14), repeat=3):
        for expr in [
            v for k, v in mem.task_memory.items() if unsorted_equal(k[:-1], (a, b))
        ]:
            add_complex_to_memory(a, b, c, expr, "+")
            add_complex_to_memory(a, b, c, expr, "-")
            add_complex_to_memory(a, b, c, expr, "*")
            add_complex_to_memory(a, b, c, expr, "/")
    for a in range(1, 14):
        for b in range(14, 38):
            # if a == 2 and b == 24:
            #     print("debug")
            add_to_memory(a, b, "+")
            add_to_memory(a, b, "-")
            add_to_memory(b, a, "-")
            add_to_memory(a, b, "*")
            add_to_memory(a, b, "/")
            add_to_memory(b, a, "/")
    return mem


def trainset_memory():
    json_obj = json.load(open("log/game24/trainmem.json", "r"))
    mem = Memory()
    for obj in json_obj:
        expressions = [
            get_valid_expression(expression) for expression in obj["Answers"]
        ]
        for expression in expressions:
            calculate(expression, mem)
    return mem
