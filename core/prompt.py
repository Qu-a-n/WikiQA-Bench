# game24
class Game24prompt:
    def execute(self, n1, n2, n3):
        template = """We need to determine if there is an expression that can be obtained by the given two numbers: {n1} and {n2} to get the target number: {n3}. The operations we can use are addition (+), subtraction (-), multiplication (*), and division (/).
Format your response as the following json template (All the content in <> must be filled. Your response CAN'T contain "<" or ">" because you should have replaced them with the correct values.):
```json
{{
    "n1": {n1},
    "n2": {n2},
    "n3": {n3},
    "tries": {{
        "exp1":"r1={n1}+{n2}=<the the result of {n1}+{n2}>",
        "exp2":"r2={n1}-{n2}=<the the result of {n1}-{n2}>",
        "exp3":"r3={n2}-{n1}=<the the result of {n2}-{n1}>",
        "exp4":"r4={n1}*{n2}=<the the result of {n1}*{n2}>",
        "exp5":"r5={n1}/{n2}=<the the result of {n1}/{n2}>",
        "exp6":"r6={n2}/{n1}=<the the result of {n2}/{n1}>"
    }},
    "thought": {{
        "t1":"r1=< r1 > is <equal to or not equal to> {n3}",
        "t2":"r2=< r2 > is <equal to or not equal to> {n3}",
        "t3":"r3=< r3 > is <equal to or not equal to> {n3}",
        "t4":"r4=< r4 > is <equal to or not equal to> {n3}",
        "t5":"r5=< r5 > is <equal to or not equal to> {n3}",
        "t6":"r6=< r6 > is <equal to or not equal to> {n3}"
    }},
    "expression": "<if none of r1, r2, r3, r4, r5, r6 is equal to {n3}, fill in empty string "", otherwise, fill in the expression that is equal to {n3}>"
}}
Here are some examples of determining if there is an expression that can be obtained by the given two numbers {n1} and {n2} to get the target number {n3}:
[examples]
two numbers: 5, 11, target number: 7
response:
```json
{{
    "n1": 5,
    "n2": 11,
    "tries": {{
        "exp1":"r1=5+11=16", 
        "exp2":"r2=5-11=-6", 
        "exp3":"r3=11-5=6", 
        "exp4":"r4=5*11=55", 
        "exp5":"r5=5/11=0.45454545454545453", 
        "exp6":"r6=11/5=2.2"
    }},
    "thought": {{
        "t1":"r1=16 is not equal to 7",
        "t2":"r2=-6 is not equal to 7",
        "t3":"r3=6 is not equal to 7",
        "t4":"r4=55 is not equal to 7",
        "t5":"r5=0.45454545454545453 is not equal to 7",
        "t6":"r6=2.2 is not equal to 7"
    }}
    "expression": ""
}}
two numbers: 7, 14, target number: 2
response:
```json
{{
    "n1": 7,
    "n2": 14,
    "tries": {{
        "exp1":"r1=7+14=21",
        "exp2":"r2=7-14=-7",
        "exp3":"r3=14-7=7",
        "exp4":"r4=7*14=98",
        "exp5":"r5=7/14=0.5",
        "exp6":"r6=14/7=2"
    }},
    "thought": {{
        "t1":"r1=21 is not equal to 2",
        "t2":"r2=-7 is not equal to 2",
        "t3":"r3=7 is not equal to 2",
        "t4":"r4=98 is not equal to 2",
        "t5":"r5=0.5 is not equal to 2",
        "t6":"r6=2 is equal to 2"
    }}
    "expression": "14/7"
}}
```
[/examples]
"""
        prompt = template.format(n1=n1, n2=n2, n3=n3)
        return prompt

    def decompose(self, task):
        template = """You are an expert in solving mathematical puzzles. The goal of this puzzle is to find a way to manipulate a given set of numbers so that the end result is a specified target number. You can use addition (+), subtraction (-), multiplication (*), and division (/), and you must use each of the given numbers exactly once. Parentheses can be used to change the order of operations.

Here are the details:
- Numbers: {numbers}
- Target: {target}

Follow these instructions to solve the puzzle:
1. Use each of the given numbers exactly once.
2. You can use the operations +, -, *, and /.
3. You can use parentheses to change the order of operations.
4. Return the expression that evaluates to the target number and the steps you took to arrive at the solution.
5. In each step, specify the predecessor step if the numbers used in the current step were previous steps' result.

Format your response as follows:
```json
{{
    "numbers": {numbers},
    "target": {target},
    "thought_process": "<Describe your thought process and steps you took to arrive at the solution>",
    "solution": "<Fill in the mathematical expression that evaluates to the target number or return None>",
    "steps": [
        {{
            "thought_process": "<Fill in the thought process for this step>",
            "expression": "<Fill in the first step of your solution>",
            "used_numbers": [<Fill in the numbers used in this step>],
            "result": <Fill in the result of this step>,
            "remaining_numbers": [<Fill in the numbers left after this step>],
            "predecessor": []
        }},
        {{
            "thought_process": "<Fill in the thought process for this step>",
            "expression": "<Fill in the second step of your solution>",
            "used_numbers": [<Fill in the numbers used in this step>],
            "result": <Fill in the result of this step>,
            "remaining_numbers": [<Fill in the numbers left after this step>],
            "predecessor": ["<Reference to the step(s) from which the numbers were used>"]
        }},
        ...
    ]
}}
```

Here are some examples of solving the puzzle (the thought process is omitted to encourage diverse and creative thinking):
```json
{{
    "numbers": [4, 7, 13, 13],
    "target": 24,
    "thought_process": "...",
    "solution": "4*(7-(13/13))",
    "steps": [
        {{
            "thought_process": "This step should first calculate 13/13, which equals 1, because both 13 and 13 are the given numbers, so there is no predecessor for this step.",
            "expression": "13/13=1",
            "used_numbers": [13, 13],
            "result": 1,
            "remaining_numbers": [4, 7, 1],
            "predecessor": []
        }},
        {{
            "thought_process": "This step should subtract 1 from 7 to get 6. Because 1 is the result of step0, the predecessor of this step includes step0",
            "expression": "7-1=6",
            "used_numbers": [7, 1],
            "result": 6,
            "remaining_numbers": [4, 6],
            "predecessor": [0]
        }},
        {{
            "thought_process": "This step should multiply 4 by 6 to get 24. Because 6 is the result of step1, the predecessor of this step includes step1",
            "expression": "4*6=24",
            "used_numbers": [4, 6],
            "result": 24,
            "remaining_numbers": [24],
            "predecessor": [1]
        }}
    ]
}}
```
```json
{{
    "numbers": [4, 6, 13],
    "target": 28,
    "thought_process": "...",
    "solution": "4*(13-6)",
    "steps": [
        {{
            "thought_process": "This step should subtract 6 from 13 to get 7, because both 6 and 13 are the given numbers, so there is no predecessor for this step.",
            "expression": "13-6=7",
            "used_numbers": [13, 6],
            "result": 7,
            "remaining_numbers": [4, 7],
            "predecessor": []
        }},
        {{
            "thought_process": "This step should multiply 4 by 7 to get 28. Because 7 is the result of step0, the predecessor of this step includes step0",
            "expression": "4*7=28",
            "used_numbers": [4, 7],
            "result": 28,
            "remaining_numbers": [28],
            "predecessor": [0]
        }}
    ]
}}
```
```json
{{
    "numbers": [6, 8, 9, 11],
    "target": 24,
    "thought_process": "...",
    "solution": "8*6/(11-9)",
    "steps": [
        {{
            "thought_process": "This step should subtract 9 from 11 to get 2, because both 9 and 11 are the given numbers, so there is no predecessor for this step.",
            "expression": "11-9=2",
            "used_numbers": [11, 9],
            "result": 2,
            "remaining_numbers": [6, 8, 2],
            "predecessor": []
        }},
        {{
            "thought_process": "This step should multiply 8 by 6 to get 48. Because 6 and 8 are the given numbers, there is no predecessor for this step.",
            "expression": "8*6=48",
            "used_numbers": [8, 6],
            "result": 48,
            "remaining_numbers": [48, 2],
            "predecessor": []
        }},
        {{
            "thought_process": "This step should divide 48 by 2 to get 24. Because 48 is the result of step1 and 2 is the result of step0, the predecessor of this step includes step0 and step1",
            "expression": "48/2=24",
            "used_numbers": [48, 2],
            "result": 24,
            "remaining_numbers": [24],
            "predecessor": [0, 1]
        }}
    ]
}}
```
"""
        prompt = template.format(numbers=task[:-1], target=task[-1])
        return prompt

    def refine(self, task):
        template = """You are an expert in solving mathematical puzzles. The goal of this puzzle is to modify a given set of candidate numbers so that they can be used to form a specified target number through basic arithmetic operations (addition, subtraction, multiplication, and division). 

Here are the details:
- candidate numbers: [{n1}, {n2}]
- target: {target}

It is known that the given candidate numbers cannot form the target number as they are. Your task is to modify one or more of the candidate numbers so that they can be used to form the target number.

Follow these instructions to solve the puzzle:
1. Modify one or more of the given candidate numbers, but try to change only one number if possible.
2. Ensure the modified numbers can be used to form the target number using basic arithmetic operations.
3. Return the modified numbers.

Format your response as follows:
```json
{{
    "candidate_numbers": [{n1}, {n2}],
    "target": {target},
    "thought_process": "<Describe your thought process and steps you took to arrive at the modified numbers>",
    "modified_numbers": [<Fill in the modified numbers>]
}}
```

Here are some examples of refining the candidate numbers to form the target number (Not giving out thought_process is to avoid limiting your thinking, your thought process should be diverse and creative):
```json
{{
    "candidate_numbers": [9, 6],
    "target": 24,
    "thought_process": "...",
    "modified_numbers": [9, 15]
}}
```
```json
{{
    "candidate_numbers": [2, 6],
    "target": 6,
    "thought_process": "...",
    "modified_numbers": [2, 3]
}}
```
```json
{{
    "candidate_numbers": [20, 5],
    "target": 10,
    "thought_process": "...",
    "modified_numbers": [20, 2]
}}
```
```json
{{
    "candidate_numbers": [3, 7],
    "target": 7
    "thought_process": "...",
    "modified_numbers": [3, 10]
}}
```
"""
        prompt = template.format(n1=task[0], n2=task[1], target=task[2])
        return prompt

    # Other
    def selfeval(self, question, expression):
        template = """The 24 game problem is a puzzle game where the goal is to calculate the number 24 using four numbers and four arithmetic operators.
Now you are a judge, please determine whether a given expression to a specific 24 problem is correct.
The principle of judgment is: if the result of the expression is not 24, the final judgment result is "False"; if the result of the expression is 24, we then remove the operators and parentheses from the expression to obtain a same form with the question. If the sorted numbers in the question and expression are same, the final judgment result is "True"; If the sorted numbers in the question and expression are different, the final judgment result is "False". 

[examples]
question = "3 6 9 11", expression = "(3-6)*(11-9)"
Firstly we calculate the value of this expression: 3-6=-3, 11-9=2, -3*2=-6. The result is -6, not 24, so this answer is wrong. There is no need to compare the times of occurrences of numbers in the question and expression.
Finally, the judgment result is
"result": "False"

question = "6 8 9 13", expression = "6 * (13 - 9)"
Firstly we calculate the value of this expression: 13-9=4, 6*4=24. The result is 24, so we need to compare the times of occurrences of numbers in the question and expression.
Then we remove the operators and parentheses from the expression to obtain a form same with the question. The expression {expression} becomes "6 13 9".
Then we separately sort the numbers appearing in question and expression. The sorted numbers in question are: 6, 8, 9, 13. The sorted numbers in expression are: 6, 9, 13. The sorting results are different.
Finally, the judgment result is
"result": "False"

question = "8 4 8 10", expression = "(8-4)*(10-4)"
Firstly we calculate the value of this expression: 8-4=4, 10-4=6, 4*6=24. The result is 24, so we need to compare the times of occurrences of numbers in the question and expression.
Then we remove the operators and parentheses from the expression to obtain a form same with the question. The expression {expression} becomes "4 8 10 4"
Then we separately sort the numbers appearing in question and expression. The sorted numbers in question are: 4, 8, 8, 10. The sorted numbers in expression are: 4, 4, 8, 10. The sorting results are different.
Finally, the judgment result is
"result": "False"

question = "9 3 3 13", expression = "(6 - 9 + 13) * 3 - 6"
Firstly we calculate the value of this expression: 6-9=-3, -3+13=10, 10*3=30, 30-6=24. The result is 24, so we need to compare the times of occurrences of numbers in the question and expression.
Then we remove the operators and parentheses from the expression to obtain a form same with the question. The expression {expression} becomes "6 9 13 3 6"
Then we separately sort the numbers appearing in question and expression. The sorted numbers in question are: 3, 3, 9, 13. The sorted numbers in expression are: 3, 6, 6, 9, 13. The sorting results are different.
Finally, the judgment result is
"result": "False"

question = "7 8 12 16", expression = "(8 - 7) * (12 - 4) + 16"
Firstly we calculate the value of this expression: 8-7=1, 12-4=8, 1*8=8, 8+16=24. The result is 24, so we need to compare the times of occurrences of numbers in the question and expression.
Then we remove the operators and parentheses from the expression to obtain a form same with the question. The expression {expression} becomes "8 7 12 4 16"
Then we separately sort the numbers appearing in question and expression. The sorted numbers in question are: 7, 8, 12, 16. The sorted numbers in expression are: 4, 7, 8, 12, 16. The sorting results are different.
"result": "False"

question = "8 2 1 3", expression = "8 - 2) * (3 + 1)"
There expression is illegal, so the answer is incorrect.
Finally, the judgment result is
"result": "False, the expression does not conform to the formula specification."

question = "3 6 9 11",
expression = "(9-6)*(11-3)",
Firstly we calculate the value of this expression: 9-6=3, 11-3=8, 3*8=24. The result is 24, so we need to compare the times of occurrences of numbers in the question and expression.
Then we remove the operators and parentheses from the expression to obtain a form same with the question. The expression {expression} becomes "3 6 9 11"
Then we separately sort the numbers appearing in question and expression. The sorted numbers in question are: 3, 6, 9, 11. The sorted numbers in expression are: 3, 6, 9, 11. The sorting results are same.
Finally, the judgment result is.
"result": "True"
[/examples]

Now, Please imitate the above example to determine the correctness of the following questions and expressions：
"question": "{question}", "expression": "{expression}"
Output a json following the format:
```json
[
    {{
        "result": "True"
    }}
]
```
"""
        prompt = template.format(question=question, expression=expression)
        return prompt

    def numbers(numbers: list):
        string = ""
        for i in range(len(numbers)):
            string += str(numbers[i])
            if i < len(numbers) - 2:
                string += ", "
            elif i == len(numbers) - 2:
                string += " and "
        return string

    def reflexion(numbers, x, y, numbers_used_to_get_x, numbers_used_to_get_y):
        template = """[main task description]
Our main task is to obtain the target number {target} by performing arithmetic operations on {numbers}, but this task is too difficult, so we need to break it down into two smaller tasks.
[/main task description]

Here is the instruction about how to decompose the main task:
[decompose instruction]
Although we do not know how to obtain the target number {target} from {numbers}, based on mathematical attempts, we know that this expression must be calculated step by step. Each calculation step will consume an operator and a number to produce another number, which will then serve as an operand for the next calculation step. The final result must be the target number.

Therefore, we should consider the situation of the last step first instead of trying to construct the complete expression in one go.

Firstly, we need to find two intermediate numbers x and y. These two numbers are operands for the last calculation step of the final expression, provided that at least one can be obtained through x+y, x-y, x*y, x/y, y-x or y/x operations leading to the target number.

Then we have a smaller problem: how to obtain x from a subset (at least one) of {numbers} and obtain y from another subset (at least one) of {numbers}.
[/decompose instruction]

Format your response as the following json template:
```json
{{
    "nunbers": [{numbers}],
    "target": {target},
    "thought": "<fill in the reason why you choose such x and y to be the numbers left before the last step>",
    "x": <fill in the number of x>,
    "y": <fill in the number of y>,
    "numbers_used_to_get_x": [<fill in the list of numbers used to get x>],
    "numbers_used_to_get_y": [<fill in the list of numbers left after getting x>]
}}
```
Here are some necessary principles to follow:
[principle]
principle1: The two intermediate numbers x and y should be obtainable through some arithmetic operations between two of the numbers {numbers}.
principle2: The two intermediate numbers x and y should be easily combined to get {target} through arithmetic operations. (At least one of the results of following expressions x+y, x-y, x*y, x/y, y-x, y/x is {target})
principle3: numbers_used_to_get_x and numbers_used_to_get_y should be subsets of {numbers}, and the union of numbers_used_to_get_x and numbers_used_to_get_y should be equal to {numbers}.
principle4: The intermediate numbers must all be positive.
[/principle]

Here are some examples of finding intermediate numbers x and y to get a valid task decomposition solution:
[examples]
numbers: 2, 4, 5 and 19, target: 24
response:
```json
{{
    "thought": "...",
    "x": 4,
    "y": 28,
    "numbers_used_to_get_x": [4],
    "numbers_used_to_get_y": [19, 5, 2]
}}
```
numbers: 2, 5, 8 and 10, target: 24
response:
```json
{{
    "thought": "...",
    "x": 3,
    "y": 8,
    "numbers_used_to_get_x": [8, 5],
    "numbers_used_to_get_y": [10, 2]
}}
```
numbers: 3, 7, 13 and 13, target: 24
response:
```json
{{
    "thought": "...",
    "x": 8,
    "y": 3,
    "numbers_used_to_get_x": [7, 13, 13],
    "numbers_used_to_get_y": [7]
}}
```
[/examples]

Here are some negative decomposition for your task (numbers: {numbers}, target: {target}):
[negative decomposition]
{reflection}
[/negative decomposition]
Please avoid these negative decomposition when you are trying to find the suitable x and y for your task (numbers: {numbers}, target: {target}).
"""
        reflection = """```json
    {{
        "thought": "...",
        "x": {x},
        "y": {y},
        "numbers_used_to_get_x": {numbers_used_to_get_x},
        "numbers_used_to_get_y": {numbers_used_to_get_y}
    }}
    ```
    """.format(
            x=x,
            y=y,
            numbers_used_to_get_x=numbers_used_to_get_x,
            numbers_used_to_get_y=numbers_used_to_get_y,
        )
        prompt = template.format(
            numbers=Game24prompt.numbers(numbers), target=x + y, reflection=reflection
        )
        return prompt


# hotpotQA
class HotpotQAprompt:
    def context(self, obj: dict):
        contexts = []
        titles = obj["title"]
        sentences = obj["sentences"]
        for i in range(len(titles)):
            contexts.append({"title": titles[i], "content": " ".join(sentences[i])})
        return contexts

    # decompose + execute
    def decompose(self, question: str):
        template = """
You are an intelligent assistant. Your task is to decompose a complex, multi-hop question into simpler, single-hop questions. Each simpler question should contain only one unknown entity (i.e., the answer to the question).

Here is the complex question:
- Question: {question}

Follow these instructions to decompose the question:
1. Identify the entities and relationships involved in the question.
2. Break down the question into a series of simpler questions, each addressing only one unknown entity.
    - If a problem contains only one unknown entity, there may be two situations. 
    One is that the problem has only one condition in the problem description, indicating that the problem is already the simplest problem. The sub-problem is the problem itself (e.g.  example 3).
    the other is that the problem contains multiple conditions in the problem description, but there is no dependency between these conditions, and the problem can be decomposed into multiple sub-problems according to the independence of the conditions (e.g. examples 1, 7, 11 and 12).
    - If the problem is to compare two entities, it can be decomposed into two questions, asking about a certain attribute of each entity separately, and then answering the original question based on the comparison of these attributes (e.g. examples 5, 6, 8 and 13).
    - If there are multiple unknown entities in the problem, the problem can be decomposed into multiple sub-problems according to the relationship between these entities.
    Each sub-problem only involves one unknown entity, and there are dependencies between these sub-problems, which need to be solved in the order of dependencies (e.g. examples 2, 4, 9 and 10).

Format your response as follows:
```json
{{
    "original_question": "{question}",
    "thought_process": "<Fill in your thought process here, how do you decompose the complex question into simpler ones?>",
    "decomposed_questions": [
        {{
            "question": "<First decomposed question>",
            "predecessor": [<Index of the predecessor question in the decomposed_questions list>]
        }},
        {{
            "question": "<Second decomposed question>",
            "predecessor": [<Index of the predecessor question in the decomposed_questions list>]
        }},
        ...
    ]
}}
```

Here are some examples of decomposing complex questions into simpler ones:

Example 1:
- Original Question: Who was known by his stage name Aladin and helped organizations improve their performance as a consultant?
- Decomposed Questions:
```json
{{
    "original_question": "Who was known by his stage name Aladin and helped organizations improve their performance as a consultant?",
    "thought_process": "",
    "decomposed_questions": [
        {{
            "question": "Who are known by the stage name Aladin?",
            "predecessor": []
        }},
        {{
            "question": "Who helped organizations improve their performance as a consultant?",
            "predecessor": []
        }},
        {{
            "question": "Who is the intersection of <answer0> and <answer1>?",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 2:
- Original Question: What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?
- Decomposed Questions:
```json
{{
    "original_question": "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?",
    "thought_process": "First, identify the actress who portrayed Corliss Archer in the film Kiss and Tell. Then, determine what government position she held.",
    "decomposed_questions": [
        {{
            "question": "Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?",
            "predecessor": []
        }},
        {{
            "question": "What government position was held by <answer0>?",
            "predecessor": [0]
        }}
    ]
}}
```

Example 3:
- Original Question: D1NZ is a series based on what oversteering technique?
- Decomposed Questions:
```json
{{
    "original_question": "The question 'D1NZ is a series based on what oversteering technique?' 
    "thought_process": "The question asks for a specific technique related to the D1NZ series, which is a straightforward query about a particular aspect of the series. It is a direct question that does not involve multiple steps, complex reasoning, or dependencies that would necessitate breaking it down into smaller parts. Therefore, it cannot be decomposed into sub-questions.",
    "decomposed_questions": [
        {{
            "question": "D1NZ is a series based on what oversteering technique?",
            "predecessor": []
        }}
    ]
}}
```

Example 4:
- Original Question: Suicide's 1977 released album features a song based on what brand's comic character?
- Decomposed Questions:
```json
{{
    "original_question": "Suicide's 1977 released album features a song based on what brand's comic character?",
    "thought_process": "First, identify the song featured in Suicide's 1977 released album. Then, determine which brand's comic character the song is based on.",
    "decomposed_questions": [
        {{
            "question": "Suicide's 1977 released album features what song?",
            "predecessor": []
        }},
        {{
            "question": "<answer0> is based on what brand's comic character?",
            "predecessor": [0]
        }}
    ]
}}
```

Example 5:
- Original Question: Which filmmaker was known for animation, Lev Yilmaz or Pamela B. Green?
- Decomposed Questions:
```json
{{
    "original_question": "Which filmmaker was known for animation, Lev Yilmaz or Pamela B. Green?",
    "thought_process": "First, determine if Lev Yilmaz is known for animation. Then, determine if Pamela B. Green is known for animation. Finally, compare the results to identify which filmmaker is known for animation.",
    "decomposed_questions": [
        {{
            "question": "Is Lev Yilmaz known for animation?",
            "predecessor": []
        }},
        {{
            "question": "Is Pamela B. Green known for animation?",
            "predecessor": []
        }},
        {{
            "question": "If <answer0> is yes, answer 'Lev Yilmaz'; If <answer1> is yes, answer 'Pamela B. Green'.",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 6:
- Original Question: Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?
- Decomposed Questions:
```json
{{
    "original_question": "Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?",
    "thought_process": "First, determine the neighborhood where the Laleli Mosque is located. Then, determine the neighborhood where the Esma Sultan Mansion is located. Finally, compare the two neighborhoods to see if they are the same.",
    "decomposed_questions": [
        {{
            "question": "What neighborhood is the Laleli Mosque located in?",
            "predecessor": []
        }},
        {{
            "question": "What neighborhood is the Esma Sultan Mansion located in?",
            "predecessor": []
        }},
        {{
            "question": "Are the <answer0> and <answer1> the same? If so, answer yes; otherwise, answer no.",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 7:
- Original Question: Which American cable news and talk radio host was the former GOP representative
- Decomposed Questions:
```json
{{
    "original_question": "Which American cable news and talk radio host was the former GOP representative?",
    "thought_process": "To determine the American cable news and talk radio host who was a former GOP representative, we need to decompose the question. First, we identify all American cable news and talk radio hosts. Then, we identify all former GOP representatives. Finally, we find the intersection of these two sets to get the answer.",
    "decomposed_questions": [
        {{
            "question": "Who are the American cable news and talk radio hosts?",
            "predecessor": []
        }},
        {{
            "question": "Who are the former GOP representatives?",
            "predecessor": []
        }},
        {{
            "question": "Who is the intersection of <answer0> and <answer1>?",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 8:
- Original Question: Are Ferocactus and Silene both types of plant?
- Decomposed Questions:
```json
{{
    "original_question": "Are Ferocactus and Silene both types of plant?",
    "thought_process": "First, determine if Ferocactus is a type of plant. Then, determine if Silene is a type of plant. Finally, compare the results to see if both are types of plants.",
    "decomposed_questions": [
        {{
            "question": "Is Ferocactus a type of plant?",
            "predecessor": []
        }},
        {{
            "question": "Is Silene a type of plant?",
            "predecessor": []
        }},
        {{
            "question": "Are the <answer0> and <answer1> both yes? If so, answer yes; otherwise, answer no.",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 9:
- Original Question: A medieval fortress in Dirleton, East Lothian, Scotland borders on the south side of what coastal area?
- Decomposed Questions:
```json
{{
    "original_question": "A medieval fortress in Dirleton, East Lothian, Scotland borders on the south side of what coastal area?",
    "thought_process": "First, identify the medieval fortress in Dirleton, East Lothian, Scotland. Then, determine the coastal area that borders the south side of this fortress.",
    "decomposed_questions": [
        {{
            "question": "What is the name of the medieval fortress in Dirleton, East Lothian, Scotland?",
            "predecessor": []
        }},
        {{
            "question": "<answer0> borders on the south side of what coastal area?",
            "predecessor": [0]
        }}
    ]
}}
```

Example 10:
- Original Question: Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with?
- Decomposed Questions:
```json
{{
    "original_question": "Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with?",
    "thought_process": "First, identify the program that the Apple Remote was originally designed to interact with. Then, determine what other device can control this program.",
    "decomposed_questions": [
        {{
            "question": "What program was the Apple Remote originally designed to interact with?",
            "predecessor": []
        }},
        {{
            "question": "Aside from the Apple Remote, what other device can control the program <answer0>?",
            "predecessor": [0]
        }}
    ]
}}
```

Example 11:
- Original Question: What is the name of the film starring Rose McGowan and features the character Earl McGraw's daughter?
- Decomposed Questions:
```json
{{
    "original_question": "What is the name of the film starring Rose McGowan and features the character Earl McGraw's daughter?",
    "thought_process": "To answer this question, we need to identify films that star Rose McGowan and then narrow those down to ones that also feature the character Earl McGraw's daughter. We can break this down into a few steps: First, we find a list of films starring Rose McGowan. Second, we find a list of films that feature the character Earl McGraw's daughter. Finally, we determine which film appears in both lists.",
    "decomposed_questions": [
        {{
            "question": "What are the names of the films starring Rose McGowan?",
            "predecessor": []
        }},
        {{
            "question": "What are the names of the films that feature the character Earl McGraw's daughter?",
            "predecessor": []
        }},
        {{
            "question": "What is the name of the film that is the intersection of <answer0> and <answer1>?",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 12:
- Original Question: David Huntsinger has worked with this gospel singer born in the month of July?
- Decomposed Questions:
```json
{{
    "original_question": "David Huntsinger has worked with this gospel singer born in the month of July?",
    "thought_process": "To find the gospel singer that David Huntsinger has worked with who is born in the month of July, we need to break down the question into parts. First, we identify all gospel singers that David Huntsinger has worked with. Then, we identify gospel singers born in the month of July. Finally, we find the intersection of these two sets to get the answer.",
    "decomposed_questions": [
        {{
            "question": "Who are the gospel singers that David Huntsinger has worked with?",
            "predecessor": []
        }},
        {{
            "question": "Who are the gospel singers born in the month of July?",
            "predecessor": []
        }},
        {{
            "question": "Who is the intersection of <answer0> and <answer1>?",
            "predecessor": [0, 1]
        }}
    ]
}}
```

Example 13:
- Original Question: Who was born first, Erika Jayne or Marco Da Silva?
- Decomposed Questions:
```json
{{
    "original_question": "Who was born first, Erika Jayne or Marco Da Silva?"
    "thought_process": ""
    "decomposed_questions": [
        {{
            "question": "When was Erika Jayne born?"
            "predecessor": []
        }},
        {{
            "question": "When was Marco Da Silva born?"
            "predecessor": []
        }},
        {{
            "question": "If <answer0> is earlier than <answer1>, answer 'Erika Jayne'; otherwise, answer 'Marco Da Silva'."
            "predecessor": [0, 1]
        }}
    ]
}}
```
"""
        prompt = template.format(question=question)
        return prompt

    def execute(self, question: str, context: list):
        # 4. If the information in context alone cannot provide an answer, directly use the "unknown" marker as the answer which means context doesn't have enough information to answer the question.
        template = """
You are an intelligent assistant. Your task is to answer the given question based on the provided context. Follow the thought process to arrive at a concise and accurate answer.

Here is the question and context:
- Question: {question}
- Context: {context}

Follow these instructions to answer the question:
1. Do not use your own knowledge to answer the question. Only use the information provided in the context.
2. If the question is a simple yes-or-no question, answer directly with "yes" or "no" based on the context.
3. If the question is more complex, find the exact text in the context that answers the question and use it without any changes. 
   (For example, if the original text is "1969 until 1974", your answer should be "1969 until 1974", not "1969-1974" or "1969 to 1974").
4. Be aware that the context may contain misleading information.
5. Keep your answer brief and concise. Avoid repeating words from the question.

Here is an example to illustrate how to answer concisely:
- Question: Was Delicatessen, the 1991 French movie, made in the style of whose work?
Good Answer: Terry Gilliam
Bad Answer: Terry Gilliam's work, in the style of Terry Gilliam, Terry Gilliam's style
- Question: How many restaurants comprise the quick service restaurant chain that Ron Joyce helped found?
Good Answer: 3,400
Bad Answer: 3,400 restaurants; 3,400 locations; 3,400 quick service restaurants

Format your response as follows:
```json
{{
    "question": "{question}",
    "thought_process": "<Explain how you analyzed the context and found the answer. Mention the specific parts of the context that supported your answer.>",
    "answer": "<Provide the concise and accurate answer. The fewer words in the answer, the better.>"
}}
```
"""
        prompt = template.format(question=question, context=context)
        return prompt

    # cluster
    def duplicate(self, target: str, questions: list, n: int):
        template = """We now have a target question and a set of {n} candidate questions, and we need to find the question that is semantically duplicate with the target question.
target: {target}
questions: {questions}

Follow the instructions when finding the question that is semantically duplicate with "{target}":
1. The standard for determining if two questions are semantically duplicates is that if the two questions are answered, the answers will be the same.
It means that the difference lies only in the different forms of expression or the varying degrees of richness in preconditions.
2. Only up to one question is semantically duplicate with the target question.
3. If none of the questions meet the standard for duplication, return None.


Format your response as the following json template:
```json
{{
    "target": "{target}",
    "thought_process": "<Fill in your thought process here, how do you determine which question is semantically duplicate with the target question?>",
    "duplicate_question": "<Fill in the question that is duplicate with the target question>"
}}
```

Here are some examples of finding the question that is semantically duplicate with the target question:
Example 1:
- Target Question: What is the name of the group of black Indians associated with the Seminole people?
- Candidate Questions: ["Who are the group of black Indians associated with the Seminole people?", "Where did the group of black Indians associated with the Seminole people settle?", "Where did the descendants of <answer0> settle?"]
```json
{{
    "target": "What is the name of the group of black Indians associated with the Seminole people?",
    "thought_process": "The question 'Who are the group of black Indians associated with the Seminole people?' is semantically duplicate with the target question because the answer to both questions is the same.",
    "duplicate_question": "Who are the group of black Indians associated with the Seminole people?"
}}
```

Example 2:
- Target Question: What river is Frenchmans Creek a tributary of?
- Candidate Questions: ["What is the name of the river that Frenchmans Creek is a tributary of?", What river is Frenchmans Creek's tributary?", "How long is <answer>?"
```json
{{
    "target": "What river is Frenchmans Creek a tributary of?",
    "questions": ["What is the name of the river that Frenchmans Creek is a tributary of?", "What river is Frenchmans Creek's tributary?", "How long is <answer>?"]
    "thought_process": "The question 'What is the name of the river that Frenchmans Creek is a tributary of?' is semantically duplicate with the target question because the answer to both questions is the same.",
    "duplicate_question": "What is the name of the river that Frenchmans Creek is a tributary of?"
}}
```

Example 3:
- Target Question: What Cayman Islands registered Mandarin and Cantonese-language television broadcaster launched Phoenix Hong Kong Channel on 28 March 2011?
- Candidate Questions: ["What is the name of the Mandarin and Cantonese-language television broadcaster registered in the Cayman Islands?", "Did <answer0> launch Phoenix Hong Kong Channel on 28 March 2011?"]
```json
{{
    "target": "What Cayman Islands registered Mandarin and Cantonese-language television broadcaster launched Phoenix Hong Kong Channel on 28 March 2011?",
    "questions": ["What is the name of the Mandarin and Cantonese-language television broadcaster registered in the Cayman Islands?", "Did <answer0> launch Phoenix Hong Kong Channel on 28 March 2011?"],
    "thought_process": "The question 'What is the name of the Mandarin and Cantonese-language television broadcaster registered in the Cayman Islands?' is semantically duplicate with the target question because the answer to both questions is the same.",
    "duplicate_question": "What is the name of the Mandarin and Cantonese-language television broadcaster registered in the Cayman Islands?"
}}
```

Example 4:
- Target Question: What is the name of the film starring Rose McGowan and features the character Earl McGraw's daughter?
- Candidate Questions: ["What are the names of the films starring Rose McGowan?", "What are the names of the films that feature the character Earl McGraw's daughter?", "What is the name of the film that is the intersection of <answer> and <answer>?"]
```json
{{
    "target": "What is the name of the film starring Rose McGowan and features the character Earl McGraw's daughter?",
    "questions": ["What are the names of the films starring Rose McGowan?", "What are the names of the films that feature the character Earl McGraw's daughter?", "What is the name of the film that is the intersection of <answer> and <answer>?"]
    "thought_process": "The question 'What are the names of the films starring Rose McGowan?' is semantically duplicate with the target question because the answer to both questions is the same.",
    "duplicate_question": "What are the names of the films starring Rose McGowan?"
}}
```
"""
        prompt = template.format(target=target, questions=questions, n=n)
        return prompt

    # restructure
    def predecessor(
        self,
        original_question: str,
        question: str,
        candidates: list,
    ):
        template = """
You are an intelligent assistant. Your task is to identify the most suitable question from the given candidates that can serve as a legitimate predecessor for the current question.

Here is the current question and the list of candidate questions:
- Original Question: {original_question}
- Current Question: {question}
- Candidate Questions: {candidates}

Follow these instructions to identify the legitimate predecessor question:
1. Analyze the current question to understand the dependencies indicated by placeholders like <answeri>.
2. Review each candidate question to determine if its answer can logically serve as the required dependency for the current question.
3. Select the candidate question(s) whose answer(s) can directly fill the placeholders in the current question.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "current_question": "{question}",
    "candidates": {candidates},
    "thought_process": "<Fill in your thought process here, how do you analyze the dependencies and select the suitable candidate question(s)?>",
    "selected_candidate": "<Fill in the selected candidate question>"
}}
```
Here are some examples of identifying the legitimate predecessor question for the current question:
Example 1:
- Original Question: "Who directed the 1941 film based on the novel of the same name by Zane Grey starring an actor who was also an artist and stuntman?"
- Current Question: "Which director directed a film starring <answer1>?"
- Context: Omitting the context for brevity
```json
{{
    "original_question": "Who directed the 1941 film based on the novel of the same name by Zane Grey starring an actor who was also an artist and stuntman?",
    "current_question": "Which director directed a film starring <answer1>?",
    "candidates": ["Who is the actor that starred in the 1941 film and was also an artist and stuntman?", "Who directed the 1941 film?", "What is the name of the novel by Zane Grey that the 1941 film is based on?"]
    "thought_process": "The current question requires the name of the actor who starred in the 1941 film. The candidate question 'Who is the actor that starred in the 1941 film and was also an artist and stuntman?' directly addresses this requirement by providing the necessary information.",
    "selected_candidate": "Who is the actor that starred in the 1941 film and was also an artist and stuntman?"
}}
```
"""
        prompt = template.format(
            original_question=original_question,
            question=question,
            candidates=candidates,
        )
        return prompt

    def convergence(self, original_question: str, candidates: list):
        template = """
You are an intelligent assistant. Your task is to identify the most suitable sub-question from the given candidates whose answer can serve as the answer to the original question.

Here is the original question and the list of candidate sub-questions:
- Original Question: {original_question}
- Candidate Sub-Questions: {candidates}

Follow these instructions to identify the suitable sub-question:
1. Analyze the original question to understand the main entity or information it seeks.
2. Review each candidate sub-question to determine if its answer can semantically serve as the answer to the original question.
3. Select the sub-question whose answer directly addresses the original question. 
If there are multiple sub-questions whose answer can semantically serve as the answer to the original question, 
choose the one that have dependencies (such as tags like <answeri>) and describe the most complete subproblem.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "candidates": {candidates},
    "thought_process": "<Fill in your thought process here, how do you analyze the original question and select the suitable sub-question?>",
    "selected_sub_question": "<Fill in the selected sub-question>"
}}
```
Here are some examples of selecting a sub-question to answer the original question:
Example 1:
- Original Question: which king of Northumbria did The \"Historia\" gives the abbot central place in his election as king
- Candidate Sub-Questions: ["Who is the king of Northumbria mentioned in The 'Historia'?", "Which abbot was given a central place in the election as king by <answer0>?", "In the election of <answer0> as king, which abbot was given a central place?"]
```json
{{
    "original_question": "which king of Northumbria did The \"Historia\" gives the abbot central place in his election as king",
    "candidates": ["Who is the king of Northumbria mentioned in The 'Historia'?", "Which abbot was given a central place in the election as king by <answer0>?", "In the election of <answer0> as king, which abbot was given a central place?"],
    "thought_process": "The original question is asking about the king of Northumbria in a specific historical context provided by 'The Historia'. The key information sought is the identity of the king. The first candidate sub-question directly asks for the king of Northumbria mentioned in 'The Historia', which directly addresses the original question. The other sub-questions involve additional entities (abbot) and dependencies (<answer0>) which are not the primary focus of the original question.",
    "selected_sub_question": "Who is the king of Northumbria mentioned in The 'Historia'?"
}}
```

Example 2:
- Original Question: How long is the river for which Frenchmans Creek is a tributary?
- Candidate Sub-Questions: ["What is the name of the river that Frenchmans Creek is a tributary of?", "How long is <answer0>?", "What is the name of the main river into which Frenchmans Creek flows?"]
```json
{{
    "original_question": "How long is the river for which Frenchmans Creek is a tributary?",
    "candidates": ["What is the name of the river that Frenchmans Creek is a tributary of?", "How long is <answer0>?", "What is the name of the main river into which Frenchmans Creek flows?"],
    "thought_process": "The original question is asking for the length of a specific river, specifically the one for which Frenchmans Creek is a tributary. The key information sought is the length of that river. The second candidate sub-question ('How long is <answer0>?') directly asks for the length of the river, which matches the original question's requirement. The other sub-questions ask for the name of the river, which is not the primary information being sought.",
    "selected_sub_question": "How long is <answer0>?"
}}
```

Example 3:
- Original Question: Emmett Brown rides in a sports car that features what type of doors?
- Candidate Sub-Questions: ["Emmett Brown rides in a sports car that features what type of doors?", "What sports car does Emmett Brown ride in?", "What type of doors does <answer0> feature?", "What type of doors does the <answer0> sports car feature?", "What type of doors does <answer0> have?"]
```json
{{
    "original_question": "Emmett Brown rides in a sports car that features what type of doors?",
    "candidates": ["Emmett Brown rides in a sports car that features what type of doors?", "What sports car does Emmett Brown ride in?", "What type of doors does <answer0> feature?", "What type of doors does the <answer0> sports car feature?", "What type of doors does <answer0> have?"],
    "thought_process": "The original question is asking for the type of doors on the sports car that Emmett Brown rides in. The key information sought is the type of doors. The first candidate sub-question is identical to the original question and thus directly addresses it. The other sub-questions involve identifying the sports car first and then asking about the type of doors, which adds unnecessary complexity. Among the remaining options, 'What type of doors does the <answer0> sports car feature?' is the most specific and complete sub-question that can serve as the answer to the original question.",
    "selected_sub_question": "What type of doors does the <answer0> sports car feature?"
}}
```

Example 4:
- Original Question: "What is the name of the Australian specialist electronic music magazine that features avant-rock, experimental sound art, and experimental hip hop?",
- Candidate Sub-Questions: ["What is the name of the Australian specialist electronic music magazine?", "Does the electronic music magazine feature avant-rock, experimental sound art, and experimental hip hop?", "What type of music does the Australian specialist electronic music magazine feature?", "What is the name of the magazine that features avant-rock, experimental sound art, and experimental hip hop?"]
```json
{{
    "original_question": "What is the name of the Australian specialist electronic music magazine that features avant-rock, experimental sound art, and experimental hip hop?",
    "candidates": ["Does the electronic music magazine feature avant-rock, experimental sound art, and experimental hip hop?", "What type of music does the Australian specialist electronic music magazine feature?", "What is the name of the magazine that features avant-rock, experimental sound art, and experimental hip hop?", "What is the name of the Australian specialist electronic music magazine?"],
    "thought_process": "The original question is asking for the name of an Australian specialist electronic music magazine that features specific music genres. The key information sought is the name of the magazine. The first candidate sub-question directly asks for the name of the magazine, which matches the original question's requirement. The other sub-questions involve identifying the music genres first and then asking about the magazine name, which adds unnecessary complexity. Among the remaining options, 'What is the name of the magazine that features avant-rock, experimental sound art, and experimental hip hop?' is the most specific and complete sub-question that can serve as the answer to the original question.",
    "selected_sub_question": "What is the name of the Australian specialist electronic music magazine?"
}}
```
"""
        prompt = template.format(
            original_question=original_question, candidates=candidates
        )
        return prompt

    def summarize(self, original_question: str, candidates: list, context: str):
        template = """
You are an intelligent assistant. Your task is to select two sub-questions and their corresponding answers from the given candidates and use them to answer the original question.

Here is the original question and the list of candidate sub-questions:
- Original Question: {original_question}
- Candidate Sub-Questions: {candidates}
- Context: {context}

Follow these instructions to select the sub-questions and their answers:
1. The two sub-questions should cover the key information of the original question, so that the original question can be answered through the answers to these two sub-questions.
2. The candidate questions will come with a list of answers, which may have a high degree of consistency or some differences. A final answer needs to be voted on or summarized based on these answers.
3. Based on the selected answers to the two sub-questions, answer the original question, but also consider whether the answers to these two sub-questions can fully address the original question and whether they are consistent with context. In such cases, you should prioritize referencing information in the context.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "candidates": {candidates},
    "thought_process": "<Fill in your thought process here, how do you analyze the original question and select the suitable sub-questions and their answers?>",
    "selected_sub_questions": [
        {{
            "question": "<First selected sub-question>",
            "answer": "<Semantical majority answer to the first sub-question>"
        }},
        {{
            "question": "<Second selected sub-question>",
            "answer": "<Semantical majority answer to the second sub-question>"
        }}
    ],
    "final_answer": "<Provide the final answer to the original question based on the selected sub-questions and their answers>"
}}
Here are some examples of selecting sub-questions and their answers to answer the original question:
Example 1:

Original Question: Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?
Context: Omitting the context for brevity
{{
    "original_question": "Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?",
    "candidates": [
        {{
            "question": "Where is the Laleli Mosque located?",
            "answer": ["Istanbul", "Istanbul", "Istanbul", "Neighborhood"]
        }},
        {{
            "question": "What neighborhood is the Laleli Mosque located in?",
            "answer": ["Laleli", "Laleli"]
        }},
        {{
            "question": "Where is the Esma Sultan Mansion located?",
            "answer": ["Istanbul"]
        }},
        {{
            "question": "What is the name of the neighborhood where both the Laleli Mosque and Esma Sultan Mansion are located?",
            "answer": ["Laleli"]
        }},
        {{
            "question": "What is the name of the neighborhood where the Esma Sultan Mansion are located?",
            "answer": ["Ortaköy", "Ortaköy", "Istanbul"]
        }}
    ],
    "thought_process": "The original question is asking whether the Laleli Mosque and Esma Sultan Mansion are located in the same neighborhood. To answer this, we need to determine the neighborhoods of both landmarks. The sub-question 'What neighborhood is the Laleli Mosque located in?' directly addresses the location of the Laleli Mosque, and the consistent answer is 'Laleli'. The sub-question 'What is the name of the neighborhood where the Esma Sultan Mansion are located?' directly addresses the location of the Esma Sultan Mansion, with the majority answer being 'Ortaköy'. Since the neighborhoods are different, the final answer to the original question is 'No'.",
    "selected_sub_questions": [
        {{
            "question": "What neighborhood is the Laleli Mosque located in?",
            "answer": "Laleli"
        }},
        {{
            "question": "What is the name of the neighborhood where the Esma Sultan Mansion are located?",
            "answer": "Ortaköy"
        }}
    ],
    "final_answer": "No"
}}
Example 2:

Original Question: What is the name of the film starring Rose McGowan and features the character Earl McGraw's daughter?
Context: Omitting the context for brevity
{{
    "original_question": "What is the name of the film starring Rose McGowan and features the character Earl McGraw's daughter?",
    "candidates": [
        {{
            "question": "What are the names of the films starring Rose McGowan?",
            "answer": ["Grindhouse, Death Proof and Mind hacker", "Grindhouse", "Grindhouse", "Death Proof and Doctor Jack"]
        }},
        {{
            "question": "What are the names of the films that feature the character Earl McGraw's daughter?",
            "answer": ["Death Proof"]
        }},
        {{
            "question": "What is the name of the film that is the intersection of <answer0> and <answer1>?",
            "answer": ["Death Proof"]
        }}
    ],
    "thought_process": "The original question is asking for the name of a film that stars Rose McGowan and features the character Earl McGraw's daughter. To answer this, we need to identify the films starring Rose McGowan and the films featuring Earl McGraw's daughter. The sub-question 'What are the names of the films starring Rose McGowan?' provides multiple answers, including 'Grindhouse', 'Death Proof', 'Mind Hacker', and 'Doctor Jack'. This indicates that Rose McGowan has starred in several films, but 'Grindhouse' and 'Death Proof' are mentioned multiple times. The sub-question 'What are the names of the films that feature the character Earl McGraw's daughter?' consistently answers 'Death Proof'. By cross-referencing these answers, we find that 'Death Proof' is the film that fits both criteria.",
    "selected_sub_questions": [
        {{
            "question": "What are the names of the films starring Rose McGowan?",
            "answer": "Grindhouse, Death Proof, Mind hacker and Doctor Jack"
        }},
        {{
            "question": "What are the names of the films that feature the character Earl McGraw's daughter?",
            "answer": "Death Proof"
        }}
    ],
    "final_answer": "Death Proof"
}}
"""
        prompt = template.format(
            original_question=original_question, candidates=candidates, context=context
        )
        return prompt

    def majority(
        self, objects: list, original_question: str = None, context: list = None
    ):
        ternimal_template = """
You are an intelligent assistant. Your task is to find the semantical majority element in the given list of answers to the original question, considering the provided context. 
A semantical majority element is the one that represents the most common or frequent concept among the answers, even if they are expressed in different forms.

Here is the original question, context, and list of answers:
- Original Question: {original_question}
- Context: {context}
- Answers: {objects}

Follow these instructions to find the majority element:
1. Determine the elements that appear the most times in the meaning, and the elements may have slight differences in form.
When determining the majority element, it needs to be summarized.
2. If the illegitimate elements constitute the majority, return false.
3. The context provides additional information that can help identify the semantical majority element, consider it in your analysis.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "thought_process": "<Explain your thought process here, how do you determine the semantical majority element and ensure it aligns with the context?>",
    "majority_element": "<Fill in the semantical majority element or false if illegitimate answers are the majority>"
}}
```
"""
        normal_template = """
You are an intelligent assistant. Your task is to find the semantical majority element in the given list of objects. 
A semantical majority element is the one that represents the most common or frequent concept among the objects, even if they are expressed in different forms.

Here is the list of objects:
- Objects: {objects}

Follow these instructions to find the majority element:
1. Determine the elements that appear the most times in the meaning, and the elements may have slight differences in form.
When determining the majority element, it needs to be summarized.
2. If the illegitimate elements constitute the majority, return false.

Format your response as follows:
```json
{{
    "thought_process": "<Explain your thought process here, how do you determine the semantical majority element?>",
    "majority_element": "<Fill in the semantical majority element or false if illegitimate elements are the majority>"
}}
```
"""
        if original_question and context:
            prompt = ternimal_template.format(
                original_question=original_question, context=context, objects=objects
            )
        else:
            prompt = normal_template.format(objects=objects)
        return prompt

    # OT
    def stage(self, original_question: str, reasoning_chain: list):
        # reasoning_chain:
        # list of questions
        # [{question: str, answer: str},...]

        # return: question or answer

        template = """
You are an intelligent assistant. Your task is to evaluate whether the current question chain is sufficient to answer the original question or if additional sub-questions are needed.

Here is the original question and the current question chain:
- Original Question: {original_question}
- Question Chain: {reasoning_chain}

Follow these instructions to evaluate the situation:
1. Analyze the original question and the question chain to determine if the chain logically leads to an answer for the original question.
2. If the question chain provides a clear path to an answer or if the last question in the chain can be answered directly from the given context or known information, then no new sub-questions are needed.
3. If there are gaps in the chain or if the last question requires further clarification or additional information, then new sub-questions are needed.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "reasoning_chain": {reasoning_chain},
    "thought_process": "<Fill in your thought process here, how do you determine if additional sub-questions are needed?>",
    "additional_sub_questions_needed": <true_or_false>
    "additional_sub_questions": [<Fill in the list of additional sub-questions needed>]
}}
```
"""
        prompt = template.format(
            original_question=original_question, reasoning_chain=reasoning_chain
        )
        return prompt

    def stage_got(self, original_question: str, reasoning_chain: list):
        # reasoning_chain : [[some sub_questions for the 1st stage], [qs for the 2nd stage], [3rd stage], ... ,[last stage]]
        template = """
You are an intelligent assistant. Your task is to evaluate whether the current question chain is sufficient to answer the original question or if additional sub-questions are needed. 
The question chain is a list of lists: [[subquestions for the 1st stage], [subquestions for the 2nd stage], [subquestions for the 3rd stage], ... ,[subquestions for the last stage]]

Here is the original question and the current question chain:
- Original Question: {original_question}
- Question Chain: {reasoning_chain}

Follow these instructions to evaluate the situation:
1. Analyze the original question and the question chain to determine if the chain logically leads to an answer for the original question.
2. If the question chain provides a clear path to an answer or if the last question in the chain can be answered directly from the given context or known information, then no new sub-questions are needed.
3. If there are gaps in the chain or if the last question requires further clarification or additional information, then new sub-questions are needed.
4. If needed, you should give less than 4 sub-questions.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "reasoning_chain": {reasoning_chain},
    "thought_process": "<Fill in your thought process here, how do you determine if additional sub-questions are needed?>",
    "additional_sub_questions_needed": <true_or_false>
    "additional_sub_questions": [<Fill in the list of additional sub-questions needed>]
}}
```
"""
        prompt = template.format(
            original_question=original_question, reasoning_chain=reasoning_chain
        )
        return prompt
    

    def evaluate_got(self, original_question: str, questions: list):
        # return questions:list
        template = """
You are an intelligent assistant. Your task is to evaluate the given list of sub-questions and remove the temporarily unnecessary sub-question(s) to resolve the original_question.

Here is the original complex question and the list of sub-questions:
- Original Question: {original_question}
- Sub-Questions: {questions}

Follow these instructions to remove the unnecessary sub-questions:
1. Analyze each sub-question to determine its relevance and importance in resolving the original complex question.
2. Consider the logical sequence and dependencies of the sub-questions.
3. Select the most temporarily unnecessary sub-question(s) and remove it/them from the list of sub-questions.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "sub_questions": {questions},
    "thought_process": "<Fill in your thought process here, how do you analyze and rank the sub-questions in terms of their relevance and importance?>",
    "selected_sub_questions": [<List of the sub-questions after removing the unnecessary one(s)>]
}}
```
Here are some examples of evaluating and selecting the best sub-questions:

Example 1:
- Original Question: "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?"
- Sub-Questions: ["Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?", "What government position was held by <answer0>?"]
```json
{{
    "original_question": "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?",
    "sub_questions": ["Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?", "What government position was held by <answer0>?"],
    "thought_process": "The question 'Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?' should be prioritized first as it identifies the main entity needed to answer the original question. The second question depends on the answer to the first. So the second question is temporarily unnecessary.",
    "selected_sub_questions": ["Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?"]
}}
```

Example 2:
- Original Question: "Who was born first, Erika Jayne or Marco Da Silva?"
- Sub-Questions: ["When was Erika Jayne born?", "When was Marco Da Silva born?", "If <answer0> is earlier than <answer1>, answer 'Erika Jayne'; otherwise, answer 'Marco Da Silva'."]
```json
{{
    "original_question": "Who was born first, Erika Jayne or Marco Da Silva?",
    "sub_questions": ["When was Erika Jayne born?", "When was Marco Da Silva born?", "If <answer0> is earlier than <answer1>, answer 'Erika Jayne'; otherwise, answer 'Marco Da Silva'."],
    "thought_process": "The questions 'When was Erika Jayne born?' and 'When was Marco Da Silva born?' should be prioritized first as they provide the necessary information to compare their birth dates. The third question depends on the answers to the first two. So the third question is temporarily unnecessary.",
    "selected_sub_questions": ["When was Erika Jayne born?", "When was Marco Da Silva born?"]
}}
```

Example 3:
- Original Question: "Edmund Robert Harris is the principal benefactor of a museum located where ?"
- Sub-Questions: ["Which museum is Edmund Robert Harris the principal benefactor of?", "What is the museum associated with Edmund Robert Harris?"]
```json
{{
    "original_question": "Edmund Robert Harris is the principal benefactor of a museum located where ?",
    "sub_questions": ["Which museum is Edmund Robert Harris the principal benefactor of?", "What is the museum associated with Edmund Robert Harris?", "Where is the museum <answer0> located?"],
    "thought_process": "There is no logical sequence between the questions 'Which museum is Edmund Robert Harris the principal benefactor of?' and 'What is the museum associated with Edmund Robert Harris?'. They are equally important for solving the original question. So we don't need to remove any one.",
    "selected_sub_questions": ["Which museum is Edmund Robert Harris the principal benefactor of?", "What is the museum associated with Edmund Robert Harris?"]
}}
```
"""
        prompt = template.format(
            original_question=original_question, questions=questions
        )
        return prompt
    

    def evaluate(self, original_question: str, questions: list, k: int = 1):
        # k=1, 选最好的问题
        # k>1, 选最好的k个问题且不要重复

        # return questions:list
        template = """
You are an intelligent assistant. Your task is to evaluate the given list of sub-questions and select the best {k} question(s) that should be prioritized to help resolve the original complex question.

Here is the original complex question and the list of sub-questions:
- Original Question: {original_question}
- Sub-Questions: {questions}
- k: {k}

Follow these instructions to evaluate and select the best sub-questions:
1. Analyze each sub-question to determine its relevance and importance in resolving the original complex question.
2. Consider the logical sequence and dependencies of the sub-questions.
3. Select the top {k} sub-question(s) that should be prioritized for answering to make the most progress towards resolving the original complex question.

Format your response as follows:
```json
{{
    "original_question": "{original_question}",
    "sub_questions": {questions},
    "thought_process": "<Fill in your thought process here, how do you analyze and rank the sub-questions in terms of their relevance and importance?>",
    "selected_sub_questions": [<List of the selected top {k} sub-questions>]
}}
```

Here are some examples of evaluating and selecting the best sub-questions:

Example 1:
- Original Question: "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?"
- k: 1
- Sub-Questions: ["Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?", "What government position was held by <answer0>?"]
```json
{{
    "original_question": "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?",
    "sub_questions": ["Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?", "What government position was held by <answer0>?"],
    "thought_process": "The question 'Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?' should be prioritized first as it identifies the main entity needed to answer the original question. The second question depends on the answer to the first.",
    "selected_sub_questions": ["Who is the woman who portrayed Corliss Archer in the film Kiss and Tell?"]
}}
```

Example 2:
- Original Question: "Who was born first, Erika Jayne or Marco Da Silva?"
- k: 2
- Sub-Questions: ["When was Erika Jayne born?", "When was Marco Da Silva born?", "If <answer0> is earlier than <answer1>, answer 'Erika Jayne'; otherwise, answer 'Marco Da Silva'."]
```json
{{
    "original_question": "Who was born first, Erika Jayne or Marco Da Silva?",
    "sub_questions": ["When was Erika Jayne born?", "When was Marco Da Silva born?", "If <answer0> is earlier than <answer1>, answer 'Erika Jayne'; otherwise, answer 'Marco Da Silva'."],
    "thought_process": "The questions 'When was Erika Jayne born?' and 'When was Marco Da Silva born?' should be prioritized first as they provide the necessary information to compare their birth dates. The third question depends on the answers to the first two.",
    "selected_sub_questions": ["When was Erika Jayne born?", "When was Marco Da Silva born?"]
}}
```
"""
        prompt = template.format(
            original_question=original_question, questions=questions, k=k
        )
        return prompt

    def legitimate(self, answer: str):
        template = """
You are an intelligent assistant. Your task is to check the legitimacy of the given answer.

Here is the given answer:
- Given Answer: {answer}

Follow these instructions to determine if the given answer is legitimate:
1. Analyze the given answer to see if it provides a meaningful and specific response.
2. Check if the answer is a placeholder or non-informative.

Format your response as follows:
```json
{{
    "given_answer": "{answer}",
    "thought_process": "<Fill in your thought process here, how do you determine if the given answer is legitimate or not?>",
    "is_legitimate": <true_or_false>
}}
```

Here are some examples of checking the correctness of the given answer:

Example 1:
- Given Answer: "Chauncey Billups"
```json
{{
    "given_answer": "Chauncey Billups",
    "thought_process": "The answer 'Chauncey Billups' is a legitimate response to the question.",
    "is_legitimate": true
}}
```

Example 2:
- Given Answer: "No answer found"
```json
{{
    "given_answer": "No answer found",
    "thought_process": "The answer 'No answer found' is a placeholder response indicating a lack of information or a missing answer.",
    "is_legitimate": false
}}
```

Example 3:
- Given Answer: "There is no information in the context about a celebrated American animator known for a distinctive style",
```json
{{
    "given_answer": "There is no information in the context about a celebrated American animator known for a distinctive style",
    "thought_process": "The answer 'There is no information in the context about a celebrated American animator known for a distinctive style' is a placeholder response indicating a lack of information in the context.",
    "is_legitimate": false
}}
```

Example 4:
- Given Answer: "No relevant information provided in the context"
```json
{{
    "given_answer": "No relevant information provided in the context",
    "thought_process": "The answer 'No relevant information provided in the context' is a placeholder response indicating a lack of relevant information to answer the question.",
    "is_legitimate": false
}}
```

Example 5:
- Given Answer: "no"
```json
{{
    "given_answer": "no",
    "thought_process": "The answer 'no' is a legitimate response to the question.",
    "is_legitimate": true
}}
```
"""
        prompt = template.format(answer=answer)
        return prompt


# MATH
class MathPrompt:
    # decompose + execute
    def decompose(self, question: str):
        template = """

Format your response as the following json template:
```json
{{
    "original_question": "{question}",
    "thought_process": "<Fill in your thought process here, how do you decompose the complex question into simpler ones?>",
    "decomposed_questions": [
        {{
            "premise_variable": {{
                "name": "<variable_name>",
                "description": "<variable_description>"
            }}
            "question": "<First decomposed question>",
            "return": ["<returned_variable1>", "<returned_variable2>", ...],
            "predecessor": [<Index of the predecessor question in the decomposed_questions list>]
        }},
        {{
            "premise_variable": {{
                "name": "<variable_name>",
                "description": "<variable_description>"
            }}
            "question": "<Second decomposed question>",
            "return": ["<returned_variable1>", "<returned_variable2>", ...],
            "predecessor": [<Index of the predecessor question in the decomposed_questions list>]
        }},
        ...
    ]
}}
```
"""
        prompt = template.format(question=question)
        return prompt

    def execute(self, question: str):
        template = """

Format your response as the following json template:
```json
{{
    "question": "{question}",
    "thought_process": "<Fill in your thought process here, how do you analyze the context and arrive at the answer? Which segments in the context supported your answer?>",
    "code": "<Fill in the code snippet that can solve the question>",
}}
```
"""
        prompt = template.format(question=question)
        return prompt

    # cluster
    def duplicate(self, questions: list):
        # TODO：应该对变量和问题分别设置duplicate函数
        template = """"""

    # restructure
    def predecessor(self, original_question: str, question: str, candidates: list):
        template = """"""

    def convergence(self, original_question: str, candidates: list):
        template = """"""

    def summarize(self, original_question: str, candidates: list):
        template = """"""

    def majority(self, question: str, answers: list):
        template = """"""

    # OT
    def stage(self, original_question: str, reasoning_chain: list):
        template = """"""

    def evaluate(self, original_question: str, questions: list, k: int = 1):
        template = """"""
