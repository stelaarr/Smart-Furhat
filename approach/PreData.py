import torch
import cv2
from approach.ResEmoteNet import ResEmoteNet
from torchvision import transforms

def REN_get_item():
    face_tracker = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    labels = ['happy','surprise','sad','angry','disgust','fear','neutral']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using {device} device")
    model = ResEmoteNet()
    model.load_state_dict(torch.load('.//checkpoints//ResEmoteNetBS32.pth', weights_only=True))
    model.to(device)
    model.eval()
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    return labels,device, model, transform, face_tracker
