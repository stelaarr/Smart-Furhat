# Angry
def Perform_AngryExpression():
    furhat.gesture(body={
    "frames": [
    {
        "time": [1.0,2,2.2],    #A list of times can be provided, at those times the params will be executed.
        "persist": True,
        "params": {
            "BROW_In_LEFT":1.0,
            "BROW_In_RIGHT":1.0,
            "EXPR_ANGER": 1.0,
            "NECK_TILT": 5
        }
    },
    {
        "time": [5.0],
        "persist": False,
        "params": {"reset": True}
    }],
    "class": "furhatos.gestures.Gesture"
    })

# Disgust
def Perform_DisgustExpression():
    furhat.gesture(body={
    "frames":[
    {
      "time":[1.0,2.0],
      "persist":True,
      "params":{
        "BROW_IN_LEFT":1,
        "BROW_IN_RIGHT":1,
        "NECK_ROLL":8.0,
        "EXPR_DISGUST":1
        }
    },
    {
      "time":[5.0],
      "persist":False,
      "params":{
        "reset":True
        }
    }],
    "class": "furhatos.gestures.Gesture"
    })

# Fear
def Perform_FearExpression():
    furhat.gesture(body={
    "frames":[
    {
      "time":[1.0,1,5,1.5,2.0],
      "persist":True,
      "params":{
        "BROW_IN_LEFT":1,
        "BROW_IN_RIGHT":1,
        "LOOK_DOWN":0.35,
        "EXPR_FEAR":1.0,
        "NECK_PAN":15
        }
    },
    {
      "time":[5.0],
      "persist":False,
      "params":{
        "reset":True
        }
    }],
    "class": "furhatos.gestures.Gesture"
    })

# Happy
def Perform_HappyExpression():
    furhat.gesture(body={
    "frames":[
    {
      "time":[1.0,1.5],
      "persist":False,
      "params":{
        "BROW_UP_LEFT":1,
        "BROW_UP_RIGHT":1,
        "SMILE_OPEN":0.8,
        }
    },
    {
      "time":[5.0],
      "persist":False,
      "params":{
        "reset":True
        }
    }],
    "class": "furhatos.gestures.Gesture"
    })

# Neutral
def Perform_NeutralExpression():
    furhat.gesture(body={
    "frames":[
    {
      "time":[1.0],
      "persist":False,
      "params":{
        "PHONE_B_M_P": 1.0,
        }
    },
    {
      "time":[5.0],
      "persist":False,
      "params":{
        "reset":True
        }
    }],
    "class": "furhatos.gestures.Gesture"
    })

# Sad
def Perform_SadExpression():
    furhat.gesture(body={
    "frames":[
    {
      "time":[1.0,2.0,3.0,3.25,3.25],
      "persist":False,
      "params":{
        "SMILE_CLOSED":1.0,
        "EXPR_SAD": 1.0,
        "BROW_DOWN_LEFT":0.8,
        "BROW_DOWN_RIGHT":0.8,
        "LOOK_DOWN":0.2,
        "NECK_TILT":10
        }
    },
    {
      "time":[5.0],
      "persist":False,
      "params":{
        "reset":True
        }
    }],
    "class": "furhatos.gestures.Gesture"
    })

# Surprise
def Perform_SurprisedExpression():
    furhat.gesture(body={
    "frames":[
    {
      "time":[1.0,1.5,1.5],
      "persist":True,
      "params":{
        "SURPRISE": 1.0,
        "BROW_UP_LEFT":1.0,
        "BROW_UP_RIGHT":1.0,
        "NECK_TILT":-8
        }
    },
    {
      "time":[5.0],
      "persist":False,
      "params":{
        "reset":True
        }
    }],
    "class": "furhatos.gestures.Gesture"
    })
