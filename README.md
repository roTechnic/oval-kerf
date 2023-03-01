# oval-kerf
A tool to redraw SVGs to compensate for the oval shape of diode laser cutters

There is a video explaining how this works and how to measure your x and y kerf size at: https://youtu.be/0UIqhCjMC0U

To run this you will need to install Python 3

Then you will need to install certain modules, this can be done by running

pip3 install  svgpathtools numpy typer

Then just run 

oval_kerf.py --kerf-x-size X --kerf-y-size Y filename.svg

where X and Y are the sizes of your laser dot

it will output a file called filename_kerfed.svg

Usage: oval_kerf.py [OPTIONS] FILENAME


  Add an oval kerf to any paths in an SVG file.


  Outputs an SVG file (filename_kerfed.svg) with the origianl paths and new
  
  paths for inside and outside cuts. simply select which ones you want in
  
  lighturn and delete the rest!
  

Arguments:

  FILENAME  [required]
  

Options:

  --kerf-x-size FLOAT         cm - horizontal radius of ellipse (kerf). You will need to work this out for your laser cutter
                              
  --kerf-y-size FLOAT         cm - vertical radius of ellipse (kerf). You will need to work this out for your laser cutter
                              
  --delta-theta FLOAT         radians - decrease this to increase the resolution of the kerf model (default should be fine)  [default: 0.0001]
                              
  --max-segment-length FLOAT  mm - max length of line segments is offset model. Increase this if your file is too big or decrease it if you need more resolution [default: 0.001]
                              
  --help                      Show this message and exit.
