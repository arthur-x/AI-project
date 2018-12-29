# -*- coding: utf-8 -*-
from angle import angle


def format_data(data_frame):
    data_list = data_frame.split(',')
    data_dict = dict()
    for data in data_list:
        data = data.split('=')
        try:
            data_dict[data[0]] = float(data[1])
        except ValueError:
            if len(data[1]) == 0:
                data_dict[data[0]] = None
            else:
                pass
    return data_dict


def receiver(rece):

    data, addr = rece.recvfrom(2048)
    data = data.decode('utf-8')
    data_dict = format_data(data)
    return data_dict


def pid(state, target_latitude=37.7, target_longitude=-122.4, target_altitude=5000):
    """control_state with var_separator ,
    %f, %f, %f, %f, %f
    aileron, elevator, rudder, throttle0, throttle1
    """

    aileron = state['aileron']
    elevator = state['elevator']
    rudder = state['rudder']
    throttle0 = state['throttle0']
    throttle1 = state['throttle1']

    fly_mode = float(state["altitude"]) < target_altitude - 2000

    target_heading = angle(state['longitude'], state['latitude'], target_longitude, target_latitude)
    heading_error = state['heading-deg'] - target_heading
    if heading_error > 180:
        heading_error -= 360
    if heading_error < -180:
        heading_error += 360

    if fly_mode:  # 如果处于起飞模式
        if abs(float(state['speed-down-fps'])) < 1 and float(state['airspeed-kt']) < 120:  # 如果在跑道上并且跑的还没到起飞速度
            if float(state['speed-north-fps']) < -0.0005:
                if float(state['north-accel-fps_sec']) < 0.0001:
                    rudder -= 0.001
            elif float(state['speed-north-fps'] > 0.0005):
                if float(state['north-accel-fps_sec']) > -0.0001:
                    rudder += 0.001
            if throttle0 < 0.6:
                throttle0 += 0.01
                throttle1 += 0.01

        else:  # 如果不在跑道上
            if float(state['speed-north-fps']) < -0.005:
                if float(state['north-accel-fps_sec']) < 0.01:
                    rudder -= 0.005
            elif float(state['speed-north-fps']) > 0.005:
                if float(state['north-accel-fps_sec']) > -0.01:
                    rudder += 0.005

        if float(state['speed-down-fps']) < -0.1 or float(state['airspeed-kt']) > 121:  # 起飞之后基本都能落到这里
            if throttle0 < 0.6:  # 速度控制
                throttle0 += 0.01
                throttle1 += 0.01
            if elevator > -0.1:  # 升降控制
                elevator -= 0.001  # 如果上升速率比较慢，加大加快上升的速率
            elif -0.1 >= elevator > -0.2:  # 如果上升速率比较快，减慢加快上升的速率
                elevator -= 0.0001
            if float(state['roll-deg']) != 0:  # 翻滚控制
                aileron = -0.1 * float(state['roll-deg'])

    else:  # normal fly mode
        print("high level")
        if float(state["roll-deg"]) != 0:
            aileron = -0.1 * float(state['roll-deg'])
        elevator = (float(state["altitude"]) - target_altitude + 666) * 0.00015
        rudder = 0
        throttle0 = 0.6
        throttle1 = 0.6

    control = str(aileron)+","+str(elevator)+","+str(rudder)+","+str(throttle0)+","+str(throttle1)+"\n"  # type: str
    print(control)
    return control
