import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary).
  Should set num_frames and basename if the frames
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    isFrame = 0
    name = ''
    num_frames = 1
    shade_type = ""

    for command in commands:
        # print command
        cmd = command['op']
        args = command['args']

        if cmd == "frames":
            num_frames = int(command["args"][0])
            isFrame = 1
        elif cmd == "basename":
            name = command["args"][0]
        elif cmd == "shading":
            # print "hi"
            shade_type = command["shade_type"]
            # print shade_type


    if not isFrame:
        print("Vary is found but frames is not so the entire program is exiting...")
        exit(0)
    if isFrame and not len(name):
        name  = "base"
        print("Frame is found but basename is not, the basename is now base...")
    # print shade_type
    return [name, num_frames, shade_type]

"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    #print num_frames
    frames = [ {} for i in range(num_frames) ]
    for command in commands:
        if command["op"] == 'vary':
            args = command["args"]
            knob = command["knob"]
            start_frame = args[0]
            end_frame = args[1]
            start_value = float(args[2])
            end_value = float(args[3])
            increment = (end_value - start_value) / (end_frame - start_frame)
            for i in range(num_frames):
                if i >= start_frame and i <= end_frame:
                    frames[i][knob] = start_value + increment * (i - start_frame)
    # print frames
    return frames


def run(filename):
    bob = 0
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    lights = []
    # lights = [[0.5,
    # 0.75,
    # 1],
    # [255,
    # 255,
    # 255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 1, 0.5],
                        'green': [0.2, 1, 0.5],
                          'blue': [0.2, 1, 0.5]}]
    reflect = '.white'

    [name, num_frames, shade_type] = first_pass(commands)
    knobs = second_pass(commands, num_frames)


    for i in range(int(num_frames)):
        print ("Pic " + str(i+1) + " out of " + str(int(num_frames)) + " ==> " + str(int((i+1)/float(num_frames)*100)) + "% complete!")
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20
        consts = ''
        coords = []
        coords1 = []

        for knob in knobs[i]:
            symbols[knob][1] = knobs[i][knob]

        for command in commands:
            # print command
            c = command['op']
            args = command['args']
            knob_value = 1

            if c == 'light':
                # print symbols
                s = symbols[command['light']]
                # print s
                sample_color = s[1]['color'][:]
                sample_location = s[1]['location'][:]
                if command['knob']:


                    if len(command['knob']) == 2:
                        knob1_value = symbols[command["knob"][1]][1]
                        knob2_value = symbols[command["knob"][0]][1]
                        # save a copy of old info..

                        #this is in the case where they only give 2 knobs
                        if command["knob"][1][:5] == "color":
                            s[1]['color'][0] = min(s[1]['color'][0] * knob1_value, 255)
                            s[1]['color'][1] = min(s[1]['color'][1] * knob1_value, 255)
                            s[1]['color'][2] = min(s[1]['color'][2] * knob1_value, 255)
                        if command["knob"][0][:8] == "location":
                            s[1]['location'][0] = min(s[1]['location'][0] * knob2_value, 1)
                            s[1]['location'][1] = min(s[1]['location'][1] * knob2_value, 1)
                            s[1]['location'][2] = min(s[1]['location'][2] * knob2_value, 1)


                    elif len(command['knob']) == 6:


                        knob1_value = symbols[command["knob"][0]][1]
                        knob2_value = symbols[command["knob"][1]][1]
                        knob3_value = symbols[command["knob"][2]][1]
                        knob4_value = symbols[command["knob"][3]][1]
                        knob5_value = symbols[command["knob"][4]][1]
                        knob6_value = symbols[command["knob"][5]][1]
                        # this is in the case where they give 6 knobs

                        # print "this should print"
                        # print knob1_value, knob4_value

                        if command["knob"][0][:4] == "xcor":
                            s[1]['location'][0] = min(s[1]['location'][0] * knob1_value, 255)

                        if command["knob"][1][:4] == "ycor":
                            s[1]['location'][1] = min(s[1]['location'][1] * knob2_value, 255)
                        if command["knob"][2][:4] == "zcor":
                            s[1]['location'][2] = min(s[1]['location'][2] * knob3_value, 255)

                        if command["knob"][3][:3] == "red":
                            s[1]['color'][0] = min(s[1]['color'][0] * knob4_value, 255)

                        if command["knob"][4][:5] == "green":
                            s[1]['color'][1] = min(s[1]['color'][1] * knob5_value, 255)
                        if command["knob"][5][:4] == "blue":
                            s[1]['color'][2] = min(s[1]['color'][2] * knob6_value, 255)
                # print s[1]

                to_remove = []
                for j in range(len(lights)):
                    sym = lights[0][2]
                    if sym == command['light']:
                        to_remove.append(j)
                # print to_remove

                offset = 0
                for thing in to_remove:
                    lights.pop(thing - offset)
                    offset += 1

                # print "after clearing the stuff"
                # print lights
                #COMMENTED THIS OUT
                lights.append([s[1]['location'], s[1]['color'], command['light']])
                # print "after appending the lights"
                # print lights
                s[1]['color'] = sample_color
                s[1]['location'] = sample_location

                # print "these are the lights"
                # print lights

            if c == 'mesh':
                # this is some object file
                if command['constants'] and command['constants'] != ":":
                    reflect = command['constants']

                add_mesh(tmp, args[0])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, shade_type, view, ambient, lights, symbols, reflect)
                tmp = []
                reflect = '.white'

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, shade_type, view, ambient, lights, symbols, reflect)
                tmp = []
                reflect = '.white'

            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, shade_type, view, ambient, lights, symbols, reflect)
                tmp = []
                reflect = '.white'

            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, shade_type, view, ambient, lights, symbols, reflect)
                tmp = []
                reflect = '.white'

            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []

            elif c == 'move':
                if command["knob"]:
                    knob_value = symbols[command["knob"]][1]
                tmp = make_translate(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []

            elif c == 'scale':
                if command["knob"]:
                    knob_value = symbols[command["knob"]][1]
                tmp = make_scale(args[0] * knob_value, args[1]* knob_value, args[2]* knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []

            elif c == 'rotate':
                if command["knob"]:
                    knob_value = symbols[command["knob"]][1]
                theta = args[1] * (math.pi/180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []

            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )

            elif c == 'pop':
                stack.pop()

            elif c == 'display':
                display(screen)

            elif c == 'save':
                save_extension(screen, args[0])

        save_extension(screen,'anim/' + name + ('%03d' %int(i)))

    make_animation(name)
