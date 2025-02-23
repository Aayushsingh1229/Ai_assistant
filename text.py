try:
    from NetHyTech_Pyttsx3_Speak import speak
    speak("Testing speech synthesis", 0)
except ImportError:
    print("Module 'NetHyTech_Pyttsx3_Speak' not found. Check if it is installed and accessible.")
except AttributeError:
    print("The 'speak' function is not found in 'NetHyTech_Pyttsx3_Speak'. Check the module contents.")
except Exception as e:
    print(f"An error occurred: {e}")
