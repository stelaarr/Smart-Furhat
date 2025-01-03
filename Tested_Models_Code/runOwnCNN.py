from approach.ownCNN import EmotionCNN
import os
import torch
from PIL import Image
from torchvision import transforms

labels = ['happy', 'surprise', 'sad', 'angry', 'disgust', 'fear', 'neutral']
datasetMode = 4 # 1 for FER2013, 2 for RAFDB, 3 for AffectNet7, 4 for FERPLUS, 5 for ALL


# Load the trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device} device")
model = EmotionCNN()
model.load_state_dict(torch.load('.//checkpoints//ownBS32.pth', weights_only=True))
model.to(device)
model.eval()

# Define the transformation
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((48, 48)),
    transforms.ToTensor()
])

match datasetMode:
    case 1:
        imgPath =  ".//datasets//FER2013test//"
        print("TestData: FER2013")
    case 2:
        imgPath =  ".//datasets//RAFDBtest//"
        print("TestData: RAFDB")
    case 3:
        imgPath =  ".//datasets//AffectNet7test//"
        print("TestData: AffectNet7")
    case 4:
        imgPath =  ".//datasets//FERPLUStest//"
        print("TestData: FERPLUS")
    case 5:
        imgPath =  ".//datasets//ALLtest//"
        print("TestData: ALL")
    case _:
        print("Invalid dataset mode")


AllCorrect = 0
AllTotal = 0
for root, dirs, files in os.walk(imgPath):
    for dir in dirs:
        print(f'Now Testing: {dir} ')
        correct = 0
        total = 0
        for file in os.listdir(imgPath + dir + "//"):
            filename = os.fsdecode(file)
            image_path = filename
            image = Image.open(imgPath + dir + "//" + filename)
            image = transform(image).unsqueeze(0).to(device)
            with torch.no_grad():
                output = model(image)
                _, predicted = torch.max(output, 1)
            predicted_label = labels[predicted.item()]
            # print(imgPath + dir + "//" + filename)
            # print(f'Predicted label: {predicted_label}')


            true_label = dir
            # print(f'True label: {true_label}')
            if true_label == predicted_label:
                correct += 1
                AllCorrect += 1
            total += 1
            AllTotal += 1
            accuracy = correct / total if total > 0 else 0
        print(f'{true_label} Accuracy: {accuracy * 100:.2f}%')

AllAccuracy = AllCorrect / AllTotal if AllTotal > 0 else 0
print(f'All Accuracy: {AllAccuracy * 100:.2f}%')