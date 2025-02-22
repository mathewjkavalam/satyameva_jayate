import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import requests
import json

def load_model():
    model = models.resnet50(pretrained=True)
    model.eval()
    return model

def load_labels():
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    response = requests.get(url)
    labels = response.text.splitlines()
    return labels

def classify_animal(image_path, model, labels):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(image)
        _, predicted = outputs.max(1)
    
    return labels[predicted.item()]

if __name__ == "__main__":
    model = load_model()
    labels = load_labels()
    image_path = input("Enter the path to the image: ")
    animal_name = classify_animal(image_path, model, labels)
    print(f"The image contains: {animal_name}")
