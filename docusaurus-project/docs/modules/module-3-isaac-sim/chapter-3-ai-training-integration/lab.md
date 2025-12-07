---
title: Chapter 3 Lab - Synthetic Dataset Training
sidebar_position: 4
description: Lab exercise to export a synthetic dataset and train a simple vision classifier using Isaac Sim data.
---

# Chapter 3 Lab: Synthetic Dataset Training

## Objective

In this lab, you will learn how to export a synthetic dataset from Isaac Sim, create PyTorch data loaders for the synthetic data, and train a simple vision classifier. This hands-on exercise will help you understand the complete workflow from synthetic data generation to AI model training.

## Prerequisites

- NVIDIA Isaac Sim installed and running
- Ubuntu 22.04 with ROS 2 Humble installed
- Python 3.8+ with PyTorch, torchvision, and NumPy
- Completion of Chapter 1-2 labs
- Basic understanding of deep learning concepts

## Estimated Time

120-150 minutes

## Lab Setup

### Step 1: Install Required Dependencies

Install the necessary Python packages for deep learning:

```bash
pip3 install torch torchvision torchaudio
pip3 install opencv-python numpy pillow matplotlib scikit-learn
```

### Step 2: Create Workspace

Create a new directory for the lab:

```bash
mkdir -p ~/isaac_ai_training_ws
cd ~/isaac_ai_training_ws
```

### Step 3: Create Lab Package

Create a package for the AI training lab:

```bash
mkdir -p ~/isaac_ai_training_ws/ai_training_lab
mkdir -p ~/isaac_ai_training_ws/ai_training_lab/data
mkdir -p ~/isaac_ai_training_ws/ai_training_lab/models
mkdir -p ~/isaac_ai_training_ws/ai_training_lab/utils
```

## Lab Exercises

### Exercise 1: Create Synthetic Data Exporter

In this exercise, you'll create a script to export synthetic data from Isaac Sim in a format suitable for training.

#### Step 1: Create Data Export Script

Create `~/isaac_ai_training_ws/ai_training_lab/data_exporter.py`:

```python
#!/usr/bin/env python3
"""
Synthetic Data Exporter for Isaac Sim
This script demonstrates how to export synthetic data from Isaac Sim for AI training
"""

import os
import json
import numpy as np
import cv2
from datetime import datetime
import pickle

class SyntheticDataExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.data_counter = 0

        # Create output directories
        os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'annotations'), exist_ok=True)

        # Data statistics
        self.stats = {
            'total_samples': 0,
            'class_distribution': {},
            'export_timestamps': []
        }

    def export_single_sample(self, rgb_image, depth_image, segmentation_mask,
                           bounding_boxes, class_labels, sample_id=None):
        """
        Export a single synthetic sample with all associated data

        Args:
            rgb_image: RGB image array
            depth_image: Depth image array
            segmentation_mask: Segmentation mask array
            bounding_boxes: List of bounding boxes [[x, y, w, h], ...]
            class_labels: List of class labels for each bounding box
            sample_id: Optional custom sample ID
        """
        if sample_id is None:
            sample_id = f"sample_{self.data_counter:06d}"

        # Save RGB image
        rgb_path = os.path.join(self.output_dir, 'images', f"{sample_id}.png")
        cv2.imwrite(rgb_path, cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))

        # Save depth image
        depth_path = os.path.join(self.output_dir, 'images', f"{sample_id}_depth.png")
        cv2.imwrite(depth_path, (depth_image * 255).astype(np.uint8))

        # Save segmentation mask
        seg_path = os.path.join(self.output_dir, 'images', f"{sample_id}_seg.png")
        cv2.imwrite(seg_path, segmentation_mask.astype(np.uint8))

        # Create annotation data
        annotation_data = {
            'sample_id': sample_id,
            'image_path': rgb_path,
            'depth_path': depth_path,
            'seg_path': seg_path,
            'bounding_boxes': bounding_boxes,
            'class_labels': class_labels,
            'timestamp': datetime.now().isoformat(),
            'image_shape': rgb_image.shape
        }

        # Save annotation as JSON
        annot_path = os.path.join(self.output_dir, 'annotations', f"{sample_id}.json")
        with open(annot_path, 'w') as f:
            json.dump(annotation_data, f, indent=2)

        # Update statistics
        for label in class_labels:
            if label not in self.stats['class_distribution']:
                self.stats['class_distribution'][label] = 0
            self.stats['class_distribution'][label] += 1

        self.stats['total_samples'] += 1
        self.stats['export_timestamps'].append(datetime.now().isoformat())

        self.data_counter += 1

        print(f"Exported sample {sample_id} with {len(class_labels)} objects")

    def export_classification_dataset(self, images, labels, class_names):
        """
        Export a classification dataset

        Args:
            images: List of RGB images
            labels: List of class labels (integers)
            class_names: List of class names
        """
        for i, (img, label) in enumerate(zip(images, labels)):
            sample_id = f"classification_{i:06d}"

            # Save image
            img_path = os.path.join(self.output_dir, 'images', f"{sample_id}.png")
            cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

            # Save class label
            label_path = os.path.join(self.output_dir, 'labels', f"{sample_id}.txt")
            with open(label_path, 'w') as f:
                f.write(f"{label}\n")

            # Save annotation with class name
            annotation_data = {
                'sample_id': sample_id,
                'image_path': img_path,
                'class_id': label,
                'class_name': class_names[label],
                'timestamp': datetime.now().isoformat()
            }

            annot_path = os.path.join(self.output_dir, 'annotations', f"{sample_id}.json")
            with open(annot_path, 'w') as f:
                json.dump(annotation_data, f, indent=2)

            # Update statistics
            class_name = class_names[label]
            if class_name not in self.stats['class_distribution']:
                self.stats['class_distribution'][class_name] = 0
            self.stats['class_distribution'][class_name] += 1

        self.stats['total_samples'] += len(images)
        print(f"Exported {len(images)} classification samples")

    def create_metadata_file(self):
        """Create a metadata file with dataset statistics"""
        metadata_path = os.path.join(self.output_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(self.stats, f, indent=2)

        print(f"Dataset statistics saved to {metadata_path}")
        print(f"Total samples: {self.stats['total_samples']}")
        print(f"Class distribution: {self.stats['class_distribution']}")

    def generate_sample_data(self, num_samples=100):
        """
        Generate sample synthetic data for testing
        In a real scenario, this would interface with Isaac Sim
        """
        print(f"Generating {num_samples} sample synthetic data points...")

        class_names = ['cube', 'sphere', 'cylinder', 'robot']

        for i in range(num_samples):
            # Generate synthetic RGB image with colored shapes
            height, width = 224, 224
            rgb_img = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)  # Dark background

            # Add random shapes
            num_shapes = np.random.randint(1, 4)
            class_labels = []

            for j in range(num_shapes):
                shape_type = np.random.choice(['cube', 'sphere', 'cylinder'])
                class_labels.append(shape_type)

                # Random position and size
                x = np.random.randint(20, width - 40)
                y = np.random.randint(20, height - 40)
                w = np.random.randint(20, 60)
                h = np.random.randint(20, 60)

                # Random color
                color = np.random.randint(100, 255, 3)

                if shape_type == 'cube':
                    cv2.rectangle(rgb_img, (x, y), (x + w, y + h), color.tolist(), -1)
                elif shape_type == 'sphere':
                    center = (x + w//2, y + h//2)
                    radius = min(w, h) // 2
                    cv2.circle(rgb_img, center, radius, color.tolist(), -1)
                elif shape_type == 'cylinder':
                    center = (x + w//2, y + h//2)
                    axes = (w//2, h//2)
                    cv2.ellipse(rgb_img, center, axes, 0, 0, 360, color.tolist(), -1)

            # Generate corresponding depth image (simplified)
            depth_img = np.ones((height, width), dtype=np.float32) * 2.0  # 2 meters

            # Generate segmentation mask (simplified)
            seg_mask = np.zeros((height, width), dtype=np.uint8)
            for j in range(num_shapes):
                # Assign different class IDs to different shapes
                class_id = ['cube', 'sphere', 'cylinder'].index(class_labels[j]) + 1
                # In real implementation, this would be more sophisticated
                seg_mask = np.random.randint(0, len(class_names), (height, width))

            # Generate bounding boxes
            bboxes = []
            for j in range(num_shapes):
                x = np.random.randint(20, width - 40)
                y = np.random.randint(20, height - 40)
                w = np.random.randint(20, 60)
                h = np.random.randint(20, 60)
                bboxes.append([x, y, w, h])

            # Export the sample
            self.export_single_sample(
                rgb_image=rgb_img,
                depth_image=depth_img,
                segmentation_mask=seg_mask,
                bounding_boxes=bboxes,
                class_labels=class_labels
            )

# Example usage
if __name__ == "__main__":
    exporter = SyntheticDataExporter("./synthetic_dataset")
    exporter.generate_sample_data(num_samples=50)  # Generate 50 sample images
    exporter.create_metadata_file()
    print("Sample data export completed!")
```

#### Step 2: Create Isaac Sim Integration Script

Create `~/isaac_ai_training_ws/ai_training_lab/isaac_data_collector.py`:

```python
#!/usr/bin/env python3
"""
Isaac Sim Data Collector
This script demonstrates how to collect data from Isaac Sim for training
"""

import numpy as np
import os
from datetime import datetime

class IsaacSimDataCollector:
    def __init__(self, scene_config):
        self.scene_config = scene_config
        self.data_exporter = None

        # Simulation properties
        self.world = None
        self.cameras = []
        self.lidars = []

        print("Isaac Sim Data Collector initialized")

    def setup_scene(self):
        """Setup Isaac Sim scene for data collection"""
        print("Setting up Isaac Sim scene...")

        # In a real implementation, this would:
        # 1. Load the configured scene
        # 2. Setup cameras and sensors
        # 3. Configure lighting and objects
        # 4. Set up semantic segmentation
        pass

    def collect_single_frame(self):
        """Collect a single frame of data from Isaac Sim"""
        # In a real Isaac Sim implementation, this would:
        # 1. Get RGB image from camera
        # 2. Get depth image from camera
        # 3. Get segmentation mask
        # 4. Get LiDAR point cloud
        # 5. Get bounding box annotations
        # 6. Get object poses

        # For this lab, we'll simulate the data collection
        height, width = 224, 224

        # Simulate RGB image
        rgb_img = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)

        # Simulate depth image
        depth_img = np.random.uniform(1.0, 10.0, (height, width)).astype(np.float32)

        # Simulate segmentation mask
        seg_mask = np.random.randint(0, 5, (height, width)).astype(np.uint8)

        # Simulate bounding boxes and labels
        num_objects = np.random.randint(1, 4)
        bboxes = []
        labels = []

        for i in range(num_objects):
            x = np.random.randint(10, width - 30)
            y = np.random.randint(10, height - 30)
            w = np.random.randint(20, 50)
            h = np.random.randint(20, 50)
            bboxes.append([x, y, w, h])

            label = np.random.choice(['cube', 'sphere', 'cylinder', 'robot'])
            labels.append(label)

        return {
            'rgb': rgb_img,
            'depth': depth_img,
            'segmentation': seg_mask,
            'bounding_boxes': bboxes,
            'class_labels': labels
        }

    def collect_dataset(self, num_samples=100, output_dir="./isaac_synthetic_data"):
        """Collect a dataset of synthetic images"""
        print(f"Collecting {num_samples} samples...")

        # Initialize exporter
        from data_exporter import SyntheticDataExporter
        self.data_exporter = SyntheticDataExporter(output_dir)

        for i in range(num_samples):
            # Collect frame data
            frame_data = self.collect_single_frame()

            # Export the sample
            self.data_exporter.export_single_sample(
                rgb_image=frame_data['rgb'],
                depth_image=frame_data['depth'],
                segmentation_mask=frame_data['segmentation'],
                bounding_boxes=frame_data['bounding_boxes'],
                class_labels=frame_data['class_labels'],
                sample_id=f"isaac_{i:06d}"
            )

            if i % 10 == 0:
                print(f"Collected {i}/{num_samples} samples")

        # Create metadata file
        self.data_exporter.create_metadata_file()
        print(f"Dataset collection completed! Saved to {output_dir}")

    def collect_classification_dataset(self, num_samples=200, output_dir="./classification_data"):
        """Collect a classification-specific dataset"""
        print(f"Collecting classification dataset with {num_samples} samples...")

        # Initialize exporter
        from data_exporter import SyntheticDataExporter
        exporter = SyntheticDataExporter(output_dir)

        # Define class names
        class_names = ['cube_red', 'cube_blue', 'sphere_red', 'sphere_blue',
                      'cylinder_red', 'cylinder_blue', 'robot', 'obstacle']

        images = []
        labels = []

        for i in range(num_samples):
            # Generate synthetic image
            height, width = 224, 224
            img = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)  # Dark background

            # Choose a random class
            class_idx = np.random.randint(0, len(class_names))
            class_name = class_names[class_idx]

            # Add object based on class
            if 'cube' in class_name:
                x, y, w, h = 50, 50, 124, 124
                color = [255, 0, 0] if 'red' in class_name else [0, 0, 255]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
            elif 'sphere' in class_name:
                center = (112, 112)
                radius = 80
                color = [255, 0, 0] if 'red' in class_name else [0, 0, 255]
                cv2.circle(img, center, radius, color, -1)
            elif 'cylinder' in class_name:
                center = (112, 112)
                axes = (90, 60)
                color = [255, 0, 0] if 'red' in class_name else [0, 0, 255]
                cv2.ellipse(img, center, axes, 0, 0, 360, color, -1)
            elif 'robot' in class_name:
                # Draw a simple robot shape
                cv2.rectangle(img, (80, 80), (144, 144), [100, 100, 100], -1)  # Body
                cv2.circle(img, (100, 70), 20, [200, 200, 200], -1)  # Head
                cv2.circle(img, (90, 65), 5, [0, 0, 0], -1)  # Eye
                cv2.circle(img, (110, 65), 5, [0, 0, 0], -1)  # Eye
            elif 'obstacle' in class_name:
                # Draw a complex obstacle
                pts = np.array([[50, 50], [100, 30], [150, 80], [120, 150], [60, 130]], np.int32)
                cv2.fillPoly(img, [pts], [150, 75, 0])

            images.append(img)
            labels.append(class_idx)

        # Export the classification dataset
        exporter.export_classification_dataset(images, labels, class_names)
        exporter.create_metadata_file()
        print(f"Classification dataset collection completed! Saved to {output_dir}")

# Example usage (when running inside Isaac Sim)
if __name__ == "__main__":
    collector = IsaacSimDataCollector(scene_config={})
    collector.collect_classification_dataset(num_samples=200)
```

### Exercise 2: Create PyTorch Data Loaders

Now you'll create PyTorch data loaders for the synthetic dataset.

#### Step 1: Create Custom Dataset Class

Create `~/isaac_ai_training_ws/ai_training_lab/dataset.py`:

```python
import torch
from torch.utils.data import Dataset
import os
import cv2
import json
import numpy as np
from PIL import Image
from torchvision import transforms
import random

class IsaacSimClassificationDataset(Dataset):
    """Dataset class for Isaac Sim synthetic classification data"""

    def __init__(self, data_dir, transform=None, task='classification'):
        """
        Args:
            data_dir (str): Directory containing the dataset
            transform: Optional transform to be applied on images
            task (str): Type of task ('classification', 'detection')
        """
        self.data_dir = data_dir
        self.transform = transform
        self.task = task

        # Load image paths and labels
        self.image_paths = []
        self.labels = []
        self.annotations = []

        # Discover all images and their annotations
        images_dir = os.path.join(data_dir, 'images')
        annotations_dir = os.path.join(data_dir, 'annotations')

        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Skip depth and segmentation images
                if not any(x in filename for x in ['_depth', '_seg']):
                    base_name = os.path.splitext(filename)[0]

                    # Check if corresponding annotation exists
                    annot_file = f"{base_name}.json"
                    annot_path = os.path.join(annotations_dir, annot_file)

                    if os.path.exists(annot_path):
                        img_path = os.path.join(images_dir, filename)

                        # Load annotation
                        with open(annot_path, 'r') as f:
                            annotation = json.load(f)

                        if 'class_id' in annotation:  # Classification task
                            self.image_paths.append(img_path)
                            self.labels.append(annotation['class_id'])
                            self.annotations.append(annotation)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image
        img_path = self.image_paths[idx]
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        # Get label
        label = self.labels[idx]

        return image, label

class IsaacSimDetectionDataset(Dataset):
    """Dataset class for Isaac Sim synthetic detection data"""

    def __init__(self, data_dir, transform=None):
        """
        Args:
            data_dir (str): Directory containing the dataset
            transform: Optional transform to be applied on images
        """
        self.data_dir = data_dir
        self.transform = transform

        # Load image paths and annotations
        self.image_paths = []
        self.annotations = []

        images_dir = os.path.join(data_dir, 'images')
        annotations_dir = os.path.join(data_dir, 'annotations')

        # Class mapping (update based on your specific classes)
        self.class_to_idx = {
            'cube': 1,
            'sphere': 2,
            'cylinder': 3,
            'robot': 4,
            'obstacle': 5
        }

        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Skip depth and segmentation images
                if not any(x in filename for x in ['_depth', '_seg']):
                    base_name = os.path.splitext(filename)[0]

                    # Check if corresponding annotation exists
                    annot_file = f"{base_name}.json"
                    annot_path = os.path.join(annotations_dir, annot_file)

                    if os.path.exists(annot_path):
                        img_path = os.path.join(images_dir, filename)

                        # Load annotation
                        with open(annot_path, 'r') as f:
                            annotation = json.load(f)

                        # Validate annotation
                        if 'bounding_boxes' in annotation and 'class_labels' in annotation:
                            self.image_paths.append(img_path)
                            self.annotations.append(annotation)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image
        img_path = self.image_paths[idx]
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Load annotation
        annotation = self.annotations[idx]

        # Extract bounding boxes and labels
        boxes = []
        labels = []

        for bbox, class_label in zip(annotation['bounding_boxes'], annotation['class_labels']):
            x, y, w, h = bbox
            boxes.append([x, y, x + w, y + h])  # Convert to [x1, y1, x2, y2] format
            labels.append(self.class_to_idx.get(class_label, 0))

        # Convert to tensors
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)

        # Create target dictionary
        target = {
            'boxes': boxes,
            'labels': labels,
            'image_id': torch.tensor([idx])
        }

        # Apply transforms
        if self.transform:
            # Convert image to PIL for transforms
            image = Image.fromarray(image)
            image = self.transform(image)
        else:
            # Convert to tensor directly
            image = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0

        return image, target

def get_transforms(train=True):
    """Get standard transforms for training/validation"""
    if train:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])

    return transform

def create_data_loaders(data_dir, batch_size=32, train_ratio=0.8):
    """Create training and validation data loaders"""
    # Get transforms
    train_transform = get_transforms(train=True)
    val_transform = get_transforms(train=False)

    # Load full dataset
    full_dataset = IsaacSimClassificationDataset(data_dir, transform=None)

    # Split into train and validation
    dataset_size = len(full_dataset)
    train_size = int(train_ratio * dataset_size)
    val_size = dataset_size - train_size

    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size]
    )

    # Apply transforms to the split datasets
    train_dataset.dataset.transform = train_transform
    val_dataset.dataset.transform = val_transform

    # Create data loaders
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )

    return train_loader, val_loader
```

#### Step 2: Create Data Loading Utilities

Create `~/isaac_ai_training_ws/ai_training_lab/utils/data_utils.py`:

```python
import torch
import torchvision.transforms as transforms
import os
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def visualize_batch(dataloader, num_samples=8):
    """Visualize a batch of data from the dataloader"""
    # Get a batch of data
    data_iter = iter(dataloader)
    images, labels = next(data_iter)

    # Denormalize images for visualization
    mean = torch.tensor([0.485, 0.456, 0.406])
    std = torch.tensor([0.229, 0.224, 0.225])

    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    axes = axes.ravel()

    for i in range(min(num_samples, len(images))):
        # Denormalize
        img = images[i].permute(1, 2, 0)  # C, H, W -> H, W, C
        img = img * std + mean
        img = torch.clamp(img, 0, 1)

        axes[i].imshow(img)
        axes[i].set_title(f'Label: {labels[i].item()}')
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

def get_class_names_from_metadata(metadata_path):
    """Extract class names from metadata file"""
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # If classification dataset, return class distribution keys
        if 'class_distribution' in metadata:
            return list(metadata['class_distribution'].keys())

    # Default class names
    return ['cube', 'sphere', 'cylinder', 'robot', 'obstacle']

def analyze_dataset_stats(dataset_path):
    """Analyze dataset statistics"""
    metadata_path = os.path.join(dataset_path, 'metadata.json')

    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        print("Dataset Statistics:")
        print(f"Total samples: {metadata.get('total_samples', 0)}")
        print("Class distribution:")
        for class_name, count in metadata.get('class_distribution', {}).items():
            print(f"  {class_name}: {count}")

        return metadata
    else:
        print("Metadata file not found")
        return None

def create_balanced_subset(dataset, target_samples_per_class=100):
    """Create a balanced subset of the dataset"""
    # Get all labels
    all_labels = []
    for _, label in dataset:
        all_labels.append(label)

    all_labels = np.array(all_labels)

    # Find indices for each class
    unique_labels = np.unique(all_labels)
    selected_indices = []

    for label in unique_labels:
        class_indices = np.where(all_labels == label)[0]
        # Randomly select up to target_samples_per_class
        if len(class_indices) > target_samples_per_class:
            selected_class_indices = np.random.choice(
                class_indices, target_samples_per_class, replace=False
            )
        else:
            selected_class_indices = class_indices

        selected_indices.extend(selected_class_indices)

    # Create subset
    subset = torch.utils.data.Subset(dataset, selected_indices)
    return subset
```

### Exercise 3: Train a Simple Vision Classifier

Now you'll create and train a simple vision classifier using the synthetic data.

#### Step 1: Create the Model

Create `~/isaac_ai_training_ws/ai_training_lab/models/simple_classifier.py`:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

class SimpleClassifier(nn.Module):
    """Simple CNN classifier for synthetic data"""

    def __init__(self, num_classes=5, input_channels=3):
        super(SimpleClassifier, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)

        # Pooling
        self.pool = nn.MaxPool2d(2, 2)

        # Fully connected layers
        self.fc1 = nn.Linear(128 * 28 * 28, 512)  # Adjust based on input size
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, num_classes)

        # Dropout
        self.dropout = nn.Dropout(0.5)

        # Activation
        self.relu = nn.ReLU()

    def forward(self, x):
        # Convolutional layers with pooling
        x = self.pool(self.relu(self.bn1(self.conv1(x))))
        x = self.pool(self.relu(self.bn2(self.conv2(x))))
        x = self.relu(self.bn3(self.conv3(x)))

        # Flatten
        x = x.view(x.size(0), -1)

        # Fully connected layers
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)

        return x

class ResNetClassifier(nn.Module):
    """ResNet-based classifier using transfer learning"""

    def __init__(self, num_classes=5, pretrained=True):
        super(ResNetClassifier, self).__init__()

        # Load pretrained ResNet-18
        self.resnet = models.resnet18(pretrained=pretrained)

        # Replace the final fully connected layer
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.resnet(x)

def get_model(model_name='simple', num_classes=5):
    """Factory function to get model"""
    if model_name == 'simple':
        return SimpleClassifier(num_classes=num_classes)
    elif model_name == 'resnet':
        return ResNetClassifier(num_classes=num_classes)
    else:
        raise ValueError(f"Unknown model: {model_name}")
```

#### Step 2: Create Training Script

Create `~/isaac_ai_training_ws/ai_training_lab/train_classifier.py`:

```python
#!/usr/bin/env python3
"""
Training script for Isaac Sim synthetic data classifier
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt

from dataset import IsaacSimClassificationDataset, get_transforms, create_data_loaders
from models.simple_classifier import get_model
from utils.data_utils import visualize_batch, analyze_dataset_stats

def train_model(model, train_loader, val_loader, num_epochs=10,
                learning_rate=0.001, device='cuda'):
    """Train the model"""
    model = model.to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    # Training history
    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []

    best_val_acc = 0.0
    best_model_state = None

    print("Starting training...")

    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        start_time = time.time()

        for batch_idx, (data, targets) in enumerate(train_loader):
            data, targets = data.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Calculate accuracy
            _, predicted = torch.max(outputs.data, 1)
            total_train += targets.size(0)
            correct_train += (predicted == targets).sum().item()

            if batch_idx % 50 == 0:
                print(f'Epoch {epoch+1}/{num_epochs}, Batch {batch_idx}, '
                      f'Loss: {loss.item():.4f}')

        # Calculate epoch metrics
        epoch_train_loss = running_loss / len(train_loader)
        epoch_train_acc = 100 * correct_train / total_train

        # Validation phase
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for data, targets in val_loader:
                data, targets = data.to(device), targets.to(device)
                outputs = model(data)
                loss = criterion(outputs, targets)
                val_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total_val += targets.size(0)
                correct_val += (predicted == targets).sum().item()

        epoch_val_loss = val_loss / len(val_loader)
        epoch_val_acc = 100 * correct_val / total_val

        # Update scheduler
        scheduler.step()

        # Store metrics
        train_losses.append(epoch_train_loss)
        train_accuracies.append(epoch_train_acc)
        val_losses.append(epoch_val_loss)
        val_accuracies.append(epoch_val_acc)

        # Print epoch results
        epoch_time = time.time() - start_time
        print(f'Epoch {epoch+1}/{num_epochs} completed in {epoch_time:.2f}s')
        print(f'Train Loss: {epoch_train_loss:.4f}, Train Acc: {epoch_train_acc:.2f}%')
        print(f'Val Loss: {epoch_val_loss:.4f}, Val Acc: {epoch_val_acc:.2f}%')
        print('-' * 60)

        # Save best model
        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            best_model_state = model.state_dict().copy()

    # Load best model
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
        print(f'Best validation accuracy: {best_val_acc:.2f}%')

    return model, train_losses, train_accuracies, val_losses, val_accuracies

def plot_training_history(train_losses, train_accuracies, val_losses, val_accuracies):
    """Plot training history"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Plot losses
    ax1.plot(train_losses, label='Train Loss', marker='o')
    ax1.plot(val_losses, label='Validation Loss', marker='s')
    ax1.set_title('Training and Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)

    # Plot accuracies
    ax2.plot(train_accuracies, label='Train Accuracy', marker='o')
    ax2.plot(val_accuracies, label='Validation Accuracy', marker='s')
    ax2.set_title('Training and Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

def evaluate_model(model, test_loader, device='cuda'):
    """Evaluate the model on test data"""
    model.eval()
    correct = 0
    total = 0
    class_correct = {}
    class_total = {}

    with torch.no_grad():
        for data, targets in test_loader:
            data, targets = data.to(device), targets.to(device)
            outputs = model(data)
            _, predicted = torch.max(outputs, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()

            # Per-class accuracy
            for i in range(targets.size(0)):
                label = targets[i].item()
                pred = predicted[i].item()

                if label not in class_total:
                    class_total[label] = 0
                    class_correct[label] = 0

                class_total[label] += 1
                if label == pred:
                    class_correct[label] += 1

    overall_acc = 100 * correct / total
    print(f'Overall Test Accuracy: {overall_acc:.2f}%')

    print('Per-class accuracy:')
    for class_idx in sorted(class_total.keys()):
        acc = 100 * class_correct.get(class_idx, 0) / class_total[class_idx]
        print(f'  Class {class_idx}: {acc:.2f}% ({class_correct.get(class_idx, 0)}/{class_total[class_idx]})')

    return overall_acc

def main():
    """Main training function"""
    # Configuration
    data_dir = "./synthetic_dataset"  # Update this path to your dataset
    batch_size = 32
    num_epochs = 15
    learning_rate = 0.001
    model_name = 'simple'  # or 'resnet'
    num_classes = 5  # Update based on your dataset

    # Check for GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # Analyze dataset
    print("Analyzing dataset...")
    analyze_dataset_stats(data_dir)

    # Create data loaders
    print("Creating data loaders...")
    train_loader, val_loader = create_data_loaders(
        data_dir, batch_size=batch_size, train_ratio=0.8
    )

    print(f'Training samples: {len(train_loader.dataset)}')
    print(f'Validation samples: {len(val_loader.dataset)}')

    # Visualize a batch of data
    print("Visualizing sample batch...")
    visualize_batch(train_loader, num_samples=8)

    # Create model
    print(f"Creating {model_name} model with {num_classes} classes...")
    model = get_model(model_name, num_classes)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Train model
    model, train_losses, train_accuracies, val_losses, val_accuracies = train_model(
        model, train_loader, val_loader, num_epochs, learning_rate, device
    )

    # Plot training history
    plot_training_history(train_losses, train_accuracies, val_losses, val_accuracies)

    # Evaluate on validation set
    print("Evaluating model on validation set...")
    val_acc = evaluate_model(model, val_loader, device)

    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"./models/best_model_{timestamp}.pth"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    torch.save({
        'model_state_dict': model.state_dict(),
        'train_losses': train_losses,
        'train_accuracies': train_accuracies,
        'val_losses': val_losses,
        'val_accuracies': val_accuracies,
        'val_accuracy': val_acc,
        'timestamp': timestamp
    }, model_path)

    print(f"Model saved to {model_path}")
    print("Training completed!")

if __name__ == "__main__":
    main()
```

### Exercise 4: Test the Complete Pipeline

Now you'll test the complete pipeline from data generation to model training.

#### Step 1: Create a Complete Pipeline Script

Create `~/isaac_ai_training_ws/ai_training_lab/pipeline_test.py`:

```python
#!/usr/bin/env python3
"""
Complete pipeline test: Data generation -> Training -> Evaluation
"""

import os
import sys
import torch
import numpy as np

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_exporter import SyntheticDataExporter
from dataset import create_data_loaders
from models.simple_classifier import get_model
from train_classifier import train_model, evaluate_model

def run_complete_pipeline():
    """Run the complete AI training pipeline"""
    print("Starting complete AI training pipeline...")

    # Step 1: Generate synthetic data
    print("\n1. Generating synthetic dataset...")
    data_dir = "./synthetic_classification_data"
    exporter = SyntheticDataExporter(data_dir)

    # Generate a small classification dataset for testing
    class_names = ['cube_red', 'cube_blue', 'sphere_red', 'sphere_blue', 'robot']

    # Generate sample images
    images = []
    labels = []

    for i in range(150):  # Generate 150 samples
        # Create synthetic image with colored shapes
        height, width = 224, 224
        img = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)  # Dark background

        # Choose a random class
        class_idx = i % len(class_names)

        # Add object based on class
        if 'cube' in class_names[class_idx]:
            x, y, w, h = 50, 50, 124, 124
            color = [255, 0, 0] if 'red' in class_names[class_idx] else [0, 0, 255]
            import cv2
            cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
        elif 'sphere' in class_names[class_idx]:
            center = (112, 112)
            radius = 80
            color = [255, 0, 0] if 'red' in class_names[class_idx] else [0, 0, 255]
            import cv2
            cv2.circle(img, center, radius, color, -1)
        elif 'robot' in class_names[class_idx]:
            import cv2
            cv2.rectangle(img, (80, 80), (144, 144), [100, 100, 100], -1)  # Body
            cv2.circle(img, (100, 70), 20, [200, 200, 200], -1)  # Head

        images.append(img)
        labels.append(class_idx)

    # Export the classification dataset
    exporter.export_classification_dataset(images, labels, class_names)
    exporter.create_metadata_file()

    print(f"Generated {len(images)} synthetic images")

    # Step 2: Create data loaders
    print("\n2. Creating data loaders...")
    train_loader, val_loader = create_data_loaders(data_dir, batch_size=16, train_ratio=0.8)

    print(f"Training samples: {len(train_loader.dataset)}")
    print(f"Validation samples: {len(val_loader.dataset)}")

    # Step 3: Create and train model
    print("\n3. Training model...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Create model
    model = get_model('simple', num_classes=len(class_names))
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Train model
    model, train_losses, train_accuracies, val_losses, val_accuracies = train_model(
        model, train_loader, val_loader, num_epochs=5, learning_rate=0.001, device=device
    )

    # Step 4: Evaluate model
    print("\n4. Evaluating model...")
    val_acc = evaluate_model(model, val_loader, device)

    # Step 5: Test inference on new data
    print("\n5. Testing inference...")
    model.eval()

    # Create a new test image
    test_img = np.random.randint(0, 50, (224, 224, 3), dtype=np.uint8)  # Dark background
    import cv2
    cv2.rectangle(test_img, (50, 50), (174, 174), [255, 0, 0], -1)  # Red cube

    # Preprocess for model
    from torchvision import transforms
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

    test_tensor = transform(test_img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(test_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_class].item()

    print(f"Predicted class: {predicted_class} ({class_names[predicted_class]})")
    print(f"Confidence: {confidence:.4f}")

    print(f"\nPipeline completed successfully!")
    print(f"Final validation accuracy: {val_acc:.2f}%")

if __name__ == "__main__":
    run_complete_pipeline()
```

#### Step 2: Run the Complete Pipeline

Run the complete pipeline test:

```bash
cd ~/isaac_ai_training_ws
python3 ai_training_lab/pipeline_test.py
```

### Exercise 5: Validate Model Performance

Now you'll create validation scripts to evaluate the trained model.

#### Step 1: Create Model Validation Script

Create `~/isaac_ai_training_ws/ai_training_lab/validate_model.py`:

```python
#!/usr/bin/env python3
"""
Model validation script
"""

import torch
import os
import json
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def load_trained_model(model_path, num_classes=5):
    """Load a trained model from checkpoint"""
    from models.simple_classifier import get_model

    checkpoint = torch.load(model_path, map_location='cpu')

    model = get_model('simple', num_classes)
    model.load_state_dict(checkpoint['model_state_dict'])

    return model, checkpoint

def validate_on_real_data(model, real_data_path, device='cpu'):
    """Validate model on real data if available"""
    # This would typically load real-world images and test the model
    # For this lab, we'll simulate with synthetic test data

    print("Validating on synthetic test data...")

    # Generate some synthetic test data
    from dataset import IsaacSimClassificationDataset, get_transforms
    import cv2

    # Create a simple test dataset
    test_images = []
    test_labels = []

    class_names = ['cube_red', 'cube_blue', 'sphere_red', 'sphere_blue', 'robot']

    for i in range(50):  # 50 test samples
        # Create synthetic test image
        height, width = 224, 224
        img = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)  # Dark background

        class_idx = i % len(class_names)

        if 'cube' in class_names[class_idx]:
            cv2.rectangle(img, (50, 50), (174, 174), [255, 0, 0], -1)  # Red cube
        elif 'sphere' in class_names[class_idx]:
            cv2.circle(img, (112, 112), 80, [0, 0, 255], -1)  # Blue sphere
        elif 'robot' in class_names[class_idx]:
            cv2.rectangle(img, (80, 80), (144, 144), [100, 100, 100], -1)  # Gray robot

        test_images.append(img)
        test_labels.append(class_idx)

    # Convert to tensors and evaluate
    from torchvision import transforms
    transform = get_transforms(train=False)

    model.eval()
    correct = 0
    total = 0
    all_predictions = []
    all_targets = []

    with torch.no_grad():
        for img, target in zip(test_images, test_labels):
            # Apply transforms
            img_pil = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
            img_tensor = transform(torch.from_numpy(img).permute(2, 0, 1).float() / 255.0).unsqueeze(0)

            # Predict
            output = model(img_tensor.to(device))
            _, predicted = torch.max(output, 1)

            total += 1
            correct += (predicted.item() == target)
            all_predictions.append(predicted.item())
            all_targets.append(target)

    accuracy = 100 * correct / total
    print(f"Test accuracy: {accuracy:.2f}%")

    # Generate classification report
    print("\nClassification Report:")
    print(classification_report(all_targets, all_predictions,
                              target_names=class_names))

    # Plot confusion matrix
    cm = confusion_matrix(all_targets, all_predictions)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

    return accuracy

def analyze_model_performance(model_path, num_classes=5):
    """Analyze the performance of a trained model"""
    print(f"Analyzing model: {model_path}")

    # Load model
    model, checkpoint = load_trained_model(model_path, num_classes)
    print(f"Model loaded from checkpoint")
    print(f"Training completed at: {checkpoint.get('timestamp', 'Unknown')}")
    print(f"Final validation accuracy: {checkpoint.get('val_accuracy', 0):.2f}%")

    # Plot training history
    if 'train_losses' in checkpoint and 'val_losses' in checkpoint:
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

        # Loss plot
        ax1.plot(checkpoint['train_losses'], label='Train Loss')
        ax1.plot(checkpoint['val_losses'], label='Validation Loss')
        ax1.set_title('Training History - Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()

        # Accuracy plot
        ax2.plot(checkpoint['train_accuracies'], label='Train Accuracy')
        ax2.plot(checkpoint['val_accuracies'], label='Validation Accuracy')
        ax2.set_title('Training History - Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.legend()

        plt.tight_layout()
        plt.show()

    # Validate on test data
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    accuracy = validate_on_real_data(model, "./test_data", device)

    return accuracy

def main():
    """Main validation function"""
    # Look for saved models
    model_dir = "./models"
    if os.path.exists(model_dir):
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.pth')]

        if model_files:
            latest_model = sorted(model_files)[-1]  # Get most recent model
            model_path = os.path.join(model_dir, latest_model)

            print(f"Found model: {latest_model}")
            accuracy = analyze_model_performance(model_path)
            print(f"Model validation completed with accuracy: {accuracy:.2f}%")
        else:
            print("No saved models found. Run training first.")
    else:
        print("No models directory found. Run training first.")

if __name__ == "__main__":
    main()
```

## Verification Checks

Complete the following verification steps to ensure you've successfully completed the lab:

### Verification 1: Data Export
- [ ] Synthetic data exporter script runs without errors
- [ ] Sample synthetic dataset is generated with proper structure
- [ ] Images, labels, and annotations are saved correctly
- [ ] Metadata file contains dataset statistics

### Verification 2: PyTorch Data Loaders
- [ ] Custom dataset classes load synthetic data correctly
- [ ] Data loaders create proper batches with correct dimensions
- [ ] Transforms are applied correctly to images
- [ ] Dataset splitting works properly (train/validation)

### Verification 3: Model Training
- [ ] Simple classifier model is created successfully
- [ ] Training script runs without errors
- [ ] Model shows decreasing loss during training
- [ ] Training and validation accuracy improve over epochs

### Verification 4: Model Validation
- [ ] Trained model is saved with proper checkpoint format
- [ ] Model can be loaded from checkpoint
- [ ] Validation script runs and shows model performance
- [ ] Confusion matrix and classification report are generated

### Verification 5: Complete Pipeline
- [ ] Complete pipeline script runs end-to-end
- [ ] Final model achieves reasonable accuracy (>60% for random data)
- [ ] Model can make predictions on new synthetic images
- [ ] All components integrate correctly

## Expected Results

After completing this lab, you should have:

1. Created a synthetic data exporter that can generate and save Isaac Sim data
2. Implemented PyTorch data loaders for synthetic classification datasets
3. Trained a simple vision classifier on synthetic data
4. Validated the model performance with proper metrics
5. Demonstrated the complete pipeline from data generation to model deployment

## Troubleshooting

### Common Issues

**PyTorch import errors:**
- Ensure PyTorch is properly installed: `pip3 install torch torchvision torchaudio`
- Check CUDA compatibility if using GPU

**Memory issues during training:**
- Reduce batch size in the training script
- Use CPU instead of GPU if memory is limited
- Reduce model complexity for testing

**Data loading errors:**
- Verify dataset directory structure matches expected format
- Check that all required files (images, annotations) exist
- Ensure file paths in annotations are correct

**Poor model performance:**
- Check that transforms are applied consistently during training and inference
- Verify class balance in the dataset
- Try different learning rates or model architectures

## Summary

This lab provided hands-on experience with the complete AI training pipeline using Isaac Sim synthetic data. You learned how to export synthetic datasets, create efficient PyTorch data loaders, train vision classifiers, and validate model performance. This workflow is essential for developing robust AI models that can leverage the scalability and control of synthetic data generation.

## Next Steps

With the completion of Module 3 and the entire digital twin and simulation curriculum, you now have comprehensive knowledge of:
- Gazebo simulation and robotics
- Unity visualization and ROS integration
- Isaac Sim GPU-accelerated simulation
- Perception pipeline development
- AI training with synthetic data

This foundation prepares you for advanced robotics development, computer vision applications, and AI research in physical AI and humanoid robotics.