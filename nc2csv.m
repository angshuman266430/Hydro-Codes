% ########################################################################################################
% #
% #    conver netcdf to csv for RAS 2D boundary 
% #    Author: Angshuman M Saharia
% #    Contact: asaharia@thewaterinsitute.org
% #
% ######################################################################################################### 
% # Shan Zou v1 written  on 09/08/2022: simple tool
% input: .nc files from ADCIRC extraction
% output: .csv for each storm 

% check how many storms with the extracted data in data folder
nc_dir=dir('*.nc');
nstorm=length(nc_dir);
nstation=1585;

if ~exist('./plots','dir')
    mkdir('./plots');
end

% read netcdf data
for istorm=1:nstorm
    fprintf('istorm=%d\n',istorm);
    theNC=[nc_dir(istorm).folder filesep nc_dir(istorm).name];       
    theMat=[theNC(1:end-3) '.mat' ];
    Created_by=strcat(theNC, datestr(now));
    
    theCSV=[theNC(1:end-3) '.csv' ];
    fid=fopen(theCSV,'w');
    fprintf(fid,'        station,');
    for i=1:nstation
        fprintf(fid,'%10d,',i);
    end
    fprintf(fid,'\n');


    if ~exist(theMat,'file')
        ncid=netcdf.open(theNC,'NOWRITE');
        [numdims, numvars, numglobalatts, unlimdimid]=netcdf.inq(ncid);
        save(theMat, 'Created_by');
        for ivar=1:numvars
            varname=netcdf.inqVar(ncid,ivar-1);
            value=netcdf.getVar(ncid,ivar-1);
            eval([varname '=value;']);
            save(theMat, varname, '-append');
        end
        netcdf.close(ncid)
    else
        load(theMat)
    end
    
    % time series plot of all stations for each storm
    for i=1:nstation
        eval(['t{i}=' 'time_station_' num2str(i,'%04d') '*1.0;']);
        eval(['wse{i}=' 'data_station_', num2str(i,'%04d') ';']);
        tdate=datenum(1970,1,1)+double(t{i})/3600/24.0;
        plot(tdate,wse{i});
%         pause
        ylim([0 5]);
        hold on;
%         str=[datestr(tdate(maxStormInd(istorm)),'mm/dd HH:MM') newline 'max=' num2str(maxStorm(istorm)*3.28083,'%5.2f'),' ft'];
%         text( tdate(maxStormInd(istorm))+1, (maxStorm(istorm)-0.1)*3.28083, str);

    end
    hold off;
    datetick('x','mm/dd','keeplimits','keepticks'); grid on;
    xlabel('date');
    ylabel('WSE (ft)');
    title(strcat('Storm: ', theNC(end-20:end-14) ),'interprete','none');
    set(gcf,'PaperUnits','inches','PaperPosition',[0 0 11 6]);
    print(gcf,'-r300','-djpeg',strcat('./plots/storm_',theNC(end-20:end-14),'_ts.jpg'));
    
    % write out .csv
    for i=1:length(tdate)
        fprintf(fid,'%s,',datestr(tdate(i),'ddmmmyyyy HH:MM'));
        for ista=1:nstation
            fprintf(fid,'%10.2f,',wse{ista}(i));
        end
        fprintf(fid,'\n');
    end
    fclose(fid);
    clear theMat theNC theCSV t wse tdate varname value
end




