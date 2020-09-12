import math
import speech_recognition as sr  # https://pypi.org/project/SpeechRecognition/
import project.parameters as pp
from project.structures import House


def get_cmd_id(cmd):
    lowest_ed_to_len_ratio = math.inf
    accepted_kwg = None
    for kwg in pp.all_kw_groups:
        curr_ed_to_len_ratio = kwg.ed_to_len_ratio(cmd)
        if curr_ed_to_len_ratio < lowest_ed_to_len_ratio:
            lowest_ed_to_len_ratio = curr_ed_to_len_ratio
            accepted_kwg = kwg
    if lowest_ed_to_len_ratio <= pp.max_ed:
        return accepted_kwg.cmd_id
    raise ValueError


def interpret(text: str, house):
    words = text.split()
    start = 0
    end = 0
    for i, word in enumerate(words):
        if word in pp.akw:
            start = i + 1
        if word in pp.ekw:
            end = i
            break
    if end == 0:
        end = -1

    cmd = words[start]
    try:
        cmd_id = get_cmd_id(cmd)
        start += 1
    except ValueError:  # first word is not a command so it must be a toggle command
        cmd_id = pp.toggle_id

    thing_to_set = None
    set_to = None
    if cmd_id == pp.set_id:
        thing_to_set = words[start]
        start += 1
        if words[end - 2] not in pp.for_kw:
            print("Invalid command")
        set_to = words[end - 1]
        end -= 2

    obj_name = " ".join(words[start:end])
    try:
        obj_id = house[obj_name].id
    except ValueError:
        print("Object not found")
        return

    return obj_id + "-" + str(cmd_id), thing_to_set, set_to


def listen_loop(house):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print()
            print("Speak")
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio, language="pl-PL").lower()
                print("AUDIO UNDERSTOOD")
                print(text)
                print("AUDIO END")

                print(interpret(text, house))
            except sr.UnknownValueError:
                print("Couldn't understand the audio")


def main():
    house = House()
    house.add_obj("światło w kuchni")
    house.add_obj("światło w łazience")
    house.add_obj("radio w kuchni")
    house.add_obj("budzik w sypialni")
    house.add_obj("światło", "B")

    text = "cześć halo tom ustaw kolor światło w kuchni na zielony proszę teraz ci powiem"
    code = interpret(text, house)
    print(code)
    listen_loop(house)


if __name__ == '__main__':
    main()
