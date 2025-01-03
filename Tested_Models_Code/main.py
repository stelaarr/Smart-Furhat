import torch
import os
from approach.ResEmoteNet import ResEmoteNet
from torchvision import transforms
from PIL import Image

# 加载模型
labels = ['happy','surprise','sad','angry','disgust','fear','neutral']
device = "cuda" if torch.cuda.is_available() else "cpu"
modelMode  = 6 # 1 for FER2013, 2 for RAFDB, 3 for AffectNet7, 4 for BestModel128, 5 for BestModel64, 6 for BestModel32
datasetMode = 5 # 1 for FER2013, 2 for RAFDB, 3 for AffectNet7, 4 for FERPLUS, 5 for ALL

model = ResEmoteNet()

match modelMode:
    case 1:
        checkpoint = torch.load('.//checkpoints//fer2013_model.pth', map_location=device, weights_only=True)
        model.load_state_dict(checkpoint['model_state_dict'])
        print("Model: FER2013")
    case 2:
        checkpoint = torch.load('.//checkpoints//rafdb_model.pth', map_location=device, weights_only=True)
        model.load_state_dict(checkpoint['model_state_dict'])
        print("Model: RAFDB")
    case 3:
        checkpoint = torch.load('.//checkpoints//affectnet7_model.pth', map_location=device, weights_only=True)
        model.load_state_dict(checkpoint['model_state_dict'])
        print("Model: AffectNet7")
    case 4:
        checkpoint = torch.load('.//checkpoints//best_modelBS128.pth', map_location=device, weights_only=True)
        model.load_state_dict(torch.load('.//checkpoints//best_modelBS128.pth', weights_only=True))
        print("Model: BestModel128")
    case 5:
        checkpoint = torch.load('.//checkpoints//best_modelBS64.pth', map_location=device, weights_only=True)
        model.load_state_dict(torch.load('.//checkpoints//best_modelBS64.pth', weights_only=True))
        print("Model: BestModel64")
    case 6:
        checkpoint = torch.load('.//checkpoints//best_modelBS32.pth', map_location=device, weights_only=True)
        model.load_state_dict(torch.load('.//checkpoints//best_modelBS32.pth', weights_only=True))
        print("Model: BestModel32")
    case _:
        print("Invalid model mode")

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


# model = ResEmoteNet()

# model.load_state_dict(checkpoint['model_state_dict'])
# model = torch.load('.//checkpoints//affectnet7_model.pth', map_location=device, weights_only=False)
# model.load_state_dict(torch.load('.//checkpoints//affectnet7_model.pth',map_location=device, weights_only=True))
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