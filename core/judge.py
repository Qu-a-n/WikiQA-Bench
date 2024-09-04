import torch
import torch.nn as nn
import torch.nn.functional as F
from core.utils import Memory, trainset_memory

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class judge(nn.Module):  # P(n_pre/sec|n_sec/pre, n_parent)
    def __init__(self, feature_dim=1536, vector_num=3, label_num=4):
        super(judge, self).__init__()
        self.fc1 = nn.Linear(feature_dim * vector_num, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, label_num)

    def forward(self, x1, x2):
        x = torch.cat((x1, x2), dim=1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        prob = F.softmax(x, dim=1)
        return prob

    def train(self, dataloader=None, epochs=100, lr=0.01):
        self.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        if dataloader is None:
            dataloader = self.get_dataloader()

        for epoch in range(epochs):
            acc = 0
            for inputs1, inputs2, labels in dataloader:
                inputs1 = inputs1.to(device)
                inputs2 = inputs2.to(device)
                labels = labels.to(device)

                outputs = self(inputs1, inputs2)
                loss = criterion(outputs, labels)
                acc += (outputs.argmax(dim=1) == labels).float().sum()

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            acc = acc / len(dataloader.dataset)

            print(f"[{epoch+1}/{epochs}]: Loss={loss.item()}, Acc={acc}")


def get_game24dataloader(mem: Memory):
    mem = trainset_memory() if mem is None else mem
    successed = mem.task_memory.successed
    predecessor = mem.task_memory.predecessor
    data = []
    for i in range(len(successed)):
        for j in range(1, len(successed)):
            data.append((successed[i], successed[j], 0))  # 无关关系
            data.append((successed[j], successed[i], 0))
    for k, v in predecessor.items():
        for i in v:
            data.append((k, i, 1))  # k是i的前驱
            data.append((i, k, 2))  # i是k的后继
    for i in range(len(successed)):
        data.append((successed[i], successed[i], 3))  # 重复关系


def get_hotpotqaloader(json_obj):
    data = []
    for obj in json_obj:
        for successor in obj["sub_questions"]:
            data.append(
                (obj["original_question"]["description"], successor["description"], 1)
            )
            data.append(
                (successor["description"], obj["original_question"]["description"], 2)
            )
    pass
