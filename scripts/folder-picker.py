import modules.scripts as scripts
import gradio as gr
import os
import logging

from modules import script_callbacks

root_path = "c:\\ai"
root_path = os.path.abspath(root_path)

def add_picker_dropdown(component, **kwargs):
    if "elem_id" in kwargs.keys() and kwargs["elem_id"] == "extras_batch_input_dir":
        ddindir = gr.Dropdown(choices = [root_path], label = "Input directory - append subfolder")
        ddindir.select(fn = ddindir_select, inputs = [component, ddindir], outputs = component)
        component.change(fn = extras_batch_input_dir_change, inputs = component, outputs = ddindir)
    if "elem_id" in kwargs.keys() and kwargs["elem_id"] == "extras_batch_output_dir":
        ddoutdir = gr.Dropdown(choices = [root_path], label = "Onput directory - append subfolder")
        ddoutdir.select(fn = ddoutdir_select, inputs = [component, ddoutdir], outputs = component)
        component.change(fn = extras_batch_output_dir_change, inputs = component, outputs = ddoutdir)
    

def extras_batch_input_dir_change(base_path):
    if os.path.isdir(base_path) and base_path.find(root_path) == 0:
        folders = [ folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder)) ]
        folders = [".", ".."] + folders
        return gr.update(value = folders[0], choices = folders)
    else:
        return gr.update(value = "", choices = [root_path])
    
def ddoutdir_select(base_path, folder):
    if folder == "." or folder == "..":
        new_base_path  = os.path.abspath(os.path.join(base_path, folder))
        if new_base_path.find(root_path) == 0:
            return new_base_path
        else:
            return root_path
    else:
        return os.path.join(base_path, folder)
        
def extras_batch_output_dir_change(base_path):
    if os.path.isdir(base_path) and base_path.find(root_path) == 0:
        folders = [ folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder)) ]
        folders = [".", ".."] + folders
        return gr.update(value = folders[0], choices = folders)
    else:
        return gr.update(value = "", choices = [root_path])
    
def ddindir_select(base_path, folder):
    if folder == "." or folder == "..":
        new_base_path  = os.path.abspath(os.path.join(base_path, folder))
        if new_base_path.find(root_path) == 0:
            return new_base_path
        else:
            return root_path
    else:
        return os.path.join(base_path, folder)

script_callbacks.on_after_component(add_picker_dropdown)
