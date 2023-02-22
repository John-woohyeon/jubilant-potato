import modi
import time

if __name__ == '__main__':
    bundle = modi.MODI(
           conn_type = 'ble',
           network_uuid = 'EB0C3D47'
        )
    display = bundle.displays[0]
    dial = bundle.dials[0]
    button = bundle.buttons[0]
    gyro = bundle.gyros[0]
    motor_xy = bundle.motors.get(3235)
    motor_z = bundle.motors.get(2344)
    count = 0
    
state = False
a = 0
end1 = 0

while True:
    motor_z.second_degree = 50 # 초기 z축 값 설정
    if dial.degree < 5: # MODE 0 - 짐벌 모드
        display.text_noclear = '''6.Initial\n\n0.Gimbal 1.H-V'''
        motor_z.second_degree = 50
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                    a = 0
                                    count = 0
                                    break
                            display.text_noclear = '''\n Mode 0\n\n Gimbal\n\n1:Y 2:N '''
                            if button.toggled != state:
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time() 
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5:
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2 :
                                while True:
                                    display.text_noclear = '''\n Mode 0\n\n Gimbal\n\nRunning '''
                                    # 모드 실행 시 Running이 디스플레이에 뜨며 실행
                                    cur_roll = gyro.roll
                                    cur_pitch = gyro.pitch
                                    trans_roll = int((cur_roll + 180)*10/36)
                                    trans_pitch = int((cur_pitch + 180)*10/36)
                                    error_roll = 50 - trans_roll
                                    error_pitch = 50 - trans_pitch

                                    cur = [cur_roll, cur_pitch]
                                    trans = [trans_roll, trans_pitch]
                                    error = [error_roll, error_pitch]

                                    #####################################################
                                    Kp = 1
                                    Ki = 1.05
                                    dt = 0.95
                                    #####################################################

                                    roll_P_temp = error[0]*Kp
                                    roll_I_temp = error[0]*Ki*dt
                                    control_roll = (roll_P_temp + roll_I_temp)/2
                                    target_roll = 50 + int(control_roll) # 기준 값 50

                                    pitch_P_temp = error[1]*Kp
                                    pitch_I_temp = error[1]*Ki*dt
                                    control_pitch = (pitch_P_temp + pitch_I_temp)/2
                                    target_pitch = 100 - int(control_pitch) # 기준 값 100
                                    
                                    target = [target_roll, target_pitch]
                                    if target[1] >= 100:
                                        target[1] = 100 # pitch 축 100 이상에 대한 값 100으로 리턴
                                    print("#################################################")
                                    print("current roll : ", trans[0])
                                    print("target roll : ", target[0])
                                    print("#################################################")
                                    print("current pitch : ", trans[1])
                                    print("target pitch : ", target[1])
                                    print("#################################################")
                                    motor_xy.degree = target[0], target[1]
                                    time.sleep(0.1)
                                    error_roll = 50 - trans_roll
                                    error_pitch = 50 - trans_pitch
                                    if a == 1:
                                        break
                                    if button.toggled != state:
                                            state = button.toggled
                                            start2 = time.time()
                    ################## 모드 바깥으로 나가는 부분 #####################
                                            while True:
                                                if button.toggled != state:
                                                    state = button.toggled
                                                    end2 = time.time() 
                                                    print('end')
                                                    if end2 - start2 < 0.5:
                                                        a = 1
                                                        count = 0
                                                        break    
                                                    else:
                                                        start2 = end2
                                                        break
                    #################################################################
    elif dial.degree < 17: # MODE 1 - 가로 / 세로 모드
        display.text_noclear = '''0.Gimbal\n\n1.H-V\n\n2.Selfie'''
        motor_z.second_degree = 50
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                a = 0
                                count = 0
                                break
                            display.text_noclear = '''\n Mode 1\n Hori-Vert\n1:Y 2:N '''    
                            if button.toggled != state:
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time()
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5:
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2:
                                while True:
                                    display.text_noclear = '''\n Mode 1\n Hori-Vert\nRunning'''
                                    motor_xy.degree = 50,73
                                    if a == 1:
                                           break
                                    if button.toggled != state: 
                                        state = button.toggled
                                        start2 = time.time() 

                                        while True:
                                            if button.toggled != state:
                                                state = button.toggled
                                                end2 = time.time() 
                                                print('end')
                                                if end2 - start2 < 0.5:
                                                    a = 1
                                                    count = 0
                                                    break
                                                else:
                                                    start2 = end2
                                                    break
    elif dial.degree < 33: # MODE 2 - 셀카모드 
        display.text_noclear = '''1.H-V\n\n\n\n2.Selfie  3.Tripod '''
        motor_z.second_degree = 50
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                    a = 0
                                    count = 0
                                    break
                            display.text_noclear = '''\n Mode 2\n\n Selfie\n\n1:Y 2:N '''
                            if button.toggled != state:
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time() 
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5:
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2:
                                b = 0
                                while True:
                                    display.text_noclear = '''\n Mode 2\n\n Selfie\n\nRunning'''
                                    s_start = time.time()
                                    motor_xy.first_speed = 0
                                    while b == 0:
                                        motor_xy.first_speed = 30
                                        s_end = time.time()
                                        if button.toggled != state:
                                            state = button.toggled
                                            motor_xy.first_speed = 0
                                            b = 1
                                        if s_end- s_start > 4:
                                            b = b + 1
                                            break
                                    if a == 1:
                                           break
                                    if button.toggled != state:
                                        state = button.toggled
                                        start2 = time.time()

                                        while True:
                                            if button.toggled != state:
                                                state = button.toggled
                                                end2 = time.time() 
                                                print('end')
                                                if end2 - start2 < 0.5:
                                                    a = 1
                                                    count = 0
                                                    break
                                                else:
                                                    start2 = end2
                                                    break
    elif dial.degree < 47: # MODE 3 - 삼각대 고정 모드 
        display.text_noclear = '''2.Selfie\n\n3.Tripod  4.panornS '''
        motor_z.second_degree = 50
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                    a = 0
                                    count = 0
                                    break
                            display.text_noclear = '''\n Mode 3\n\n Tripod\n\n1:Y 2:N '''
                            if button.toggled != state:
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time() 
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5 :
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2:
                                while True:
                                    display.text_noclear = '''\n Mode 3\n\n Tripod\n\nRunning '''
                                    motor_z.second_degree = 50
                                    if a == 1:
                                           break
                                    if button.toggled != state:
                                        state = button.toggled
                                        start2 = time.time()

                                        while True:
                                            if button.toggled != state:
                                                state = button.toggled
                                                end2 = time.time() 
                                                print('end')
                                                if end2 - start2 < 0.5:
                                                    a = 1
                                                    count = 0
                                                    break
                                                else:
                                                    start2 = end2
                                                    break
    elif dial.degree < 58: # MODE 4 - 파노라마 모드
        display.text_noclear = '''3.Tripod\n\n4.panorn5.S.Ctrl '''
        motor_z.second_degree = 50
        panorama_set = 0
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                    a = 0
                                    count = 0
                                    break
                            display.text_noclear = '''\n Mode 4\n Panorama\n1:Y 2:N '''
                            if button.toggled != state:
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time() 
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5:
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2:
                                while True:
                                    display.text_noclear = '''\n Mode 4\n Panorama\nRunning'''
                                    while panorama_set == 0:
                                        motor_z.second_degree = 15
                                        time.sleep(2)
                                        panorama_set = panorama_set + 1
                                        while panorama_set == 1:
                                            print("Panorama Initial Point Setted")
                                            motor_z.second_degree = 85
                                            time.sleep(5)
                                            panorama_set = panorama_set + 1
                                            break
                                    if a == 1:
                                           break
                                    if button.toggled != state:
                                        state = button.toggled
                                        start2= time.time()

                                        while True:
                                            if button.toggled != state:
                                                state = button.toggled
                                                end2 = time.time() 
                                                print('end')
                                                if end2 - start2 < 0.5:
                                                    a = 1
                                                    count = 0
                                                    break
                                                else:
                                                    start2 = end2
                                                    break
    elif dial.degree < 70: # MODE 5 - 수동 컨트롤 모드 , 다이얼로 원하는 만큼의 모터 제어
        display.text_noclear = '''4.Tripod\n\n5.S.Ctrl  6.B.Ctrl '''
        motor_z.second_degree = 50
        motor_count = 0
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                    a = 0
                                    count = 0
                                    break
                            display.text_noclear = '''\n Mode 5 \nSelf ctrl\n1:Y 2:N'''                            
                            if button.toggled != state:
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time() 
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5:
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2:
                                while True:
                                    display.text_noclear = '''\n Mode 5 \nSelf ctrl\nRunning'''
                                    
                                    # 각 축 제어, 0회 -> YAW 축, 1회 -> PITCH축, 2회 -> ROLL축, 3회 이상 -> mode out
                                    while motor_count <= 3:
                                        if button.toggled != state:
                                            state = button.toggled
                                            motor_count = motor_count + 1
                                        if motor_count == 0:
                                            motor_z.second_degree = dial.degree
                                            print("motor 0 00000000000000000000000000")
                                            time.sleep(1)
                                        elif motor_count == 1:
                                            motor_xy.second_degree = dial.degree
                                            print("Motor 1 11111111111111111111111111")
                                            time.sleep(1)
                                        elif motor_count == 2:
                                            motor_xy.first_degree = dial.degree
                                            print("Motor 2 222222222222222222222222222")
                                            time.sleep(1)
                                        else:
                                            break
                                    #################################################################################
                                    if a == 1:
                                           break
                                    if button.toggled != state:
                                        state = button.toggled
                                        start2 = time.time()

                                        while True:
                                            if button.toggled != state:
                                                state = button.toggled
                                                end2 = time.time() 
                                                print('end')
                                                if end2 - start2 < 0.5:
                                                    a = 1
                                                    count = 0
                                                    break
                                                else:
                                                    start2 = end2
                                                    break
    elif dial.degree <= 100: # MODE 6 - Initial Point, 초기 값 50, 100, 50으로 회귀
        display.text_noclear = '''5.S.Ctrl\n\n\n6.Initial 0.G.B'''
        motor_z.second_degree = 50
        if button.toggled != state:
                state = button.toggled
                count += 1
                if count == 1:
                    while True:
                            if a == 1:
                                    a = 0
                                    count = 0
                                    break
                            display.text_noclear = '''\n Mode 6\n\n Initial\n\n1:Y 2:N'''
                            if button.toggled != state: 
                                state = button.toggled
                                start1 = time.time()
                                while True:
                                        if button.toggled != state:
                                            state = button.toggled
                                            end1 = time.time() 
                                            print('end')
                                            if end1 - start1 < 0.5:
                                                a = 1
                                                count = 0
                                                break
                                        elif time.time() - start1 > 0.5:
                                            start1 = end1
                                            count = 2
                                            break
                            if count == 2:
                                while True:
                                    display.text_noclear = '''\n Mode 6\n\n Initial\n\nRunning'''
                                    motor_xy.degree = 50, 100  
                                    motor_z.second_degree = 50
                                    
                                    if a == 1:
                                           break
                                    if button.toggled != state:
                                        state = button.toggled
                                        start2 = time.time()

                                        while True:
                                            if button.toggled != state:
                                                state = button.toggled
                                                end2 = time.time()
                                                print('end')
                                                if end2 - start2 < 0.5:
                                                    a = 1
                                                    count = 0
                                                    break
                                                else:
                                                    start2 = end2
                                                    break