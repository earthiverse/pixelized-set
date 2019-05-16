#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://www.ibm.com/developerworks/library/os-autogimp/

from gimpfu import *

def save_file(image, drawable, save_dir, pixel_size):
    # Save the pixelized image
    pdb.file_png_save_defaults(
        image,
        drawable,
        '{}\\{}.png'.format(save_dir, pixel_size),
        '{}\\{}.png'.format(save_dir, pixel_size))

def save_pixelized(image, drawable, save_dir, pixel_size):
    # Copy the image to a new layer
    newDrawable = pdb.gimp_layer_copy(drawable, FALSE)
    image.add_layer(newDrawable, 0)
    
    # Make the original invisible
    drawable.visible = False
    
    # Apply pixelization
    pdb.plug_in_pixelize(image, newDrawable, pixel_size)
    
    # Save the file
    save_file(image, newDrawable, save_dir, pixel_size)
    
    # Remove the new layer
    image.remove_layer(newDrawable)
    
    # Make the original visible again
    drawable.visible = True

def plugin_main(image, drawable, save_dir='C:\\temp', out_height=540, pixel_sizes='15,30,45,90,180'):
    # Crop the image
    pdb.plug_in_autocrop(image, drawable)
    
    # Resize to 540px height (1/2 of 1920x1080)
    pdb.gimp_image_scale(image, image.width/(image.height/float(out_height)), out_height)
    
    # Freeze undo (we'll end up with the same picture at this point after generating the set)
    pdb.gimp_image_undo_freeze(image)
    
    # Output pixelized images
    save_file(image, drawable, save_dir, 1)
    for pixel_size in [int(n) for n in pixel_sizes.split(',')]:
        save_pixelized(image, drawable, save_dir, pixel_size)
    
    # Thaw undo (the user can now edit the picture if they want...)
    pdb.gimp_image_undo_thaw(image)

register(
    'pixelized_set',
    'Makes a set of pixelized images',
    'Makes a set of pixelized images',
    'Kent Rasmussen',
    'Kent Rasmussen',
    '2019',
    '<Image>/Filters/Generate Pixelized Set',
    '*',
    [
        (PF_DIRNAME, 'source_directory', 'Source Directory', 'C:\\temp'),
        (PF_INT, 'out_height', 'Output Height', 540),
        (PF_STRING, 'pixelization_sizes', 'Pixel Square Sizes', '15,30,45,90,180')
    ],
    [],
    plugin_main)

main()
