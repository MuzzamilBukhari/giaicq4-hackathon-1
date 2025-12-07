import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import numpy as np
import cv2
import os
from PIL import Image

class SimpleCNN(nn.Module):
    """Simple CNN for image classification"""

    def __init__(self, num_classes=5):
        super(SimpleCNN, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
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

class SyntheticDataset(Dataset):
    """Dataset class for synthetic Isaac Sim data"""

    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform

        # In a real implementation, this would discover actual files
        # For this example, we'll generate synthetic samples
        self.samples = []

        # Generate some example samples
        for i in range(100):  # 100 synthetic samples
            # Each sample is a tuple of (image_path, label)
            # In real implementation, these would be actual file paths
            self.samples.append((f"sample_{i:06d}.png", i % 5))  # 5 classes

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        # In a real implementation, this would load actual images
        # For this example, we'll generate synthetic images

        # Generate a synthetic image based on the class
        _, label = self.samples[idx]

        # Create a simple synthetic image with colored shapes
        img = np.random.randint(0, 50, (224, 224, 3), dtype=np.uint8)  # Dark background

        # Add a shape based on the class
        if label == 0:  # Red cube
            cv2.rectangle(img, (50, 50), (174, 174), [255, 0, 0], -1)
        elif label == 1:  # Green circle
            cv2.circle(img, (112, 112), 80, [0, 255, 0], -1)
        elif label == 2:  # Blue triangle
            pts = np.array([[112, 30], [30, 194], [194, 194]], np.int32)
            cv2.fillPoly(img, [pts], [0, 0, 255])
        elif label == 3:  # Yellow diamond
            pts = np.array([[112, 30], [30, 112], [112, 194], [194, 112]], np.int32)
            cv2.fillPoly(img, [pts], [255, 255, 0])
        elif label == 4:  # Cyan pentagon
            pts = np.array([[112, 30], [40, 70], [60, 170], [164, 170], [184, 70]], np.int32)
            cv2.fillPoly(img, [pts], [0, 255, 255])

        # Convert to PIL Image
        img = Image.fromarray(img)

        if self.transform:
            img = self.transform(img)

        return img, label

def get_data_loaders(batch_size=32):
    """Get training and validation data loaders"""

    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

    # Create dataset
    dataset = SyntheticDataset(data_dir="./synthetic_data", transform=transform)

    # Split into train and validation
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    return train_loader, val_loader

def train_model():
    """Train the classification model"""

    # Check for GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Get data loaders
    train_loader, val_loader = get_data_loaders(batch_size=16)

    # Create model
    model = SimpleCNN(num_classes=5).to(device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    num_epochs = 10
    model.train()

    for epoch in range(num_epochs):
        running_loss = 0.0
        correct = 0
        total = 0

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
            total += targets.size(0)
            correct += (predicted == targets).sum().item()

            if batch_idx % 10 == 0:
                print(f'Epoch {epoch+1}/{num_epochs}, Batch {batch_idx}, Loss: {loss.item():.4f}')

        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total
        print(f'Epoch {epoch+1}/{num_epochs} completed - Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.2f}%')

    print("Training completed!")

    # Save model
    torch.save(model.state_dict(), "simple_classifier.pth")
    print("Model saved as simple_classifier.pth")

def main():
    """Main function to run the training"""
    print("Starting Isaac Sim synthetic data classifier training...")
    train_model()

if __name__ == "__main__":
    main()