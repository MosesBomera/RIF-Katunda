% Crop and resize images under new file names in a different directory 
% Cosmas 2/10/2020
% Bomera 2/29/2020

clear variables;
clc;

sourceFolder = '..\sourcefolder';
storeFolder='..\storefolder';	           % Parent folder

% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isfolder(sourceFolder)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', sourceFolder);
  uiwait(warndlg(errorMessage));
  return;
end

cd(sourceFolder);
%addpath(storefolder);

imageSizes = [512 400 256]
folderPaths = []

for size = imageSizes
    folderName  = sprintf('Cropped_%dx%d', size)   
    folderPath = strcat(storeFolder, folderName)   % Full path name
    % status = mkdir(folderName)
    mkdir ../storefolder folderName                % Create each size folder.
    addpath(folderPath)
    folderPaths = [folderPaths folderPath]         % Store all created folder paths
end

% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(sourceFolder, '*.jpg');                               % Change to whatever pattern you need.
theFiles = dir(filePattern);

for k = 1: length(theFiles)
   baseFileName = theFiles(k).name;
   image = imread(baseFileName); 
   croppedImage=imcrop(image);                         			     % Use cross hairs to select region to crop, then double click
   % Delete or rename original image
   % Check both storefolder and sourcefolder file names
   % if file_name is in storefolder, skip
   for i = 1: length(imageSizes)
       resizedImage = imresize(croppedImage, [imageSizes(i) imageSizes(i)]); % Cropped region is resized to this
       fullFileName = fullfile(folderPaths(i), baseFileName); 		     % Keep original file name
       imwrite(resized_image,fullFileName);                                  % Full path name?
   end
    
end 

