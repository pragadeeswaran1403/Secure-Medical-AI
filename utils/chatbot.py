def get_bot_response(msg):

    msg = msg.lower()

    if "brain" in msg:
        return "Brain tumor is abnormal growth of cells in brain."

    elif "lung" in msg:
        return "Lung disease affects the respiratory system."

    elif "bone" in msg:
        return "Bone fracture means crack or break in bone."

    elif "risk" in msg:
        return "High risk patients need immediate consultation."

    elif "hello" in msg:
        return "Hello! How can I help you?"

    else:
        return "Please consult your doctor for detailed analysis."