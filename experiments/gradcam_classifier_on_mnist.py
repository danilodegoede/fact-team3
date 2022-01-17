"""Script to visualize GradCAM outputs with models trained on MNIST."""
import os
import sys
import argparse
import numpy as np
import torch
from torchvision import transforms
from torchvision.utils import save_image
from tqdm import tqdm
from gradcam.utils import visualize_cam
from gradcam import GradCAM, GradCAMpp

import warnings
warnings.filterwarnings("ignore")

from experiment_utils import set_env, REPO_PATH
set_env()

from cgn_framework.mnists.models.classifier import CNN
from cgn_framework.mnists.train_cgn import save
from cgn_framework.mnists.dataloader import get_tensor_dataloaders, TENSOR_DATASETS


def main(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load model and its weights from a checkpoint
    model = CNN()
    print("Loading model weights from checkpoint: {}".format(args.ckpt_path))
    ckpt = torch.load(os.path.join(REPO_PATH, "cgn_framework", args.ckpt_path), map_location='cpu')
    model.load_state_dict(ckpt)
    model = model.eval()
    model = model.to(device)

    # load the test dataloader to evaluate GradCAM on
    print("Loading dataset: {}".format(args.dataset))
    dl_train, dl_test = get_tensor_dataloaders(args.dataset, args.batch_size)

    # save sample images from the test set
    args.num_samples = 16
    images = []
    for i, (data, target) in enumerate(dl_test):
        data = data.to(device)
        output = model(data)
        pred = output.argmax(dim=1, keepdim=True)

        if len(images) + len(data) >= args.num_samples:
            indices = np.random.choice(len(data), args.num_samples, replace=False)
            images.append(data[indices])
            break
        else:
            images.append(data)
    images = torch.cat(images, 0)
    print("[Sample test set] Saving a grid of {} images".format(len(images)))
    save_path = os.path.join(REPO_PATH, "experiments/results", f"{args.dataset}_test_samples.png")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    save(images, save_path, n_row=4)

    # apply GradCAM on the test set
    print("Applying GradCAM on the test set")

    # define the target layer to be used
    target_layer = model.model[8]
    gradcam = GradCAM(model, target_layer)

    # loop over images
    for i in tqdm(range(len(images)), desc="Applying GradCAM on one image at a time"):
        image = images[i]
        mask, _ = gradcam(image.unsqueeze(0))
        heatmap, result = visualize_cam(mask, image)

        # save result for this image
        path = save_path.replace("test_samples", f"test_sample_{i}_gradcam")
        save_image([image.data, heatmap, result], path, nrow=3, padding=0, normalize=True)
    







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, choices=TENSOR_DATASETS,
                        help='Provide dataset name.')
    parser.add_argument('--batch_size', type=int, default=16, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--ckpt_path', type=str, required=True,
                        help='path to the classifier checkpoint')
    # parser.add_argument('--epochs', type=int, default=10, metavar='N',
    #                     help='number of epochs to train (default: 14)')
    # parser.add_argument('--lr', type=float, default=1.0, metavar='LR',
    #                     help='learning rate (default: 1.0)')
    # parser.add_argument('--gamma', type=float, default=0.7, metavar='M',
    #                     help='Learning rate step gamma (default: 0.7)')
    # parser.add_argument('--log-interval', type=int, default=100, metavar='N',
    #                     help='how many batches to wait before logging training status')
    args = parser.parse_args()

    print(args)
    main(args)