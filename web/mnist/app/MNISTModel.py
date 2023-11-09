import torch.nn as nn
import torch
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
class Model(nn.Module):
  def __init__(self):
    super(Model,self).__init__()
    self.c0 = nn.Conv2d(1,5,5)
    self.p0 = nn.MaxPool2d(3)
    self.drop = nn.Dropout2d(0.5)
    self.c1 = nn.Conv2d(5,10,5)
    self.p1 = nn.MaxPool2d(2)
    self.f = nn.Flatten()
    self.l0 = nn.Linear(40,32)
    self.l1 = nn.Linear(32,18)
    self.l2 = nn.Linear(18,10)

  def forward(self,X):
    X = self.c0(X)
    X = self.p0(X)
    X = self.drop(X)
    X = self.c1(X)
    # X = self.drop(X)
    X = self.p1(X)
    X = self.f(X)
    X = self.l0(X)
    X = self.l1(X)
    X = self.l2(X)
    return X

class Run_Model():
    def __init__(self, model: Model, dataloader):
        self.dataloader = dataloader
        self.model = model

    def train(self,epochs, loss_func, optimizer, lr):
        self.model.train()
        self.criterion = loss_func
        self.optimizer = optimizer(self.model.parameters(), lr = lr)
        print('start training')
        epoch = 0
        for epoch in range(epochs):
            for img, label in self.dataloader:
                pred = self.model(img)
                loss = self.criterion(pred, label)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            print(f"epoch: {epoch}, loss: {loss.item()}")
        print('training done')
        self.loss = loss
        self.epoch = epoch
        return self.model

    def predict(self,img):
        self.model.eval()
        return self.model(img)

    def confusion_matrix(self, dataloader_test):
        pred = []
        true = []
        for img, label in dataloader_test:
            y_pred = self.model(img)
            for i in range(4):
                true.append(label[i].tolist().index(1))
                pred.append(y_pred[i].tolist().index(max(y_pred[i].tolist())))
        return confusion_matrix(true,pred)

    def save_model(self):
        checkpoint = {
            'MNIST_model': self.model.state_dict(),
            'loss': self.loss,
            'epoch': self.epoch,
            'optimizer': self.optimizer.state_dict()
        }
        torch.save(checkpoint, 'model.pth')
