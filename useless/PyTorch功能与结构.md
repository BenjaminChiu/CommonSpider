# PyTorch功能与结构

## PyTorch的两个核心功能

- 一个n维张量，类似与numpy，并且可以在GPU上运行
- 搭建和训练神经网络时的 自动微分(求导)机制

### 张量的理解（与计算框架对接）

现实中具象的图片、声音、文字 计算机是无法直接处理的。 Tensor的作用是将这些客观存在的东西 转化为计算机能够处理的数据表现形式。 即万物皆可转化为tensor，或者说 tensor是对万物的抽象。

"tensor"这个单词一般可译作“张量”，张量可以看作是一个多维数组。这个数组中包含有需要处理目标的数字属性，以此来模拟目标。

- 标量（scalar） 可以看作是 0维张量
- 向量（vector 矢量） 可以看作 1维张量
- 矩阵（matrix） 可以看作是 2维张量
- 张量，三维以上（含三维）数组

> 如何理解多少维？维度是多少？
>
> 答：
>
> - 没有数组
> - 一个数组
> - 二维数组：数组中被包含最深的元素是2个中括号，[ [1,2] , [7,9] ]
> - 三维数组：数组中被包含最深的元素是3个中括号，[ [ [1,2] , [7,9] ] , [ [6] , [70,9] ] ]

## 通用并行计算_异构计算

### 异步计算

默认情况下，PyTorch中的 GPU 操作是异步的。当调用一个使用 GPU 的函数时，这些操作会在特定的设备上排队但不一定会在稍后立即执行。

这就使我们可以并行更多的计算，包括 CPU 或其他 GPU 上的操作。

一般情况下，异步计算的效果对调用者是不可见的，因为 （1）每个设备按照它们排队的顺序执行操作， （2）在 CPU 和 GPU 之间或两个 GPU 之间复制数据时，PyTorch会自动执行必要的同步操作。

因此，计算将按每个操作同步执行的方式进行。 可以通过设置环境变量CUDA_LAUNCH_BLOCKING = 1来强制进行同步计算。当 GPU 产生error时，这可能非常有用。（异步执行时，只有在实际执行操作之后才会报告此类错误，因此堆栈跟踪不会显示请求的位置。）

### 自动并行计算

PyTorch能有效地实现在不同设备上自动并行计算。

### 多GPU计算（单主机多GPU 区别与 分布式计算）

查询显卡信息 nvidia-smi

要想使用PyTorch进行多GPU计算，最简单的方法是直接用torch.nn.DataParallel将模型wrap一下即可 默认所有存在的GPU都会被使用。 net = torch.nn.DataParallel(net)

### 多GPU模型的保存与加载

```python
正确的方法是保存的时候只保存net.module:

torch.save(net.module.state_dict(), "./8.4_model.pt")
new_net.load_state_dict(torch.load("./8.4_model.pt"))  # 加载成功
```

## 1. 搭建模型

```python
class TheModelClass(nn.Module):
    def __init__(self):
        super(TheModelClass, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
```

模型中必须要定义 `forward()` 函数，用于实现数据的前向传播。 可以在 `forward` 函数中使用任何针对 Tensor 的操作。
`forward()`(前向传播)会产生计算图，图中的节点是tensor，边是函数，这些函数是输出tensor到输入tensor的映射。这张计算图使得在网络中进行反向传播时，梯度的计算变得容易。

`backward` 函数（用来计算梯度）会被 `autograd`自动创建。
`backward`会释放计算图

## 2. Autograd 自动求导

autograd为张量上的所有操作提供了自动求导。它是一个运行时定义的框架，这意味着反向传播是根据你的代码来确定如何运行。

`torch.Tensor` 是这个包的核心类。如果设置 `.requires_grad` 为 `True`，那么将会追踪所有对于该张量的操作。当完成计算后通过调用 `.backward()` 会自动计算所有的梯度，这个张量的所有梯度将会自动积累到 `.grad` 属性。这也就完成了自动求导的过程。

自动求导中还有另外一个重要的类 `Function`。`Tensor` 和 `Function` 互相连接并生成一个非循环图，其存储了完整的计算历史。

#### 梯度的累积的作用？

实现低显存跑大batchsize，详情见（DL_个人理解\模型调优）

#### 自动求导运算本质：

`forward`函数计算从输入Tensors获得的输出Tensors。

`backward`函数接收输出Tensors对于某个标量值的梯度，并且计算输入Tensors相对于该相同标量值的梯度。

#### 自动求导可自定义

继承`torch.autograd.Function`并定义`forward`和`backward`函数

```python
class MyReLU(torch.autograd.Function):
    """
    我们可以通过建立torch.autograd的子类来实现我们自定义的autograd函数，
    并完成张量的正向和反向传播。
    """

    @staticmethod
    def forward(ctx, x):
        """
        在正向传播中，我们接收到一个上下文对象和一个包含输入的张量；
        我们必须返回一个包含输出的张量，
        并且我们可以使用上下文对象来缓存对象，以便在反向传播中使用。
        """
        ctx.save_for_backward(x)
        return x.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        """
        在反向传播中，我们接收到上下文对象和一个张量，
        其包含了相对于正向传播过程中产生的输出的损失的梯度。
        我们可以从上下文对象中检索缓存的数据，
        并且必须计算并返回与正向传播的输入相关的损失的梯度。
        """
        x, = ctx.saved_tensors
        grad_x = grad_output.clone()
        grad_x[x < 0] = 0
        return grad_x
```

## 3. 模型、张量等的保存与读取

当保存和加载模型时，需要熟悉三个核心功能：

`torch.save`：将序列化对象保存到磁盘。此函数使用Python的`pickle`模块进行序列化。使用此函数可以保存如模型、tensor、字典等各种对象。
`torch.load`：使用pickle的unpickling功能将pickle对象文件反序列化到内存。此功能还可以有助于设备加载数据。
`torch.nn.Module.load_state_dict`：使用反序列化函数 state_dict 来加载模型的参数字典。

### 什么是状态字典：state_dict

`state_dict`是Python字典对象，因此它可以很容易地保存、更新、修改、恢复。 它将每一层映射到其参数张量。注意，只有具有可学习参数的层（如卷积层，线性层等）的模型 才具有`state_dict`这一项。目标优化`torch.optim`也有`state_dict`属性，它包含有关优化器的状态信息，以及使用的超参数。

#### 1. 只保存/加载 模型参数(state_dict)

```python
保存：
torch.save(model.state_dict(), PATH + xx.pt / xx.pth)

加载：
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH))
model.eval()

# load_state_dict()函数只接受字典对象，而不是保存对象的路径。
# 传给load_state_dict()函数之前，必须反序列化所保存的state_dict。
# 例如，你无法通过 model.load_state_dict(PATH)来加载模型。
```

注意： 在运行推理之前，务必调用model.eval()去设置 dropout 和 batch normalization 层为评估模式。如果不这么做，可能导致 模型推断结果不一致。 否则的话，有输入数据，即使不训练，它也会改变权值。这是model中含有batch normalization层所带来的的性质。

#### 5. 不同模型参数下的热启动模式

```python

保存：
torch.save(modelA.state_dict(), PATH)

加载：
modelB = TheModelBClass(*args, **kwargs)
modelB.load_state_dict(torch.load(PATH), strict=False)
```

通过strict=False，来忽略非匹配键的函数（缺少某些键的 state_dict 加载；从键的数目多于加载模型的 state_dict）

如果要将参数从一个层加载到另一个层，但是某些键不匹配，主要修改正在加载的 state_dict 中的参数键的名称以匹配要在加载到模型中的键即可。

#### 6. 通过设备保存、加载模型

##### 加载到CPU

```python

# 保存代码都是一样的，参考第一个
torch.save(model.state_dict(), PATH)
# 加载
device = torch.device('cpu')
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH, map_location=device))

```

注意：map_location=device

##### 加载到GPU

```python
保存：
torch.save(model.state_dict(), PATH)
加载：
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH))
model.to(torch.device("cuda"))
```

确保 模型的任何输入张量 调用input = input.to(device)

##### 保存到CPU，加载到GPU

```python

torch.save(model.state_dict(), PATH)

加载：
device = torch.device("cuda")
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH, map_location="cuda:0"))  # Choose whatever GPU device number you want
model.to(device)
# 确保在你提供给模型的任何输入张量上调用input = input.to(device)

```

#### 3. 断点续'练'

```python
1.
保存
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    ...
}, PATH)

2.
加载
model = TheModelClass(*args, **kwargs)
optimizer = TheOptimizerClass(*args, **kwargs)

checkpoint = torch.load(PATH)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

model.eval()
# - or -
model.train()


```

组件还可以包括：外部的torch.nn.Embedding层

要保存多个组件，请在字典中组织它们并使用torch.save()来序列化字典。 PyTorch 中常见的保存checkpoint 是使用 .tar 文件扩展名。

#### 4. 在一个文件中保存多个模型

```python
1.
保存
torch.save({
    'modelA_state_dict': modelA.state_dict(),
    'modelB_state_dict': modelB.state_dict(),
    'optimizerA_state_dict': optimizerA.state_dict(),
    'optimizerB_state_dict': optimizerB.state_dict(),
    ...
}, PATH)

2.
加载
modelA = TheModelAClass(*args, **kwargs)
modelB = TheModelBClass(*args, **kwargs)
optimizerA = TheOptimizerAClass(*args, **kwargs)
optimizerB = TheOptimizerBClass(*args, **kwargs)

checkpoint = torch.load(PATH)
modelA.load_state_dict(checkpoint['modelA_state_dict'])
modelB.load_state_dict(checkpoint['modelB_state_dict'])
optimizerA.load_state_dict(checkpoint['optimizerA_state_dict'])
optimizerB.load_state_dict(checkpoint['optimizerB_state_dict'])

modelA.eval()
modelB.eval()
# - or -
modelA.train()
modelB.train()

此种方法思路：保存每个模型的
state_dict
的字典和相对应的优化器
```

当一个模型由多个torch.nn.Modules组成时，例如GAN(对抗生成网络)、sequence-to-sequence (序列到序列模型), 或者是多个模型融合, 可以采用这种与保存常规检查点相同的方法。

#### 2. 保存/加载完整模型

```python
保存：
torch.save(model, PATH + xx.pt / xx.pth)

加载：
model = torch.load(PATH + xx.pt / xx.pth)

参数解释：
# PATH为路径，推荐的文件后缀名是pt或pth
# type(model)  =>  torch.nn.Module
```

以 Python `pickle` 模块的方式来保存模型。这种方法的缺点是 序列化数据受限于某种特殊的类而且需要确切的字典结构。这是因为pickle无法保存模型类本身。

#### 保存torch.nn.DataParallel模型

```python
# 保存 多了module
torch.save(model.module.state_dict(), PATH)
# 加载 到任何想要的设备

```

使用场景：支持并行GPU

## 高度抽象接口

TensorFlow中有类似Keras、TensorFlow-Slim、TFLearn这种封装了底层计算图的高度抽象的接口

PyTorch中有模块`torch.nn`

在PyTorch中，`torch.nn.Module`模型的可学习参数（即权重和偏差）包含在模型的参数中，（使用`model.parameters()`可以进行访问）。

#### torch.nn可自定义

继承`torch.nn.Module`并定义`forward`函数

```python
class TwoLayerNet(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        """
        在构造函数中，我们实例化了两个nn.Linear模块，并将它们作为成员变量。
        """
        super(TwoLayerNet, self).__init__()
        self.linear1 = torch.nn.Linear(D_in, H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, x):
        """
        在前向传播的函数中，我们接收一个输入的张量，也必须返回一个输出张量。
        我们可以使用构造函数中定义的模块以及张量上的任意的（可微分的）操作。
        """
        h_relu = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(h_relu)
        return y_pred
```