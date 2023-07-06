clear all;
close all;
fclose all;

obs_file = 'Z:\\Greenbelt\\RAS2D\\Observation\\Observed_data.csv';
model_file1 = 'Z:\\Greenbelt\\RAS2D\\Observation\\Modeled_results_DW.csv';
model_file2 = 'Z:\\Greenbelt\\RAS2D\\Observation\\Modeled_results_SWE.csv';
obs_station_file = 'Z:\\Greenbelt\\RAS2D\\Observation\\Observed_data_StationID.txt';
model_station_file = 'Z:\\Greenbelt\\RAS2D\\Observation\\Modeled_results_StationID.txt';

obs_table = readtable(obs_file, 'PreserveVariableNames', true);
model_table1 = readtable(model_file1, 'PreserveVariableNames', true);
model_table2 = readtable(model_file2, 'PreserveVariableNames', true);
obs_station = importdata(obs_station_file);
model_station = importdata(model_station_file);

for i = 1:size(obs_station,1)
    for j = 1:size(model_station,1)
        if strcmpi(obs_station{i},model_station{j})
            model_date1 = table2array(model_table1(:,1));
            model_value1 = table2array(model_table1(:,j+1));
            model_date2 = table2array(model_table2(:,1));
            model_value2 = table2array(model_table2(:,j+1));
            obs_date = table2array(obs_table(:,(i-1)*2+1));
            obs_value = table2array(obs_table(:,i*2));

            plot(model_date1,model_value1,model_date2,model_value2,obs_date,obs_value)
            xlim([datetime('05/16/2021','InputFormat','MM/dd/uuuu') datetime('06/01/2021','InputFormat','MM/dd/uuuu')])
            obs_station{i} = strrep(obs_station{i}, '@', 'at');
            obs_station{i} = strrep(obs_station{i}, '_', ' ');
            title(obs_station{i})
            h = gca; % Get handle to current axes.
            xLabelPosition = get(h, 'XLabel'); % Get the current position of the label.
            set(xLabelPosition, 'Units', 'Normalized', 'Position', [0.5, -0.1, 0.5]); % Set new position.
            text(0.5, -0.1, 'Date', 'Units', 'Normalized', 'HorizontalAlignment', 'Center');

            ylabel('Water Surface Elevation (ft)') % Sets the y-axis label
            legend('Modeled DW','Modeled SWE','Observed')
            FigureName = sprintf('Z:\\Greenbelt\\RAS2D\\Observation\\%s.png',obs_station{i});
            FigureName = strrep(FigureName, '@', 'at');
            FigureName = strrep(FigureName, '_', ' ');
            saveas(gcf,FigureName)
        end
    end
end
