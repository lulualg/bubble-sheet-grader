# Lulwa Alghanim
# Final Project

import cv2
import numpy as np

class gradingSystem:
    def get_marking(image):
        # image resizing
        widthImg = 700
        heightImg = 700
        img = cv2.resize(image, (widthImg, heightImg))

        # cropping image to the options part only
        img = img[123:443, 70:150]

        # applying filters for edge detection
        imgCntrs = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlure = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlure, 10, 50)

        # finding contours and drawing them
        cntrs, h = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgCntrs, cntrs, -1, (0, 255, 0), 2)

        # finding image threshold
        imgThresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)[1]

        # splitting image to 20 equal rows
        rows = np.vsplit(imgThresh, 20)

        # further splitting rows to 4 columns each
        boxes = []
        for row in rows:
            columns = np.hsplit(row, 4)
            for box in columns:
                boxes.append(box)

        # finding correct option by checking amount of white pixels
        abcd = []
        for b in boxes:
            n_white_pix = np.sum(b == 255)
            abcd.append(n_white_pix)

        # making sub-lists within a lists
        n = 4
        adjusted = [i for j in [[abcd[t:t + n] for x in abcd[:1:t + 1] if (t % n) == False] for t in range(len(abcd))]
                    for i
                    in j]

        # assigning correct index a string value
        answers = []
        for part in adjusted:
            index_max = np.argmax(part)
            if index_max == 0:
                answers.append('A')
            if index_max == 1:
                answers.append('B')
            if index_max == 2:
                answers.append('C')
            if index_max == 3:
                answers.append('D')
        return answers


def main():
    # reading Answer Key image
    Answer_Key = cv2.imread('Answer Key.png')

    # reading Student Answers Image
    Answers = cv2.imread('Student Answers.png')

    # reading Student Answers 2 Image
    Answers2 = cv2.imread('Student Answers 2.png')

    # getting answers of the Answer Key image
    Ans = gradingSystem.get_marking(Answer_Key)
    print('Answer Key : ', Ans)

    # getting answers of the Answer image
    ans = gradingSystem.get_marking(Answers)
    print('Student\'s answers : ', ans)

    # getting answers of the Answer image
    ans2 = gradingSystem.get_marking(Answers2)
    print('2nd Student\'s answers : ', ans2)

    # counting correct answers
    correct = 0
    l = len(Ans)
    for i in range(l):
        if Ans[i] == ans[i]:
            correct += 1
    print(f'Student\'s Grade : {correct}/{l}')

    correct2 = 0
    for i in range(l):
        if Ans[i] == ans2[i]:
            correct2 += 1
    print(f'2nd Student\'s Grade : {correct2}/{l}')

    # Window name in which image is displayed
    window_name = 'Image'

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (50, 250)
    org2 = (40, 90)

    # fontScale
    fontScale = 6
    scale = 2

    # Red color in BGR
    color = (0, 0, 255)

    # Line thickness
    thickness = 10
    thick = 2

    # Using cv2.putText() method to add text to png
    image = cv2.putText(Answers, f'Grade : {correct}/{l}', org, font,
                        fontScale, color, thickness, cv2.LINE_AA)

    # Saving the image
    cv2.imwrite('Checked.png', image)

    # Using cv2.putText() method to add text to png
    image2 = cv2.putText(Answers2, f'Grade : {correct2}/{l}', org2, font,
                         scale, color, thick, cv2.LINE_AA)

    # Saving the image
    cv2.imwrite('Checked2.png', image2)

if __name__ == '__main__':
    main()