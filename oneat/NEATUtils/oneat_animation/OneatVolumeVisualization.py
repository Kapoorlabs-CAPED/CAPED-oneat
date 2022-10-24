from poplib import POP3_SSL_PORT
import pandas as pd
import numpy as np
import os
from napari import Viewer, layers
from scipy import spatial
from skimage import measure
from dask.array.image import imread as daskread
from tifffile import imread
from skimage import morphology
class OneatVolumeVisualization:

    def __init__(self, 
                 viewer: Viewer,
                 key_categories: dict, 
                 csvdir: str,
                 savedir: str, 
                 savename: str, 
                 ax, 
                 figure):

        self.viewer = viewer
        self.csvdir = csvdir
        self.savedir = savedir
        self.savename = savename
        self.key_categories = key_categories
        self.ax = ax
        self.figure = figure
        self.dataset = None
        self.event_name = None
        self.cell_count = None      
        self.image = None
        self.seg_image = None
        self.event_locations = []
        self.event_locations_dict = {}
        self.event_locations_size_dict = {}
        self.size_locations = []
        self.score_locations = []
        self.confidence_locations = []
        self.event_locations_clean = [] 
        self.cleantimelist = []
        self.cleaneventlist= []
        self.cleannormeventlist = []
        self.cleancelllist = []
        self.labelsize = {}
        self.segimagedir  = None
        self.plot_event_name = None 
        self.event_count_plot = None
        self.event_norm_count_plot = None 
        self.cell_count_plot = None
        self.imagename = None
        self.originalimage = None
        
   
                
               

    def show_plot(self,  plot_event_name, event_count_plot, 
      segimagedir = None, event_threshold = 0 ):

        timelist = []
        eventlist= []
        normeventlist = []
        celllist = []
        self.ax.cla()
        
        self.segimagedir = segimagedir
        self.plot_event_name = plot_event_name
        self.event_count_plot = event_count_plot 
        
        if self.dataset is not None:                             
               
                for layer in list(self.viewer.layers):
                    if isinstance(layer, layers.Image):
                            self.image = layer.data
                    if isinstance(layer, layers.Labels):
                            self.seg_image = layer.data    


                if self.image is not None:    
                        currentT   = np.round(self.dataset["T"]).astype('int')
                        currentsize = self.dataset["Score"]
                            
                        for i in range(0, self.image.shape[0]):
                            
                            condition = currentT == i
                            condition_indices = self.dataset_index[condition]
                            conditionScore = currentsize[condition_indices]
                            score_condition = conditionScore > event_threshold
                            countT = len(conditionScore[score_condition])
                            timelist.append(i)
                            eventlist.append(countT)
                           
                        self.cleannormeventlist = []    
                        
                              
                        if self.plot_event_name == self.event_count_plot:    
                                self.ax.plot(timelist, eventlist, '-r')
                                self.ax.plot(self.cleantimelist, self.cleaneventlist, '-g')
                                self.ax.set_title(self.event_name + "Events")
                                self.ax.set_xlabel("Time")
                                self.ax.set_ylabel("Counts")
                                self.figure.canvas.draw()
                                self.figure.canvas.flush_events()
                                
                                self.figure.savefig(self.savedir  + self.event_name + self.event_count_plot + (os.path.splitext(os.path.basename(self.imagename))[0]  + '.png'), dpi = 300)

                       
                       

    def show_image(self, 
                image_toread, 
                imagename, 
                segimagedir = None, 
                heatmapimagedir = None, 
                heatname = '_Heat', 
                use_dask = False):
        self.imagename = imagename
        name_remove = ('Image', 'SegImage')
        for layer in list(self.viewer.layers):
                                         if  any(name in layer.name for name in name_remove):
                                                    self.viewer.layers.remove(layer)
        try:                                            
            if use_dask:                                      
                self.image = daskread(image_toread)[0]
            else:
                self.image = imread(image_toread)    
            
            if heatmapimagedir is not None:
                    try:
                        if use_dask: 
                            heat_image = daskread(heatmapimagedir + imagename + heatname + '.tif')[0]
                        else:
                            heat_image = imread(heatmapimagedir + imagename + heatname + '.tif')
                    except:
                        heat_image = None   
            
            if  segimagedir is not None:
                    if use_dask:
                        self.seg_image = daskread(segimagedir + imagename + '.tif')[0]
                    else:
                        self.seg_image = imread(segimagedir + imagename + '.tif')    

                      
                    
                    self.viewer.add_labels(self.seg_image.astype('uint16'), name = 'SegImage'+ imagename)
                   
                    
                        
            self.originalimage = self.image
            self.viewer.add_image(self.image, name= 'Image' + imagename )
            if heatmapimagedir is not None:
                    try:
                      self.viewer.add_image(heat_image, name= 'Image' + imagename + heatname, blending= 'additive', colormap='inferno' )
                    except:
                        pass   

        except:
             pass            

    def show_csv(self, imagename, csv_event_name, segimagedir = None, event_threshold = 0, use_dask = False, heatmapsteps = 0, nms_space = 0):
        
        csvname = None
        self.event_locations_size_dict.clear()
        self.size_locations = []
        self.score_locations = []
        self.event_locations = []
        self.confidence_locations = []
        
        for layer in list(self.viewer.layers):
                    if 'Detections'  in layer.name or layer.name in 'Detections' :
                            self.viewer.layers.remove(layer)   
        for (event_name,event_label) in self.key_categories.items():
                    if event_label > 0 and csv_event_name == event_name:
                            self.event_label = event_label     
                            csvname = self.csvdir + "/" + event_name + "Location" + (os.path.splitext(os.path.basename(imagename))[0] + '.csv')
        if csvname is not None:    
            
                self.event_name = csv_event_name                         
                self.dataset   = pd.read_csv(csvname, delimiter = ',')
                for index, row in self.dataset.iterrows():
                    tcenter = int(row[0])
                    zcenter = row[1]
                    ycenter = row[2]
                    xcenter = row[3]
                    score = row[4]
                    size = row[5]
                    confidence = row[6]
                
                self.dataset_index =  self.dataset.index
                if score > event_threshold:
                                self.event_locations.append([int(tcenter),int(zcenter), int(ycenter), int(xcenter)])   

                                if int(tcenter) in self.event_locations_dict.keys():
                                    current_list = self.event_locations_dict[int(tcenter)]
                                    current_list.append([int(zcenter),int(ycenter), int(xcenter)])
                                    self.event_locations_dict[int(tcenter)] = current_list 
                                    self.event_locations_size_dict[(int(tcenter), int(zcenter), int(ycenter), int(xcenter))] = [size, score]
                                else:
                                    current_list = []
                                    current_list.append([int(zcenter),int(ycenter), int(xcenter)])
                                    self.event_locations_dict[int(tcenter)] = current_list    
                                    self.event_locations_size_dict[int(tcenter),int(zcenter), int(ycenter), int(xcenter)] = [size, score]

                                self.size_locations.append(size)
                                self.score_locations.append(score)
                                self.confidence_locations.append(confidence)
                point_properties = {'score' : np.array(self.score_locations), 'confidence' : np.array(self.confidence_locations),
                'size' : np.array(self.size_locations)}    
             
                name_remove = ('Detections','Location Map')
                for layer in list(self.viewer.layers):
                                    
                                    if  any(name in layer.name for name in name_remove):
                                            self.viewer.layers.remove(layer) 
                if len(self.score_locations) > 0:                             
                        self.viewer.add_points(self.event_locations,  properties = point_properties, symbol = 'square', blending = 'translucent_no_depth', name = 'Detections' + event_name, face_color = [0]*4, edge_color = "red") 
                        
                if segimagedir is not None:
                        for layer in list(self.viewer.layers):
                            if isinstance(layer, layers.Labels):
                                    self.seg_image = layer.data

                                    location_image, self.cell_count = LocationMap(self.event_locations_dict, self.seg_image, use_dask, heatmapsteps)     
                                    self.viewer.add_labels(location_image.astype('uint16'), name= 'Location Map' + imagename )
                                     

                                       
def LocationMap(event_locations_dict, seg_image, heatmapsteps):
       cell_count = {} 
       location_image = np.zeros(seg_image.shape)
       j = 0
       for i in range(seg_image.shape[0]):
            current_seg_image = seg_image[i,:]
            waterproperties = measure.regionprops(current_seg_image)
            indices = [prop.centroid for prop in waterproperties]
            cell_count[int(i)] = len(indices)        

            if int(i) in event_locations_dict.keys():
                currentindices = event_locations_dict[int(i)]
                    
                
                if len(indices) > 0:
                    tree = spatial.cKDTree(indices)
                    if len(currentindices) > 0:
                        for j in range(0, len(currentindices)):
                            index = currentindices[j] 
                            closest_marker_index = tree.query(index)
                            current_seg_label = current_seg_image[int(indices[closest_marker_index[1]][0]), int(
                            indices[closest_marker_index[1]][1]),int(
                            indices[closest_marker_index[1]][2]) ]
                            if current_seg_label > 0:
                                all_pixels = np.where(current_seg_image == current_seg_label)
                                all_pixels = np.asarray(all_pixels)
                                for k in range(all_pixels.shape[1]):
                                    location_image[i,all_pixels[0,k], all_pixels[1,k], all_pixels[2,k]] = 1
            
       location_image = average_heat_map(location_image, heatmapsteps)


       return location_image, cell_count


def average_heat_map(image, sliding_window):

    j = 0
    for i in range(image.shape[0]):
        
              j = j + 1
              if i > 0:
                image[i,:] = np.add(image[i,:] , image[i - 1,:])
              if j == sliding_window:
                  image[i,:] = np.subtract(image[i,:] , image[i - 1,:])
                  j = 0
    return image          

                    
                    
           
                                
 
def TimedDistance(pointA, pointB):

    
     spacedistance = float(np.sqrt( (pointA[1] - pointB[1] ) * (pointA[1] - pointB[1] ) + (pointA[2] - pointB[2] ) * (pointA[2] - pointB[2] )  ))
     
     timedistance = float(np.abs(pointA[0] - pointB[0]))
     
     
     return spacedistance, timedistance
                
                
def GetMarkers(image):
    
    
    MarkerImage = np.zeros(image.shape)
    waterproperties = measure.regionprops(image)                
    Coordinates = [prop.centroid for prop in waterproperties]
    Coordinates = sorted(Coordinates , key=lambda k: [k[0], k[1]])
    coordinates_int = np.round(Coordinates).astype(int)
    MarkerImage[tuple(coordinates_int.T)] = 1 + np.arange(len(Coordinates))

    markers = morphology.dilation(MarkerImage, morphology.disk(2))        
   
    return markers  