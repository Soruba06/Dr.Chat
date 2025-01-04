# main.py
from predict_image import predict_image

def main():
    print("AI First Aid System")
    print("====================")
    img_path = input("Enter the path to the image: ")

    try:
        # Predict the situation
        label, steps = predict_image(img_path)
        print(f"\nPredicted Situation: {label}")
        print("First Aid Steps:")
        for step in steps['steps']:
            print(f"- {step}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
