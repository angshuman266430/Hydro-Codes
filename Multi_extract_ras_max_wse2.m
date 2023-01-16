% Remove the "clear all" command
close all;
fclose all;

inputFiles = 'Extraction_RAS_GagesOnly.csv';

% coordination of the extraction location
input = sprintf('Z:\\Dr. Shubhra\\Amite_TZ_uncertainty\\PeakRAS_WSE_Extract\\%s',inputFiles);
coor = readtable(input); 
StationID = table2array(coor(:,1));
x_model = table2array(coor(:,2));
y_model = table2array(coor(:,3));
lon = table2array(coor(:,4));
lat = table2array(coor(:,5));
Number_Station = length(lon);

[filenames,PathName] = uigetfile({'*.hdf*'},'Select Time Series Files','MultiSelect', 'on');

% Initialize "tsi" as NaN with 2 columns instead of 1
tsi = NaN(length(StationID), length(filenames));

for fileIndex = 1:length(filenames)
    filename = filenames{fileIndex};
    filename = sprintf('%s\\%s',PathName,filename);

    % load in flow area names
    FA_Att = h5read(filename,'/Geometry/2D Flow Areas/Attributes'); 
    FA_Name = transpose(FA_Att.Name);
    for i = 1:size(FA_Name,1)
        FlowAreas(i,1) = deblank(convertCharsToStrings(FA_Name(i,:))); 
    end

    % find the nearest grid cell and save the water surface elevation 
    for i = 1:Number_Station

        x_modeli = x_model(i);
        y_modeli = y_model(i);

        best = 1;
        bestDist = 9999;

        for k = 1:length(FlowAreas)
            temp = ['/Geometry/2D Flow Areas/',convertStringsToChars(FlowAreas(k)),'/Cells Center Coordinate'];

            cellctrs = h5read(filename,temp);

            for j =1:size(cellctrs,2)
                dist = ((x_modeli-cellctrs(1,j))^2 + (y_modeli-cellctrs(2,j))^2 )^0.5;
                if dist < bestDist
                    best = j;
                    bestDist = dist;
                    FA_found = FlowAreas(k);
                end
            end        
        end

        % Change the "if" statement at line 54 to check if "bestDist" is not equal to 9999 instead
        if bestDist~=9999
            bestCell(i,:) = {i, x_modeli, y_modeli, bestDist, best, FA_found,fileIndex};

            valuePath1 = ['/Results/Unsteady/Output/Output Blocks/Base Output/Summary Output/2D Flow Areas/',convertStringsToChars(FA_found),'/Maximum Water Surface'];
            value = h5read(filename,valuePath1);
            % Use "fileIndex" to index the second column of "

         tsi(i, fileIndex) = value(best,1);  % WSEL(ft),Time(days)
    end
end

end
