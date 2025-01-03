## Smart Furhat

With a Furhat robot system, we can create a more human-like interaction, offering customers an emotional connection that leaves them feeling heard, valued, and supported.

## Checkpoints Installation Tutorial

Due to the large size of the trained model, it has been uploaded to Hugging Face instead of GitHub.

### Download

Download the model from the following link:
[ResEmoteNetBS32.pth](https://huggingface.co/neilchouGTX/ResEmoteNet_Four_datasets_BatchSize32/blob/main/ResEmoteNetBS32.pth)

### Create a Folder

Create a folder named `checkpoints` in the project directory and place `ResEmoteNetBS32.pth` inside it to ensure the system runs properly.

The directory structure should look like this:

```
SMART-FURHAT
├── approach
│   ├── PreData.py
│   ├── ResEmoteNet.py
├── checkpoints
│   ├── ResEmoteNetBS32.pth
├── README.md
├── user_subsystem.py
```

### Run the File

Use the python environment from the previous assignment and execute `user_subsystem.py`:

```sh
python user_subsystem.py
```
