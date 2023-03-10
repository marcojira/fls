import torchvision
import torchvision.transforms as TF
import os
import shutil

from datasets.DatasetSet import DatasetSet
from datasets.SamplesDataset import SamplesDataset
from datasets.ImageNetSampleDataset import ImageNetSampleDataset


class ImageNetDatasetSet(DatasetSet):
    def __init__(self, slurm_tmpdir=None):
        super().__init__()
        self.name = "ImageNet"
        self.sample_datasets = []

        if slurm_tmpdir:
            self.load_dataset(slurm_tmpdir)
        else:
            self.train_dataset = ImageNetSampleDataset("imagenet_train", "train")
            self.test_dataset = ImageNetSampleDataset("imagenet_val", "val")

    def load_dataset(self, slurm_tmpdir):
        base_path = ""

        file_names = [
            "ILSVRC2012_img_val.tar",
            "ILSVRC2012_img_train.tar",
            "ILSVRC2012_devkit_t12.tar.gz",
        ]

        for file_name in file_names:
            shutil.copy(
                os.path.join(base_path, file_name),
                os.path.join(slurm_tmpdir, file_name),
            )

        self.train_dataset = torchvision.datasets.ImageNet(
            root=slurm_tmpdir,
            split="train",
            transform=TF.Compose(
                [TF.Resize((128, 128), interpolation=TF.InterpolationMode.BILINEAR)]
            ),
        )
        self.train_dataset.name = "imagenet_train"

        self.test_dataset = torchvision.datasets.ImageNet(
            root=slurm_tmpdir,
            split="val",
            transform=TF.Compose(
                [TF.Resize((128, 128), interpolation=TF.InterpolationMode.BILINEAR)]
            ),
        )
        self.test_dataset.name = "imagenet_val"
