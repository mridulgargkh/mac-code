import speech_recognition as sr
import openai
import os

openai.api_key = "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"



def listen():
    print("listening")
    r = sr.Recognizer()

    with sr.Microphone() as mic:

        r.adjust_for_ambient_noise(mic,duration=0.2)
        r.pause_threshold = 0.5
        audio = r.listen(mic)
    try:
        audio = r.recognize_google(audio,language="en-in")
        print(audio)
        return audio.lower()
    except Exception as e:
        return "None"

def GetReply(question,log = None):
    if(log == None):
        mf = open("log.txt","r")
        # mf = open("log.txt","r")
        log = mf.read()
        mf.close()
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f'{log}You:{question}\n mark :  ',
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    # chat_log=None,
    frequency_penalty=0,
    presence_penalty=0.6,
)   
    answer = response["choices"][0]["text"]
    print("Mark:",str(answer).strip())
    os.system(f"say {answer.strip()}")
    # text = str(answer).strip()
    # t(str(answer.strip()))
    with open("log.txt","w") as f:
        f.write(log + f'\nYou:{question}\nMark:{answer}')

    
if __name__ == "__main__":
    while True:
        # audio = listen()
        audio = input("Enter:")

        if "generate an image of" in audio:
                sp = audio.split('generate an image of')
                os.system(f"say generating a image of {sp}")
                response = openai.Image.create(
                prompt=sp[1],
                n=1,
                size="1024x1024"
                )
                image_url = response['data'][0]['url']
                print(image_url)

        elif 'read pdf' in audio:
                import PyPDF2
                doc = open("py.pdf","rb")
                reader = PyPDF2.PdfReader(doc)
                pages = len(reader.pages)
                page = reader.pages[0]
                text = page.extract_text()
                os.system(f"say {text}")
                print(text)

        elif 'open camera' in audio:
                import cv2
                os.system("say opening camera")
                vid = cv2.VideoCapture(0)

                while(True):
                    ret, frame = vid.read()
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                vid.release()
                cv2.destroyAllWindows()

        else:
            

            GetReply(audio)
