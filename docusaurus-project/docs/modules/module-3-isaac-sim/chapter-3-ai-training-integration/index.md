---
title: Chapter 3 - AI Training Integration
sidebar_position: 3
description: Learn about PyTorch/TensorFlow data loaders for synthetic data, sim-to-real transfer, and reinforcement learning environments in Isaac Sim.
---

# Chapter 3: AI Training Integration

## Overview

This chapter explores how to leverage Isaac Sim for AI training workflows, including creating synthetic datasets for machine learning, implementing sim-to-real transfer techniques, and building reinforcement learning environments. You'll learn how to generate large-scale synthetic data efficiently and use it to train robust AI models.

## Learning Objectives

By the end of this chapter, you will be able to:
- Create PyTorch/TensorFlow data loaders for synthetic data from Isaac Sim
- Implement sim-to-real transfer techniques to bridge simulation and reality
- Build reinforcement learning environments using Isaac Sim physics
- Generate synthetic datasets for various AI training scenarios
- Evaluate and validate AI models trained on synthetic data

## 3.1 PyTorch/TensorFlow Data Loaders for Synthetic Data

Isaac Sim can generate vast amounts of synthetic training data that can be efficiently loaded into deep learning frameworks like PyTorch and TensorFlow.

### PyTorch Data Loading

Creating efficient data loaders for synthetic data in PyTorch:

```python
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import cv2
import os
from PIL import Image

class IsaacSimDataset(Dataset):
    """Dataset class for Isaac Sim synthetic data"""

    def __init__(self, data_dir, transform=None, task='classification'):
        """
        Args:
            data_dir (str): Directory containing synthetic data
            transform: Optional transform to be applied on images
            task (str): Type of task ('classification', 'detection', 'segmentation')
        """
        self.data_dir = data_dir
        self.transform = transform
        self.task = task

        # Load data file paths
        self.rgb_files = []
        self.annotations = []

        # Discover RGB images
        for file in os.listdir(os.path.join(data_dir, 'rgb')):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                rgb_path = os.path.join(data_dir, 'rgb', file)

                # Corresponding annotation file
                base_name = os.path.splitext(file)[0]

                if task == 'classification':
                    # Classification: single label per image
                    label_path = os.path.join(data_dir, 'labels', f"{base_name}.txt")
                    if os.path.exists(label_path):
                        with open(label_path, 'r') as f:
                            label = int(f.read().strip())
                        self.rgb_files.append(rgb_path)
                        self.annotations.append(label)

                elif task == 'detection':
                    # Object detection: bounding boxes and labels
                    annot_path = os.path.join(data_dir, 'annotations', f"{base_name}.json")
                    if os.path.exists(annot_path):
                        import json
                        with open(annot_path, 'r') as f:
                            annot_data = json.load(f)
                        self.rgb_files.append(rgb_path)
                        self.annotations.append(annot_data)

                elif task == 'segmentation':
                    # Segmentation: pixel-level labels
                    seg_path = os.path.join(data_dir, 'segmentation', f"{base_name}.png")
                    if os.path.exists(seg_path):
                        self.rgb_files.append(rgb_path)
                        self.annotations.append(seg_path)

    def __len__(self):
        return len(self.rgb_files)

    def __getitem__(self, idx):
        # Load RGB image
        img_path = self.rgb_files[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        # Load corresponding annotation based on task
        annotation = self.annotations[idx]

        if self.task == 'classification':
            label = annotation
            return image, label

        elif self.task == 'detection':
            # Return image and detection annotations
            targets = {
                'boxes': torch.tensor(annotation['boxes'], dtype=torch.float32),
                'labels': torch.tensor(annotation['labels'], dtype=torch.int64),
                'image_id': torch.tensor([idx])
            }
            return image, targets

        elif self.task == 'segmentation':
            # Load segmentation mask
            seg_mask = Image.open(annotation)
            if self.transform:
                seg_mask = self.transform(seg_mask)
            return image, seg_mask

# Example usage
from torchvision import transforms

# Define transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# Create dataset
dataset = IsaacSimDataset(
    data_dir='/path/to/synthetic/data',
    transform=transform,
    task='classification'
)

# Create data loader
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)
```

### TensorFlow Data Loading

Creating TensorFlow data pipelines for Isaac Sim synthetic data:

```python
import tensorflow as tf
import numpy as np
import json
import os

class IsaacSimDataLoader:
    """TensorFlow data loader for Isaac Sim synthetic data"""

    def __init__(self, data_dir, batch_size=32, image_size=(224, 224)):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.image_size = image_size

        # Build file lists
        self.rgb_files, self.annotation_files = self._build_file_lists()

    def _build_file_lists(self):
        """Build lists of RGB and annotation file paths"""
        rgb_files = []
        annotation_files = []

        rgb_dir = os.path.join(self.data_dir, 'rgb')

        for file in os.listdir(rgb_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                rgb_path = os.path.join(rgb_dir, file)
                base_name = os.path.splitext(file)[0]

                # Look for corresponding annotation
                annot_path = os.path.join(self.data_dir, 'annotations', f"{base_name}.json")

                if os.path.exists(annot_path):
                    rgb_files.append(rgb_path)
                    annotation_files.append(annot_path)

        return rgb_files, annotation_files

    def _parse_function(self, rgb_path, annot_path):
        """Parse function for TensorFlow dataset"""
        # Load and preprocess image
        image = tf.io.read_file(rgb_path)
        image = tf.image.decode_image(image, channels=3)
        image = tf.image.resize(image, self.image_size)
        image = tf.cast(image, tf.float32) / 255.0  # Normalize to [0, 1]

        # Load and parse annotation
        annotation = tf.io.read_file(annot_path)
        annotation = tf.py_function(
            func=self._parse_annotation,
            inp=[annotation],
            Tout=[tf.float32, tf.int32]  # bbox, label
        )

        return image, annotation[0], annotation[1]

    def _parse_annotation(self, annot_bytes):
        """Parse annotation from JSON bytes"""
        annot_str = annot_bytes.numpy().decode('utf-8')
        annot_data = json.loads(annot_str)

        # Extract bounding boxes and labels
        boxes = np.array(annot_data.get('boxes', []), dtype=np.float32)
        labels = np.array(annot_data.get('labels', []), dtype=np.int32)

        return boxes, labels

    def get_dataset(self):
        """Create TensorFlow dataset"""
        # Convert file lists to tensors
        rgb_paths = tf.constant(self.rgb_files)
        annot_paths = tf.constant(self.annotation_files)

        # Create dataset
        dataset = tf.data.Dataset.from_tensor_slices((rgb_paths, annot_paths))

        # Apply parsing function
        dataset = dataset.map(
            self._parse_function,
            num_parallel_calls=tf.data.AUTOTUNE
        )

        # Batch and prefetch
        dataset = dataset.batch(self.batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)

        return dataset

# Example usage
loader = IsaacSimDataLoader(
    data_dir='/path/to/synthetic/data',
    batch_size=32,
    image_size=(416, 416)
)

tf_dataset = loader.get_dataset()

# Iterate through dataset
for batch_images, batch_boxes, batch_labels in tf_dataset:
    print(f"Batch shape: {batch_images.shape}")
    break
```

### Optimizing Data Loading Performance

For large-scale synthetic datasets, optimization is crucial:

```python
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from multiprocessing import Pool
import pickle
import os

class OptimizedIsaacSimDataset(Dataset):
    """Optimized dataset with pre-processing and caching"""

    def __init__(self, data_dir, cache_dir=None, preload_factor=0.1):
        self.data_dir = data_dir
        self.cache_dir = cache_dir
        self.preload_factor = preload_factor

        # Load metadata
        self.metadata = self._load_metadata()

        # Preload some data into memory based on factor
        self.preloaded_data = {}
        preload_count = int(len(self.metadata) * preload_factor)

        for i in range(min(preload_count, len(self.metadata))):
            self.preloaded_data[i] = self._load_item(i)

    def _load_metadata(self):
        """Load metadata from a pre-generated file"""
        metadata_path = os.path.join(self.data_dir, 'metadata.pkl')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'rb') as f:
                return pickle.load(f)
        else:
            # Generate metadata (this would be done during data generation)
            return self._generate_metadata()

    def _generate_metadata(self):
        """Generate metadata file (run once during dataset creation)"""
        metadata = []
        rgb_dir = os.path.join(self.data_dir, 'rgb')

        for i, file in enumerate(os.listdir(rgb_dir)):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                base_name = os.path.splitext(file)[0]

                # Create metadata entry
                entry = {
                    'rgb_path': os.path.join(rgb_dir, file),
                    'depth_path': os.path.join(self.data_dir, 'depth', f"{base_name}.png"),
                    'seg_path': os.path.join(self.data_dir, 'segmentation', f"{base_name}.png"),
                    'annot_path': os.path.join(self.data_dir, 'annotations', f"{base_name}.json")
                }
                metadata.append(entry)

        # Save metadata
        metadata_path = os.path.join(self.data_dir, 'metadata.pkl')
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)

        return metadata

    def _load_item(self, idx):
        """Load a single item (used for preloading)"""
        item = self.metadata[idx]

        # Load RGB image
        import cv2
        rgb_img = cv2.imread(item['rgb_path'])
        rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)

        # Load annotations
        import json
        with open(item['annot_path'], 'r') as f:
            annotations = json.load(f)

        return {
            'rgb': rgb_img,
            'annotations': annotations
        }

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        if idx in self.preloaded_data:
            # Return preloaded data
            data = self.preloaded_data[idx]
        else:
            # Load from disk
            data = self._load_item(idx)

        # Convert to tensors
        rgb_tensor = torch.from_numpy(data['rgb']).permute(2, 0, 1).float() / 255.0
        annotations = data['annotations']

        return rgb_tensor, annotations

# Optimized data loader
def create_optimized_loader(data_dir, batch_size=64, num_workers=8):
    """Create optimized data loader"""
    dataset = OptimizedIsaacSimDataset(data_dir, preload_factor=0.2)

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=True  # Keep workers alive between epochs
    )
```

## 3.2 Sim-to-Real Transfer

Sim-to-real transfer techniques help bridge the gap between synthetic and real-world data, enabling models trained on synthetic data to work effectively in real environments.

### Domain Randomization for Transfer

Domain randomization is a key technique for improving sim-to-real transfer:

```python
import torch
import torchvision.transforms as transforms
import random
import numpy as np
import cv2

class DomainRandomizationTransform:
    """Transform class for domain randomization"""

    def __init__(self,
                 lighting_range=(0.5, 1.5),
                 color_jitter_range=(0.1, 0.2),
                 blur_range=(0, 3),
                 noise_range=(0, 0.05)):
        self.lighting_range = lighting_range
        self.color_jitter_range = color_jitter_range
        self.blur_range = blur_range
        self.noise_range = noise_range

    def __call__(self, image):
        # Convert PIL to numpy if needed
        if isinstance(image, torch.Tensor):
            image = transforms.ToPILImage()(image)

        # Convert to numpy array
        img_array = np.array(image).astype(np.float32)

        # Random lighting adjustment
        lighting_factor = random.uniform(*self.lighting_range)
        img_array = img_array * lighting_factor
        img_array = np.clip(img_array, 0, 255)

        # Random blur
        blur_kernel = int(random.uniform(*self.blur_range))
        if blur_kernel > 0:
            kernel_size = blur_kernel * 2 + 1
            img_array = cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)

        # Random noise
        noise_level = random.uniform(*self.noise_range)
        if noise_level > 0:
            noise = np.random.normal(0, noise_level * 255, img_array.shape)
            img_array = img_array + noise
            img_array = np.clip(img_array, 0, 255)

        # Convert back to PIL
        img_array = img_array.astype(np.uint8)
        return transforms.ToPILImage()(img_array)

# Example usage in training
def get_training_transforms():
    """Get transforms for training with domain randomization"""
    return transforms.Compose([
        DomainRandomizationTransform(
            lighting_range=(0.7, 1.3),
            color_jitter_range=(0.1, 0.2),
            blur_range=(0, 2),
            noise_range=(0, 0.03)
        ),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

def get_validation_transforms():
    """Get standard transforms for validation"""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
```

### Adversarial Domain Adaptation

Using adversarial techniques to improve domain transfer:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DomainAdversarialNetwork(nn.Module):
    """Network with domain adaptation capabilities"""

    def __init__(self, num_classes, base_model='resnet18'):
        super().__init__()

        # Base feature extractor
        if base_model == 'resnet18':
            from torchvision.models import resnet18
            self.feature_extractor = resnet18(pretrained=True)
            self.feature_extractor.fc = nn.Identity()  # Remove classification layer
            feature_dim = 512
        else:
            raise ValueError(f"Unsupported base model: {base_model}")

        # Task-specific classifier
        self.classifier = nn.Linear(feature_dim, num_classes)

        # Domain classifier (for adversarial training)
        self.domain_classifier = nn.Sequential(
            nn.Linear(feature_dim, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, 1),
            nn.Sigmoid()
        )

    def forward(self, x, domain_label=None):
        features = self.feature_extractor(x)

        # Task classification
        class_logits = self.classifier(features)

        # Domain classification (only during training)
        if domain_label is not None:
            domain_logits = self.domain_classifier(features)
            return class_logits, domain_logits
        else:
            return class_logits

def train_with_domain_adaptation(model, synthetic_loader, real_loader,
                               optimizer, num_epochs=10):
    """Train model with domain adaptation"""
    criterion_task = nn.CrossEntropyLoss()
    criterion_domain = nn.BCELoss()

    for epoch in range(num_epochs):
        model.train()

        # Create iterators for both domains
        synthetic_iter = iter(synthetic_loader)
        real_iter = iter(real_loader)

        for i in range(min(len(synthetic_loader), len(real_loader))):
            # Get batch from synthetic data (domain = 0)
            try:
                syn_data, syn_labels = next(synthetic_iter)
            except StopIteration:
                synthetic_iter = iter(synthetic_loader)
                syn_data, syn_labels = next(synthetic_iter)

            # Get batch from real data (domain = 1)
            try:
                real_data, real_labels = next(real_iter)
            except StopIteration:
                real_iter = iter(real_loader)
                real_data, real_labels = next(real_iter)

            # Combine batches
            combined_data = torch.cat([syn_data, real_data], dim=0)
            combined_labels = torch.cat([syn_labels, real_labels], dim=0)

            # Create domain labels (0 for synthetic, 1 for real)
            domain_labels = torch.cat([
                torch.zeros(syn_data.size(0)),  # Synthetic = 0
                torch.ones(real_data.size(0))   # Real = 1
            ]).to(combined_data.device)

            optimizer.zero_grad()

            # Forward pass
            class_logits, domain_logits = model(combined_data, domain_labels)

            # Task loss (only on labeled synthetic data)
            task_loss = criterion_task(class_logits[:syn_data.size(0)],
                                    combined_labels[:syn_data.size(0)])

            # Domain loss (try to confuse domain classifier)
            domain_loss = criterion_domain(domain_logits.squeeze(), domain_labels)

            # Total loss
            total_loss = task_loss - domain_loss  # Minimize domain loss to confuse classifier

            total_loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}/{num_epochs}, Task Loss: {task_loss.item():.4f}, "
              f"Domain Loss: {domain_loss.item():.4f}")
```

### Validation and Testing

Validating sim-to-real transfer effectiveness:

```python
def evaluate_transfer_performance(model, synthetic_test_loader, real_test_loader):
    """Evaluate model performance on both synthetic and real test sets"""

    model.eval()
    device = next(model.parameters()).device

    results = {}

    # Evaluate on synthetic test set
    syn_correct = 0
    syn_total = 0
    with torch.no_grad():
        for data, labels in synthetic_test_loader:
            data, labels = data.to(device), labels.to(device)
            outputs = model(data)
            _, predicted = torch.max(outputs.data, 1)
            syn_total += labels.size(0)
            syn_correct += (predicted == labels).sum().item()

    results['synthetic_accuracy'] = syn_correct / syn_total

    # Evaluate on real test set
    real_correct = 0
    real_total = 0
    with torch.no_grad():
        for data, labels in real_test_loader:
            data, labels = data.to(device), labels.to(device)
            outputs = model(data)
            _, predicted = torch.max(outputs.data, 1)
            real_total += labels.size(0)
            real_correct += (predicted == labels).sum().item()

    results['real_accuracy'] = real_correct / real_total
    results['transfer_gap'] = results['synthetic_accuracy'] - results['real_accuracy']

    print(f"Synthetic Accuracy: {results['synthetic_accuracy']:.4f}")
    print(f"Real Accuracy: {results['real_accuracy']:.4f}")
    print(f"Transfer Gap: {results['transfer_gap']:.4f}")

    return results
```

## 3.3 Reinforcement Learning Environments

Isaac Sim provides a powerful platform for creating reinforcement learning environments with realistic physics simulation.

### Creating RL Environments

Building custom RL environments in Isaac Sim:

```python
import gym
from gym import spaces
import numpy as np
import torch
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import get_prim_at_path
import carb

class IsaacSimRLEnvironment(gym.Env):
    """Custom RL environment using Isaac Sim physics"""

    def __init__(self,
                 scene_path="/World/RLScene",
                 robot_usd_path="path/to/robot.usd",
                 episode_length=1000):
        super().__init__()

        self.scene_path = scene_path
        self.robot_usd_path = robot_usd_path
        self.episode_length = episode_length
        self.current_step = 0

        # Initialize Isaac Sim world
        self.world = World(stage_units_in_meters=1.0)

        # Define action and observation spaces
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(6,), dtype=np.float32  # 6-DOF actions
        )

        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(24,), dtype=np.float32  # 24-dim state
        )

        # Robot properties
        self.robot = None
        self.target_position = np.array([2.0, 0.0, 2.0])

        # Setup scene
        self._setup_scene()

    def _setup_scene(self):
        """Setup the RL environment scene"""
        # Add ground plane
        self.world.scene.add_default_ground_plane()

        # Add robot
        add_reference_to_stage(
            usd_path=self.robot_usd_path,
            prim_path="/World/Robot"
        )

        # Add target object
        from omni.isaac.core.objects import VisualCuboid
        self.world.scene.add(
            VisualCuboid(
                prim_path="/World/Target",
                name="target",
                position=self.target_position,
                size=0.2,
                color=np.array([1.0, 0.0, 0.0])  # Red target
            )
        )

    def reset(self):
        """Reset the environment to initial state"""
        self.world.reset()
        self.current_step = 0

        # Get initial observation
        obs = self._get_observation()
        return obs

    def step(self, action):
        """Execute one step in the environment"""
        # Apply action to robot
        self._apply_action(action)

        # Step the simulation
        self.world.step(render=True)

        # Get next observation
        obs = self._get_observation()

        # Calculate reward
        reward = self._calculate_reward()

        # Check if episode is done
        done = self._is_episode_done()

        # Info dictionary
        info = {
            'step': self.current_step,
            'distance_to_target': np.linalg.norm(
                self._get_robot_position() - self.target_position
            )
        }

        self.current_step += 1

        return obs, reward, done, info

    def _apply_action(self, action):
        """Apply the action to the robot"""
        # In a real implementation, this would control robot joints
        # For this example, we'll simulate movement
        robot_position = self._get_robot_position()

        # Simple movement based on action
        new_position = robot_position + action[:3] * 0.01  # Scale down action
        self._set_robot_position(new_position)

    def _get_observation(self):
        """Get the current observation from the environment"""
        # Robot position and orientation
        robot_pos = self._get_robot_position()
        robot_rot = self._get_robot_orientation()

        # Target position
        target_pos = self.target_position

        # Distance to target
        dist_to_target = target_pos - robot_pos

        # Velocity (if available)
        robot_vel = self._get_robot_velocity()

        # Concatenate all observation elements
        obs = np.concatenate([
            robot_pos,           # 3D position
            robot_rot,           # 4D rotation (quaternion)
            dist_to_target,      # 3D distance to target
            robot_vel,           # 3D velocity
            np.array([self.current_step / self.episode_length])  # Normalized time
        ])

        return obs.astype(np.float32)

    def _calculate_reward(self):
        """Calculate reward based on current state"""
        robot_pos = self._get_robot_position()
        distance = np.linalg.norm(robot_pos - self.target_position)

        # Dense reward based on distance to target
        reward = -distance  # Negative distance (closer is better)

        # Bonus for reaching target
        if distance < 0.5:  # Within 0.5m of target
            reward += 100.0

        # Penalty for episode length
        reward -= 0.1  # Small time penalty

        return reward

    def _is_episode_done(self):
        """Check if the episode is done"""
        robot_pos = self._get_robot_position()
        distance = np.linalg.norm(robot_pos - self.target_position)

        # Done if reached target or max steps reached
        return (distance < 0.5) or (self.current_step >= self.episode_length)

    def _get_robot_position(self):
        """Get robot position from Isaac Sim"""
        # This would interface with Isaac Sim's robot interface
        # For this example, return a placeholder
        return np.array([0.0, 0.0, 0.0])

    def _get_robot_orientation(self):
        """Get robot orientation from Isaac Sim"""
        # Return identity quaternion as placeholder
        return np.array([0.0, 0.0, 0.0, 1.0])

    def _get_robot_velocity(self):
        """Get robot velocity from Isaac Sim"""
        return np.array([0.0, 0.0, 0.0])

    def _set_robot_position(self, position):
        """Set robot position in Isaac Sim"""
        # This would set the robot position in Isaac Sim
        pass

    def close(self):
        """Clean up the environment"""
        if self.world:
            self.world.clear()
```

### Training RL Agents

Training RL agents in Isaac Sim environments:

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQNNetwork(nn.Module):
    """Deep Q-Network for RL"""

    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, x):
        return self.network(x)

class DQNAgent:
    """DQN Agent for training in Isaac Sim environments"""

    def __init__(self, state_dim, action_dim, lr=1e-4, gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.state_dim = state_dim
        self.action_dim = action_dim

        # Neural networks
        self.q_network = DQNNetwork(state_dim, action_dim).to(self.device)
        self.target_network = DQNNetwork(state_dim, action_dim).to(self.device)

        # Copy weights to target network
        self.target_network.load_state_dict(self.q_network.state_dict())

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)

        # Hyperparameters
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay

        # Replay buffer
        self.memory = deque(maxlen=100000)
        self.batch_size = 32

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Choose action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)

        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state_tensor)
        return q_values.max(1)[1].item()

    def replay(self):
        """Train the network on a batch of experiences"""
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states = torch.FloatTensor([e[0] for e in batch]).to(self.device)
        actions = torch.LongTensor([e[1] for e in batch]).to(self.device)
        rewards = torch.FloatTensor([e[2] for e in batch]).to(self.device)
        next_states = torch.FloatTensor([e[3] for e in batch]).to(self.device)
        dones = torch.BoolTensor([e[4] for e in batch]).to(self.device)

        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_network(next_states).max(1)[0].detach()
        target_q_values = rewards + (self.gamma * next_q_values * ~dones)

        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_end:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self):
        """Update target network weights"""
        self.target_network.load_state_dict(self.q_network.state_dict())

def train_rl_agent(env, agent, episodes=1000):
    """Train RL agent in Isaac Sim environment"""
    scores = deque(maxlen=100)

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0

        done = False
        while not done:
            action = agent.act(state)
            next_state, reward, done, info = env.step(action)

            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

        agent.replay()

        scores.append(total_reward)

        # Update target network periodically
        if episode % 10 == 0:
            agent.update_target_network()

        if episode % 100 == 0:
            avg_score = np.mean(scores)
            print(f"Episode {episode}, Average Score: {avg_score:.2f}, "
                  f"Epsilon: {agent.epsilon:.3f}")

    print("Training completed!")

# Example usage
# env = IsaacSimRLEnvironment()
# agent = DQNAgent(state_dim=24, action_dim=6)
# train_rl_agent(env, agent, episodes=2000)
```

## Summary

This chapter covered the integration of Isaac Sim with AI training workflows, including creating data loaders for synthetic data, implementing sim-to-real transfer techniques, and building reinforcement learning environments. You learned how to efficiently load synthetic datasets into deep learning frameworks, apply domain randomization and adaptation techniques, and create custom RL environments with realistic physics simulation. These capabilities enable the training of robust AI models using synthetic data at scale.

## Next Steps

With the completion of Module 3, you now have a comprehensive understanding of NVIDIA Isaac Sim's capabilities for robotics simulation, perception, and AI training. This knowledge provides a solid foundation for advanced robotics development using GPU-accelerated simulation and synthetic data generation.

## External Resources

- [Isaac Sim AI Training Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorial_ml.html)
- [PyTorch Data Loading Best Practices](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html)
- [Sim-to-Real Transfer Research Papers](https://research.nvidia.com/labs/toronto-ai/Sim2Real/)
- [Reinforcement Learning in Isaac Sim](https://github.com/NVIDIA-Omniverse/IsaacGymEnvs)