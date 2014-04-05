function [] = batchFeatureExtraction(folderPath)
%=========================================================================
% batchFeatureExtraction - Computes and writes MFCC's for a set of speech waveform.
% 
% Input parameters: folderPath - path to the folder with input waveforms
%
%
% Diego Evin
% July 10, 2013
% diegoevin_at_gmail.com
%=========================================================================

disp('empieza el script');

tWindow = 25; %100;                % analysis frame duration (ms)
tStep = 10;                 % analysis frame shift (ms)
alpha = 0.97;                 % preemphasis coefficient
freqRange = [ 50 3800 ];       % frequency range to consider
fbChannels = 25;            % number of filterbank channels 
numCep = 13;                % number of cepstral coefficients
lifter = 22;                % cepstral sine lifter parameter

% List the *.wav files in folder
fileList = dir([folderPath, '*.wav']);
disp('La lista de archivos es   ....');
disp(fileList);

for i=1:length(fileList)
    [pathstr, fname, ext] = fileparts([folderPath,char(fileList(i).name)]);
    
    outputFileName = [pathstr, '/', fname, '.mfcc'];
    filename=[pathstr, '/', fname, ext];

    disp('filename');
    disp(filename);

    % Open output file for writting
    fileID = fopen(outputFileName, 'w');
    [ CC, FBE] = wav2mfcc( filename, tWindow, tStep, alpha, freqRange, fbChannels, numCep, lifter );
    [nCeps, nframes] = size(CC);
    
    for j=1:nframes
        fprintf(fileID, '[');
        for i=1:nCeps
            fprintf(fileID,'%f\t',CC(i,j));
        end
        fprintf(fileID,'] \n');
    end
    fclose(fileID);
end



% batchFeatureExtraction('D:\Facultad\ECI 2013\Material\Datos\NumbersDB\')
