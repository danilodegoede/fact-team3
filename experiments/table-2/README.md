## Experiments to reproduce Table 2


### Introduction

This experiment is a reproduction of the results of Table 2 in the paper.
Results are reported in sheet `Table 2` in [this spreadsheet](https://docs.google.com/spreadsheets/d/19jrl_rQnsTDQahcWdqJPeW1T5FzWay7OE_rt_e96zEM/edit?usp=sharing).


#### Setup datasets
1. Download the datasets by following their commands to download. (Make sure you have `gdown`)

#### Train on original datasets

1. Create tensor datasets for each of those
   ```bash
   cd cgn-framework/
   python mnists/generate_data.py --dataset colored_MNIST
   python mnists/generate_data.py --dataset double_colored_MNIST
   python mnists/generate_data.py --dataset wildlife_MNIST
   ```
2. Train the classifier (replace dataset with the dataset you want to train on)
   ```bash
   python mnists/train_classifier.py --dataset colored_MNIST
   ```

#### Training on `Original + CGN`
1. Generate CF data for each dataset
2. Train the classifier

#### Training on `Original + GAN`
1. Currently, code for GAN is not available (architecture is also not known)


#### Training `IRM` (invariance via model)
1. Check out code [here](https://github.com/facebookresearch/InvariantRiskMinimization). See if we can use it out-of-the-box
2. Code for colored MNIST exists [here](https://github.com/facebookresearch/InvariantRiskMinimization/blob/main/code/colored_mnist/main.py)

#### Training `LNTL` (invariance via model) [code here](https://github.com/feidfoe/learning-not-to-learn)