% ########################################################################################################
% #
% #    conver netcdf to csv for RAS 2D boundary 
% #    Author: Shan Zou
% #    Contact: szou@thewaterinsitute.org
% #
% ######################################################################################################### 
% # Shan Zou v1 written  on 09/08/2022: simple tool
% # modified by Shan Zou on 10/24/2022: for RAS61 BC options test for median and mean WSE analysis 
% input: .nc files from ADCIRC extraction
% output: .csv for each storm 

% check how many storms with the extracted data in data folder
nc_dir=dir('*.nc');
nstorm=length(nc_dir);
nstation=169;

% read segament data
tab=readtable('AmiteDS_Coordinates.csv','Delimiter',',','ReadVariableNames',true);
stationID=tab{:,1};
long=tab{:,4};
lat=tab{:,5};
segID=tab{:,6};
segpoint=tab{:,7};

if ~exist('./plots','dir')
    mkdir('./plots');
end

% read netcdf data and data analysis
for istorm=1:nstorm
    fprintf('istorm=%d\n',istorm);
    path_theNC=[nc_dir(istorm).folder filesep nc_dir(istorm).name];  
    temp=strsplit(nc_dir(istorm).name, '_');
    theNC=[char(temp(3)) '.nc'];
    theMat=[theNC(1:end-3) '.mat' ];
    Created_by=strcat(theNC, datestr(now));
    
    theCSV=[theNC(1:end-3) '_ft.csv' ];
    fid=fopen(theCSV,'w');
    fprintf(fid,'        station,');
    for i=1:nstation
        fprintf(fid,'%10d,',i);
    end
    for iseg=1:8
        fprintf(fid,strcat(' min_',num2str(iseg),',', 'max_',num2str(iseg),',','median_',num2str(iseg),',', 'mean_',num2str(iseg),','));
    end
    for iseg=1:8
        fprintf(fid,strcat(' maxvar_',num2str(iseg),',', 'meanvar_',num2str(iseg),',','mean2median_',num2str(iseg),','));
    end
    fprintf(fid,'\n');


    if ~exist(theMat,'file')
        fprintf('%s not existing, reading %s ...',theMat, theNC);
        ncid=netcdf.open(path_theNC,'NOWRITE');
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
        fprintf('%s existing, loading ...\n', theMat);
        load(theMat)
    end
    
    
    % time series plot of all stations for each storm
    for i=1:nstation
        eval(['t{i}=' 'time_station_' num2str(i,'%04d') '*1.0;']);
        eval(['wse{i}=' 'data_station_', num2str(i,'%04d') ';']);
        tdate=datenum(1970,1,1)+double(t{i})/3600/24.0;

    end
    
    
    % data analysis for median and mean time series for 8 segments
    for iseg=1:8
        y_min=0.0;
        y_max=0.0;
        seg_station=find(segID==iseg);
        seg(iseg).tdate=tdate;
        % find the mean and median for each time step
        for itime=1:length(tdate)
            i=0;
            for ista=1:length(seg_station)
                if(wse{seg_station(ista)}(itime) > -100)
                    i=i+1;
                    y(i)=wse{seg_station(ista)}(itime);
                end
            end
            if isempty(y)
                y(1)=NaN;
            end
            seg(iseg).wse_mean(itime)=mean(y);
            seg(iseg).wse_median(itime)=median(y);
            seg(iseg).wse_min(itime)=min(y);
            seg(iseg).wse_max(itime)=max(y);
            if min(y) < y_min
                y_min=min(y);
            end
            if max(y) > y_max
                y_max=max(y);
            end
%             fprintf('size of x = %d\n',length(x));
%             x
%             seg(iseg).wse_mean(itime)
%             seg(iseg).wse_median(itime)
%             seg(iseg).wse_min(itime)
%             seg(iseg).wse_max(itime)
%             pause;
            clear y;
        end
        % find the peak surge time, peak stage, variation stats
        [seg(iseg).wse_peak seg(iseg).wse_peak_ind]=max(seg(iseg).wse_max);
        tdate_peak=seg(iseg).tdate(seg(iseg).wse_peak_ind);
        seg(iseg).maxvar=seg(iseg).wse_max(seg(iseg).wse_peak_ind)-seg(iseg).wse_min(seg(iseg).wse_peak_ind);
        seg(iseg).meanvar=max(seg(iseg).wse_max(seg(iseg).wse_peak_ind)-seg(iseg).wse_mean(seg(iseg).wse_peak_ind), ...
            seg(iseg).wse_mean(seg(iseg).wse_peak_ind)-seg(iseg).wse_min(seg(iseg).wse_peak_ind) );
        seg(iseg).meanmedian=seg(iseg).wse_mean(seg(iseg).wse_peak_ind)-seg(iseg).wse_median(seg(iseg).wse_peak_ind);
        
        
            
    
        % plots to check results
        figure;
        fprintf('there are %d stations in segment No. %d ...\n', length(seg_station), iseg);
        for j=1:length(seg_station)
            plot(tdate,wse{seg_station(j)}*3.28083);hold on;
        end
        h(1)=plot(seg(iseg).tdate,seg(iseg).wse_mean*3.28083,  'b-','LineWidth',1.5);hold on;
        h(2)=plot(seg(iseg).tdate,seg(iseg).wse_median*3.28083,'r-','LineWidth',1.5);hold on;
        h(3)=plot(seg(iseg).tdate,seg(iseg).wse_min*3.28083,  'b--','LineWidth',1.5);hold on;
        h(4)=plot(seg(iseg).tdate,seg(iseg).wse_max*3.28083,'r--','LineWidth',1.5);hold on;
        plot( [tdate_peak tdate_peak],[-100 100],'k-' );hold on;
%         ylim([x_min-0.1)*3.28083 (x_max+0.1)*3.28083]);
%         xlim([min(tdate) max(tdate)]);
        xlim([tdate_peak-0.5 tdate_peak+0.5]);
        if istorm == 4
            ylim([seg(iseg).wse_mean(seg(iseg).wse_peak_ind)*3.28083-0.3 seg(iseg).wse_mean(seg(iseg).wse_peak_ind)*3.28083+0.3]);
        else
            ylim([seg(iseg).wse_mean(seg(iseg).wse_peak_ind)*3.28083-0.2 seg(iseg).wse_mean(seg(iseg).wse_peak_ind)*3.28083+0.2]);
        end
        hold off;
        datetick('x','mm/dd/HH','keeplimits','keepticks'); grid on;
        xlabel('date');
        ylabel('WSE (ft)');
        legend(h,'mean','median','min','max','Location','Southeast');
        title(strcat('Storm: ', theNC(1:end-3), ' Segment= ', num2str(iseg) ),'interprete','none');
        set(gcf,'PaperUnits','inches','PaperPosition',[0 0 11 6]);
        print(gcf,'-r300','-djpeg',strcat('./plots/storm_',theNC(1:end-3),'_seg',num2str(iseg),'_peakzoom.jpg'));
%         clf;
    end
    
%     write out .csv
    for i=1:length(tdate)
        fprintf(fid,'%s,',datestr(tdate(i),'ddmmmyyyy HH:MM'));
        for ista=1:nstation
            fprintf(fid,'%10.4f,',wse{ista}(i)*3.28083);
        end
        for iseg=1:8
            fprintf(fid,'%10.4f,',seg(iseg).wse_min(i)*3.28083, seg(iseg).wse_max(i)*3.28083,seg(iseg).wse_median(i)*3.28083,seg(iseg).wse_mean(i)*3.28083);
        end
        for iseg=1:8
            fprintf(fid,'%10.4f,',seg(iseg).maxvar*3.28083, seg(iseg).meanvar*3.28083,seg(iseg).meanmedian*3.28083);
        end
        fprintf(fid,'\n');
    end
    fclose(fid);
    clear theMat theNC theCSV t wse tdate varname value seg
    clear time_station_* data_station*
end




