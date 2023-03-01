from svgpathtools import svg2paths2, wsvg, Line, Path, wsvg
import math
import numpy as np
import typer

gradients = {'al':{}, 'ar':{}, 'bl':{}, 'br':{}}

def get_vector_direction(vector):
    y_dir = 'a' if vector.imag>0 else 'b'
    x_dir = 'r' if vector.real>=0 else 'l'
    return y_dir+x_dir

def vector(x,y):
    return x+1j*y

def get_quadrant(x,y):
    y_dir = 'a' if y>0 else 'b'
    x_dir = 'r' if x>0 else 'l'
    return y_dir+x_dir

def offset_curve(path, max_len,direction):
    nls = []
    for seg in path:
        # ignore tiny segments that are smaller than 1/1000th of our max_len
        if seg.start==seg.end or seg.length()<float(max_len)/1000:
            continue
        steps = int(seg.length()/max_len)+1
        for k in range(steps):
            # t is how far along this segment we are
            t = k / steps
            next_t = (k+1) / steps
            
            t_point = seg.point(t)
            next_t_point = seg.point(next_t)
            
            # work out gradient
            delta_x=next_t_point.real - t_point.real
            delta_y=next_t_point.imag - t_point.imag
            gradient = delta_x/delta_y if delta_y!=0 else 1000
  
            #work out direction we should offset in
            normal_direction=get_vector_direction(direction*seg.normal(t))
            
            (ellipse_x,ellipse_y) = gradients[normal_direction][min(gradients[normal_direction], key=lambda x:abs((abs(x)-(abs(gradient)))))]
            
            nl = Line(seg.point(t), seg.point(t) + vector(ellipse_x,ellipse_y))
            nls.append(nl)
            
    connect_the_dots = [Line(nls[k].end, nls[k+1].end) for k in range(len(nls)-1)]
    if path.iscontinuous() and path.isclosed():
        connect_the_dots.append(Line(nls[-1].end, nls[0].end))
    offset_path = Path(*connect_the_dots)
    return offset_path

def add_to_filename(filename,text):
    fn = filename.rsplit('.', 1)[0]
    return fn+text+'.svg'

def main(
            filename: str, 
            kerf_x_size: float = typer.Option(0.034, help='cm - horizontal radius of ellipse (kerf). You will need to work this out for your laser cutter'), 
            kerf_y_size: float = typer.Option(0.02, help='cm - vertical radius of ellipse (kerf). You will need to work this out for your laser cutter'), 
            delta_theta: float = typer.Option(0.0001, help='radians - decrease this to increase the resolution of the kerf model (default should be fine)'),
            max_segment_length: float = typer.Option(0.001, help='mm - max length of line segments is offset model. Increase this if your file is too big or decrease it if you need more resolution')
            ):
    """
    Add an oval kerf to any paths in an SVG file.

    Outputs an SVG file (filename_kerfed.svg) with the origianl paths and new paths for inside and outside cuts. simply select which ones you want in lighturn and delete the rest!
    """
    # Read SVG into a list of path objects and list of dictionaries of attributes 
    paths, attributes, svg_attributes = svg2paths2(filename)

    # half the kerf size to get turn diameter into radius
    kerf_x_size = kerf_x_size/2
    kerf_y_size = kerf_y_size/2

    for theta in np.arange(0,math.pi*2,0.01):
        x=kerf_x_size*math.cos(theta)
        y=kerf_y_size*math.sin(theta)
        delta_x=kerf_x_size*math.cos(theta+delta_theta)-x
        delta_y=kerf_y_size*math.sin(theta+delta_theta)-y
        gradients[get_quadrant(x,y)][delta_x/delta_y]=(x,y)

    outer_offset_paths = []
    for path in paths:
        outer_offset_paths.append(offset_curve(path, max_segment_length, 1))
        
    inner_offset_paths = []
    for path in paths:
        inner_offset_paths.append(offset_curve(path, max_segment_length, -1))
        
    # write it out
    output_file_name = add_to_filename(filename,"_kerfed")
    wsvg(paths + outer_offset_paths + inner_offset_paths,attributes=attributes*3, svg_attributes=svg_attributes, filename=output_file_name)

if __name__ == "__main__":
    typer.run(main)
    main2()
