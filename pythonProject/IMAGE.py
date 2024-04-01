import PySimpleGUI as sg

# Create the layout with a Graph element
layout = [
    [sg.Graph(canvas_size=(800, 600), graph_bottom_left=(0, 600), graph_top_right=(800, 0), background_color='white',
              key='graph')],
    [sg.Button('Button 1'), sg.Button('Button 2')]
]

# Create the window
window = sg.Window('Image Viewer', layout, finalize=True, size=(900, 700))

# Load the image
image_filename = 'cap.PNG'

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    graph = window['graph']
    if graph:
        # Clear the graph
        graph.erase()

        # Draw the image
        graph.draw_image(image_filename, location=(0, 0))

        # Draw the buttons
        button1_coords = (100, 100)
        button2_coords = (200, 100)
        graph.draw_button(button1_coords, button2_coords, text='Button 1', bind_return_key=True)
        graph.draw_button(button2_coords, (300, 100), text='Button 2', bind_return_key=True)

# Close the window
window.close()